import autogen
import Config
import Agents
import os

# =================================================================
# 1. Start Logging
# =================================================================
Config.start_logging()

DB_FILE = "meeting_history.txt"

def load_meeting_history():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "ยังไม่มีประวัติการเสนอขาย"

def save_meeting_history(shop_name, summary, result):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*30}\n")
        f.write(f"🏪 ร้าน: {shop_name}\n")
        f.write(f"📝 สรุปการเสนอ: {summary}\n")
        f.write(f"📊 ผลลัพธ์: {result}\n")
        f.write(f"{'='*30}\n")
    print(f"✅ บันทึกข้อมูล '{shop_name}' ลงฐานข้อมูลเรียบร้อย!")

# =================================================================
# 2. Setup Meeting Room
# =================================================================
groupchat = autogen.GroupChat(
    agents=Agents.team_members,
    messages=[],
    max_round=50,
    allow_repeat_speaker=True,
    speaker_selection_method="auto"
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    llm_config=Config.config_editor
)

# =================================================================
# 3. Kick-off (เริ่มโปรเจกต์)
# =================================================================

print("\n🎓 โปรเจกต์ Website สำหรับร้านท้องถิ่น")
print(f"📂 โหลดประวัติการเสนอขายเก่า")

past_lessons = load_meeting_history()

shop_name = input("ชื่อร้านที่จะไปเสนอ: ")
shop_location = input("ที่ตั้ง (เช่น ซอยสุขุมวิท 15): ")

initial_prompt = f"""
สถานการณ์: นักศึกษา 2 คน (Pong และ Mei) ต้องการเสนอทำเว็บไซต์ให้กับร้านน้ำชาบู้บ
ชื่อร้าน: {shop_name}
ที่ตั้ง: {shop_location}

--- ข้อมูลอ้างอิงจากการเสนอครั้งก่อน ---
{past_lessons}
---------------------------------------------------

เป้าหมาย: ให้ทีมงาน (Pong และ Mei) เสนอขายเว็บไซต์ให้กับร้าน {shop_name}

ขั้นตอนการเสนอ:
1. ถามความสนใจของเจ้าของร้านในการมีเว็บไซต์
2. ถามความต้องการรูปแบบเว็บไซต์ที่ต้องการ
3. เสนอบริการพัฒนาเว็บไซต์ตามความต้องการ
4. ถ้าเจ้าของร้านปฏิเสธแรง ให้ใช้คำพูดโน้มน้าวใจด้วยทักษะการขาย
5. ถ้าเจ้าของร้านยังไม่สนใจ ให้มอบนามบัตรแล้วลากลับ

หมายเหตุ:
- เจ้าของร้าน (Auntie) ไม่ถนัดเทคโนโลยี ชอบโซเชียลมีเดียมากกว่า
- พนักงาน (Kung) กังวลว่าเว็บไซต์จะทำให้ลูกค้ามาที่ร้านน้อยลง ส่งผลต่อรายได้
- ให้ทุกคนพูดคุยเป็นภาษาไทย
- พยายามโน้มน้าวใจให้สำเร็จ แต่ถ้าไม่ได้ก็จบที่นามบัตร
"""

Agents.student_1.initiate_chat(
    manager,
    message=initial_prompt
)

# =================================================================
# 4. Post-Meeting (จบงานแล้วเก็บของ)
# =================================================================

print("\n" + "#"*50)
print("🛑 จบการเสนอขาย")
save_choice = input("ต้องการบันทึก 'ผลการเสนอ' ไว้ไหม? (y/n): ")

if save_choice.lower() == 'y':
    summary = input("สรุปการเสนอ (Copy จากที่คุยกันมาวาง): ")
    result = input("ผลลัพธ์ (ขายได้/ปฏิเสธ/นามบัตร): ")
    save_meeting_history(shop_name, summary, result)
    print("💾 Saved! ไปร้านใหม่ได้เลย (รันโปรแกรมใหม่)")
else:
    print("🗑️ Discarded. ข้อมูลเรื่องนี้จะหายไปตลอดกาล")
