import autogen
import sys
import re
import time
import google.generativeai as genai
from google.api_core import exceptions
from google.generativeai.types import generation_types

# =================================================================
# 1. จัดอันดับ Model Priority
# =================================================================

MODEL_PRIORITY_LIST = [
    # 🏆 Tier 1: เทพเจ้า
    "models/gemini-3-pro-preview",
    "models/deep-research-pro-preview-12-2025",
    "models/gemini-2.5-pro",
    "models/gemini-pro-latest",
    
    # 🚀 Tier 2: ยอดมนุษย์
    "models/gemini-3-flash-preview",
    "models/gemini-2.5-flash",
    "models/gemini-flash-latest",
    "models/gemini-2.0-flash-exp", 
    
    # 🐎 Tier 3: ม้างาน
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    
    # 🛡️ Tier 4: ตัวประหยัด
    "models/gemini-2.5-flash-lite-preview-09-2025",
    "models/gemini-2.0-flash-lite-preview-09-2025",
    "models/gemini-2.0-flash-lite-001",
    "models/gemini-flash-lite-latest",

    # 🧱 Tier 5: ตัวปิดท้าย (Gemma)
    "models/gemma-3-27b-it",
    "models/gemma-3-12b-it",
    "models/gemma-3-4b-it"  # 🛑 ตัวสุดท้ายของรอบ
]

# =================================================================
# 💉 2. THE TIME STOPPER (Looping Edition)
# =================================================================
_original_generate_content = genai.GenerativeModel.generate_content

def _retry_on_quota_error(self, *args, **kwargs):
    current_model = self.model_name.lower()
    
    # เช็คว่าเป็นตัวปิดท้ายหรือไม่?
    last_resort_name = MODEL_PRIORITY_LIST[-1].split('/')[-1]
    is_the_last_one = last_resort_name in current_model

    try:
        return _original_generate_content(self, *args, **kwargs)
    
    # 🛑 1. กรณี Quota เต็ม (หัวใจสำคัญของการวนลูป)
    except exceptions.ResourceExhausted as e:
        
        # ถ้าไม่ใช่ตัวสุดท้าย -> ให้ Error เลยทันที (เพื่อให้ AutoGen เปลี่ยนไปตัวถัดไป)
        if not is_the_last_one:
            # print(f"⏩ {current_model} เต็ม! ข้าม...") 
            raise e 

        # 🔄 ถ้าเป็นตัวสุดท้าย (Gemma) -> ให้ "พักยก" ก่อนเริ่มรอบใหม่
        print(f"\n♻️ จบรอบการลองโมเดล! ({current_model} เต็ม).")
        print(f"⏳ กำลังพัก 30 วินาที... เพื่อวนกลับไปใช้ 'Gemini Pro' ใหม่...")
        
        wait_time = 30 
        for remaining in range(wait_time, 0, -1):
            sys.stdout.write(f"\r💤 Resting... {remaining:02d}s  ")
            sys.stdout.flush()
            time.sleep(1)
        
        print("\n🚀 Starting New Cycle! (Back to Tier 1)")
        
        # 🔥 สำคัญมาก: ต้อง raise Error เพื่อบอก AutoGen ว่า "ตัวนี้ก็ใช้ไม่ได้ ไปตัวต่อไปเถอะ"
        # (ซึ่งตัวต่อไป คือ Gemini Pro ของรอบใหม่นั่นเอง)
        raise e

    # 🛑 2. กรณีโดน Block เนื้อหา (Safety)
    except generation_types.BlockedPromptException:
        print(f"\n🚫 Blocked Content ({current_model}). Skipping...")
        raise exceptions.ResourceExhausted("Simulating Quota Error to skip blocked model") 
        # แกล้งบอกว่า Quota เต็ม เพื่อให้มันข้ามไปลองตัวอื่นเผื่อรอด

    except Exception as e:
        raise e

genai.GenerativeModel.generate_content = _retry_on_quota_error

# =================================================================
# 3. API Keys & Looping Config List
# =================================================================

# ⚠️ ใส่ API Key
API_KEYS = [
    "AIzaSyBUbet5_GttDdeHWPqFsoABvIaIbSxc5Kk",
    "AIzaSyBoER95iWm-8G7PE5CSon3kTzdkq_uN9uw",
    "AIzaSyBzfWWfU2ijVXLTji_WuBTyvzyOPI0vkAQ",
    "AIzaSyAmu8vdtLYgYf6pSIJJfnd5AQPV3cK2Zr8",
]

def get_fallback_config_list():
    config_list = []
    
    # 🔥 สร้าง Infinite Loop ที่นี่!
    # เราจะวนลูปสร้างลิสต์ซ้ำๆ 50 รอบ (เหมือนมีโมเดลให้ลอง 1,500 ตัว)
    # ลำดับจะเป็น: [Pro, Flash, Lite, Gemma] -> [Pro, Flash, Lite, Gemma] -> ...
    
    for _ in range(50):  # วนลูป 50 รอบ
        for model in MODEL_PRIORITY_LIST:
            for key in API_KEYS:
                config_list.append({
                    "model": model,
                    "api_key": key,
                    "api_type": "google",
                    "safety_settings": [
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                })
    return config_list

fallback_config_list = get_fallback_config_list()

# =================================================================
# 1. Logger System (ระบบบันทึกการสนทนา)
# =================================================================
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("meeting_log.txt", "a", encoding="utf-8")

    def write(self, message):
        # 1. ส่วนของ Terminal: ให้แสดงผลแบบดิบๆ (มีสีสวยงาม)
        self.terminal.write(message)
        
        # 2. ส่วนของไฟล์: ให้ลบโค้ดสีออกก่อน (Clean Text)
        # ใช้ Regex ลบ pattern สีทิ้งไป
        clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message) 
        self.log.write(clean_message)  
        
        # บันทึกทันที
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def start_logging():
    sys.stdout = Logger()
    print("🔴 System Logging Started: meeting_log.txt")

# =================================================================
# 5. Export Configurations
# =================================================================

# ทุกคนใช้ List เดียวกัน เพราะเราต้องการให้ "รอด" สำคัญที่สุด
# แต่ยังปรับ Temperature แยกได้เหมือนเดิม

# 🧊 สายเป๊ะ (Admin, Data)
config_research = {
    "config_list": fallback_config_list,
    "temperature": 0.3,       # ความกาวต่ำติดดิน
    "top_p": 0.5,             # เลือกแต่คำที่ชัวร์ๆ
    "top_k": 20,              # ตัดคำแปลกๆ ทิ้งหมด
    "max_output_tokens": 1500, # ห้ามบ่นยาวเกิน 1000 คำ (ประหยัดโควตา)
}

# ⚖️ สายตรรกะ (Editor)
config_editor = {
    "config_list": fallback_config_list,
    "temperature": 0.7,       # ยืดหยุ่นได้บ้าง
    "top_p": 0.7,             # ใช้คำศัพท์ระดับปัญญาชน
    "top_k": 40,              # มาตรฐาน
    "max_output_tokens": 2000, # วิจารณ์งานได้ยาวพอประมาณ
}

# 🔥 สายอาร์ต (Writer)
config_writer = {
    "config_list": fallback_config_list,
    "temperature": 0.9,       # ปล่อยของเต็มที่
    "top_p": 1.0,             # เปิดรับทุกความเป็นไปได้ของภาษา
    "top_k": 60,              # ให้โอกาสคำแปลกๆ ได้เกิด
    "max_output_tokens": 9216, # เขียนนิยายได้ยาวสะใจ (สูงสุดของรุ่น Flash)
}

# config_research = config_strict   # ให้ Data ใช้ config_strict
# config_admin = config_strict      # ให้ Admin ใช้ config_strict
# config_editor = config_logical    # ให้ Editor ใช้ config_logical
# config_writer = config_creative   # ให้ Writer ใช้ config_creative
# config_artist = config_creative   # ให้ Artist ใช้ config_creative