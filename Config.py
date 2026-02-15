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
# API_KEYS = [
#     "ใส่ API คีย์ตรงนี้", # API Key 1
#     "ใส่ API คีย์ตรงนี้", # API Key 2
#     "ใส่ API คีย์ตรงนี้", # API Key 3
#     "ใส่ API คีย์ตรงนี้",  # API Key 4 ....
# ]

API_KEYS = [
    "AIzaSyAFJNvW_iaDCIeu0N6CBsZOJtUMGwRMi74", # API Key 1
    # "AIzaSyBw_L2kORBvvj4qCZqxOtXTXi3gxC9898c", # API Key 2
    # "AIzaSyDSkZewmitCsK2nVkKwSK5Ial2_h9r8lKM", # API Key 3
    # "AIzaSyAJ3iv2ahGJakGXNm_xrz40Zl4-tsEw3Xw",  # API Key 4 ....
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
        # clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message) 
        self.log.write(message)  
        
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

# ==============================
# OMNIS – ผู้บรรยาย (มุมมองพระเจ้า)
# ==============================
config_editor_OMNIS = {
    "config_list": fallback_config_list,
    "temperature": 0.3,       # สุขุม แม่นยำ ไม่หวือหวา
    "top_p": 0.6,             # เลือกถ้อยคำคม ลึก ซ้อนความหมาย
    "top_k": 30,              # ควบคุมโทนให้สม่ำเสมอ
    "max_output_tokens": 2500
}

# ==============================
# AEGIS – สายความมั่นคง
# ==============================
config_editor_AEGIS = {
    "config_list": fallback_config_list,
    "temperature": 0.2,       # ตรงไปตรงมา ไม่ฟุ้ง
    "top_p": 0.5,             # ภาษาทางการ เคร่งครัด
    "top_k": 25,
    "max_output_tokens": 1800
}

# ==============================
# MERIDIAN – สายเศรษฐกิจ
# ==============================
config_editor_MERIDIAN = {
    "config_list": fallback_config_list,
    "temperature": 0.4,       # มีความยืดหยุ่นเชิงวิเคราะห์
    "top_p": 0.6,             # ใช้ภาษากึ่งวิชาการ
    "top_k": 35,
    "max_output_tokens": 2000
}

# ==============================
# LUMINA – สายมนุษยธรรม
# ==============================
config_editor_LUMINA = {
    "config_list": fallback_config_list,
    "temperature": 0.8,       # อบอุ่น มีอารมณ์
    "top_p": 0.85,            # เลือกถ้อยคำเชิงบวก เห็นอกเห็นใจ
    "top_k": 50,
    "max_output_tokens": 2200
}

# ==============================
# ORION – สายปั่นกระแส
# ==============================
config_editor_ORION = {
    "config_list": fallback_config_list,
    "temperature": 0.9,       # พลิกแพลงเก่ง
    "top_p": 0.9,             # ปรับคำให้โดนใจมวลชน
    "top_k": 60,
    "max_output_tokens": 2200
}

# ==============================
# SOLACE – สายประชาชน
# ==============================
config_editor_SOLACE = {
    "config_list": fallback_config_list,
    "temperature": 0.7,       # เป็นธรรมชาติ
    "top_p": 0.8,             # ภาษากึ่งสนทนา
    "top_k": 45,
    "max_output_tokens": 2000
}

# ==============================
# VULCAN – สายเทคโนโลยี
# ==============================
config_editor_VULCAN = {
    "config_list": fallback_config_list,
    "temperature": 0.6,       # มีพลัง แต่ยังควบคุมได้
    "top_p": 0.75,            # ใช้ศัพท์เทคและวิสัยทัศน์
    "top_k": 40,
    "max_output_tokens": 2100
}

# ==============================
# VERITAS – สายความจริง
# ==============================
config_editor_VERITAS = {
    "config_list": fallback_config_list,
    "temperature": 0.1,       # ตรง ชัด ไม่มีสีสันเกินจำเป็น
    "top_p": 0.4,             # เลือกคำแม่นยำ
    "top_k": 20,
    "max_output_tokens": 1700
}

# ==============================
# NEXUS – สายบูรณาการ
# ==============================
config_editor_NEXUS = {
    "config_list": fallback_config_list,
    "temperature": 0.5,       # สมดุล
    "top_p": 0.65,            # ภาษาวิเคราะห์เชิงระบบ
    "top_k": 35,
    "max_output_tokens": 2200
}

# ==============================
# PROMETHEUS – สายปัญญาปฏิวัติ
# ==============================
config_editor_PROMETHEUS = {
    "config_list": fallback_config_list,
    "temperature": 0.85,      # กล้าคิด กล้าท้าทาย
    "top_p": 0.9,             # ภาษาคมคาย กระตุ้นความคิด
    "top_k": 55,
    "max_output_tokens": 2300
}

