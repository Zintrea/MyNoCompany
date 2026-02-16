import autogen
import Config
import Agents
import os

# =================================================================
# 1. Start Logging & Knowledge Base
# =================================================================
Config.start_logging()

# ชื่อไฟล์เก็บความจำระยะยาว (Database)
DB_FILE = "company_database.txt"

# ฟังก์ชันอ่านประวัติเก่า (เพื่อให้ Data เรียนรู้)
def load_company_memory():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "ยังไม่มีประวัติผลงานในอดีต (นี่คือโปรเจกต์แรก)"

# ฟังก์ชันบันทึกความทรงจำ (เฉพาะแก่นเรื่อง)
def save_project_memory(project_name, summary, feedback):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*30}\n")
        f.write(f"📌 โปรเจกต์: {project_name}\n")
        f.write(f"📝 พล็อตย่อ: {summary}\n")
        f.write(f"📊 ผลตอบรับ/บทเรียน: {feedback}\n")
        f.write(f"{'='*30}\n")
    print(f"✅ บันทึกข้อมูล '{project_name}' ลงฐานข้อมูลบริษัทเรียบร้อย!")

# =================================================================
# 2. Setup Meeting Room
# =================================================================
groupchat = autogen.GroupChat(
    agents=Agents.pitch_team,
    messages=[],
    max_round=15, # ซ้อมสัก 15 ยกกำลังดี
    allow_repeat_speaker=False,
    speaker_selection_method="auto"
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    llm_config=Config.config_logic,
    system_message="""
    ROLE: Pitch Moderator.
    FLOW:
    1. Mr. Shark or Dr. Logic ATTACKS the pitch.
    2. The CEO DEFENDS.
    3. The Wingman SUPPORTS (optional).
    4. Repeat.
    """
)

# =================================================================
# 3. Kick-off (เริ่มโปรเจกต์ใหม่)
# =================================================================

print("\n🚀 MyNoCompany: กลับมาทำงานแล้ววว")
print(f"📂 โหลดนิยายที่เคยเขียนไว้เข้ามา")

# โหลดความทรงจำเก่ามาใส่ในตัวแปร
print("\n" + "="*50)
print("🎤 PITCHING SIMULATOR: READY")
print("="*50)
print("กรุณาวางเนื้อหาที่จะ Pitch วันนี้ลงไป (แล้วกด Enter 2 ครั้ง):")
print("(เช่น: สวัสดีครับ วันนี้ผมมานำเสนอแอปพลิเคชันขายไก่ทอดด้วย AI...)")
user_pitch_content = input(">>> ")

# สั่งงาน Admin โดยยัดเยียด "บทเรียนในอดีต" ให้ Data รู้ด้วย
initial_prompt = f"""
[SCENARIO: GADGET PRESENTATION DEFENSE ROOM]

We are rehearsing a class presentation about this gadget:
"{user_pitch_content}"

Professor Critical & Curious Classmate:
Your mission is to challenge this presentation like a real Q&A session.
Ask the kinds of questions teachers and students would ask.
Find unclear slides, weak logic, missing data, or confusing explanations.

Presenter & Tech Assistant:
Defend clearly, like a student presenting in class.
Answer as if this is the real presentation day.

Start the Q&A simulation now.
"""

# เริ่มการประชุม
Agents.admin_user.initiate_chat(
    manager,
    message=initial_prompt
)

# =================================================================
# 4. Post-Production (จบงานแล้วเก็บของ)
# =================================================================

print("\n" + "#"*50)
print("🛑 จบการประชุมโปรเจกต์นี้")
save_choice = input("ต้องการบันทึก 'พล็อตและผลตอบรับ' ของเรื่องนี้เก็บไว้ไหม? (y/n): ")

if save_choice.lower() == 'y':
    summary = input("สรุปพล็อตย่อ (Copy จากที่คุยกันมาวาง): ")
    feedback = input("สรุปผลตอบรับ/จุดเด่นจุดด้อย (Copy คำวิจารณ์ของ Data มาวาง): ")
    save_project_memory( summary, feedback)
    print("💾 Saved! เริ่มเรื่องใหม่ได้เลย (รันโปรแกรมใหม่)")
else:
    print("🗑️ Discarded. ข้อมูลเรื่องนี้จะหายไปตลอดกาล")