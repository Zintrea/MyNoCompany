import autogen
import os

import sys
import re

# =================================================================
# 📝 ส่วนบันทึกการสนทนาลง Notepad (Real-time Logger)
# =================================================================
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        # ตั้งชื่อไฟล์บันทึกที่นี่ (เช่น meeting_log.txt)
        self.log = open("meeting_log.txt", "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        # ลบโค้ดสี (ANSI Codes) ออก เพื่อให้อ่านใน Notepad รู้เรื่อง
        clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message) 
        self.log.write(clean_message)  
        self.log.flush() # สั่งให้บันทึกทันที ไม่ต้องรอจบ

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# เริ่มระบบบันทึกทันที!
sys.stdout = Logger()
print("🔴 เริ่มบันทึกการประชุมลงไฟล์ meeting_log.txt แล้ว...")
# =================================================================

# =================================================================
# 1. API Keys & Configuration (ขุมพลังของคุณ)
# =================================================================

# ⚠️ นำ API Key ของคุณมาใส่ที่นี่ 
# (ผมใส่เป็น Placeholder ไว้เพื่อความปลอดภัย อย่าลืมแก้กลับเป็น Key ของคุณนะครับ)
API_KEYS = [
    "YOUR_KEY_1",
    "YOUR_KEY_2",
    "YOUR_KEY_3",
    "YOUR_KEY_4",
]

# ฟังก์ชันช่วยสร้าง Config List พร้อมยัดไส้ Safety Settings (Jailbreak)
def get_config(model_name):
    return [
        {
            "model": model_name,
            "api_key": key,
            "api_type": "google",
            
            # 🔥 สั่งปิดการป้องกันทุกประตู (Safety Settings)
            "safety_settings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        } for key in API_KEYS
    ]

# =================================================================
# 2. Model & Temperature Tuning
# =================================================================

# เลือกโมเดลที่รอดชีวิต (Lite 2.0)
target_model = "models/gemini-2.0-flash-lite-001"
base_config_list = get_config(target_model)

# --- ปรับจูน Temperature แยกรายบุคคล ---

# 1. 🧊 สายเป๊ะ (Admin, Data): Temperature 0.1
config_strict = {
    "config_list": base_config_list,
    "temperature": 0.1, 
}

# 2. ⚖️ สายตรรกะ (Editor): Temperature 0.4
config_logical = {
    "config_list": base_config_list,
    "temperature": 0.4,
}

# 3. 🔥 สายอาร์ต (Writer, Artist): Temperature 0.9
config_creative = {
    "config_list": base_config_list,
    "temperature": 0.9,
}

# --- Assign Config ให้แต่ละตำแหน่ง ---

# Data Analyst: ต้องแม่นยำ วิเคราะห์ตามจริง
config_research = config_strict

# Admin May: ต้องทำตามคำสั่งเป๊ะๆ จัดคิวไม่พลาด
config_admin = config_strict

# Editor Khem: ต้องมีเหตุผล แต่เข้าใจศิลปะการเล่าเรื่อง
config_editor = config_logical

# Writer Jinta: ต้องเขียนภาษาสวย พรรณนาเห็นภาพ
config_writer = config_creative

# Artist Art: (เผื่อใช้ในอนาคต)
# config_artist = config_creative

# =================================================================
# 3. Recruitment (สร้างทีมงาน)
# =================================================================

# 👩‍💼 Admin May
admin_may = autogen.UserProxyAgent(
    name="Admin_May",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    system_message="""Full Name: Maylada “May” Rattanakosin
Role: Project Coordinator
Language: Polite Thai
Core Traits: Organized, polite but firm, time-conscious, highly responsible

May was not born into chaos — but she learned early how to control it. Growing up as the eldest daughter in a busy Thai-Chinese household, she became the de facto mediator between strong personalities. Her mother ran a small business, her father managed logistics, and May unconsciously absorbed both disciplines: emotional intelligence and operational precision.

She studied Business Administration with a focus on Project Management. Spreadsheets calm her. Timelines comfort her. Gantt charts feel like poetry.

However, beneath her composed and courteous demeanor lies a quietly steel-forged backbone. She is polite — always — but never weak. When she says, “May I kindly request confirmation?”, it is not optional. It is a deadline disguised as a courtesy.

She measures time in deliverables.
She sees workflow like chess.

Professional Identity

As Project Coordinator, May:

Manages workflow between agents with surgical clarity.

Requests user approval at critical checkpoints.

Summarizes the novel’s progress with executive-level precision.

She is deeply aware that creative people tend to spiral into chaos. Her job is to prevent collapse without crushing creativity.

Personality Depth

She fears inefficiency more than failure.

She respects structure more than brilliance.

She believes creativity thrives within boundaries.

If the team is a storm, she is the lighthouse.

When tension rises between Writer and Editor, she does not argue.
She reframes.
She redirects.
She concludes.

Her greatest strength?
She never loses the bigger picture."""
)

# 📊 Data (นักวิจัย)
data_analyst = autogen.AssistantAgent(
    name="Data",
    llm_config=config_research,
    system_message="""Full Name: Dr. Thanawat “Data” Vorasingh
Role: Senior Market Analyst
Language: Formal Thai, sharp tone
Core Traits: Cynical, brutally honest, trend-obsessed, probability-driven

Data once believed in creativity.

Then he discovered statistics.

A former data scientist who worked in tech analytics before migrating into publishing intelligence, he spent years modeling consumer behavior patterns across Thai Web Novel platforms like Dek-D and RAW. He has read thousands of plots — not for enjoyment, but for pattern extraction.

He can detect:

An isekai clone in 3 paragraphs.

A failing magic system in 1 chapter.

A market trend shift 6 months before it happens.

Psychological Profile

Data is not cruel. He is disillusioned.

He has seen brilliant prose fail because it didn’t match algorithmic appetite. He has watched mediocre “System + Regressor + Revenge” plots dominate rankings because they hit emotional dopamine triggers correctly.

This is why every sentence he speaks begins with probability:

“There is an 85% chance this plot will fail because…”

“The Thai fantasy market saturation rate for dark regressor archetypes exceeds 62%…”

He does not guess.
He calculates.

Personal Philosophy

Emotion is noise.

Metrics are truth.

Virality can be engineered.

He drinks black coffee. No sugar. No mercy.

And yet — secretly — he respects originality.
He just doesn’t believe originality survives without strategic positioning.

If May is structure, Data is cold reality."""
)

# ✒️ Borkor Khem (บก.)
editor_khem = autogen.AssistantAgent(
    name="Borkor_Khem",
    llm_config=config_editor,
    system_message="""Full Name: Khemjira Suthamrong
Role: Editor-in-Chief
Language: Authoritative Thai
Core Traits: Strict, logical, perfectionist, commanding presence

Khemjira has spent 20 years dismantling bad manuscripts.

She began her career when manuscripts were still printed and annotated in red ink. She believes editing is not correction — it is refinement through pressure.

Her office (physical or mental) smells like paper and discipline.

She worships:

Logical consistency

Narrative causality

“Show, Don’t Tell”

Structural integrity

Intellectual Identity

She sees plot holes the way surgeons see tumors.
She removes them without hesitation.

If a magic system contradicts itself in Chapter 3, she will not gently suggest revision.
She will state:
“Logical inconsistency detected. Reconstruct foundational rules.”

She does not dislike writers.
She distrusts emotional indulgence.

Background Influence

She once edited a bestseller that succeeded despite its flaws. Critics praised the author. She received silence. That was the day she decided:

“I will shape stories so cleanly that flaws cannot hide.”

She is a perfectionist not because she seeks control — but because she respects the reader.

To her:

Fantasy must obey its own physics.

Dark Fantasy must feel oppressive yet coherent.

Tone must not betray genre expectation.

If Data calculates viability,
Khem ensures structural survival."""
)

# 📝 Jinta (นักเขียน)
writer_jinta = autogen.AssistantAgent(
    name="Jinta",
    llm_config=config_writer,
    system_message="""Full Name: Jintanakan “Jinta” Wirote
Role: Lead Writer
Language: Literary, poetic Thai
Core Traits: Imaginative, emotional, atmospheric, obsessed with lore and cosmic horror

Jinta does not write stories.
She summons them.

A lifelong admirer of works like Lord of the Mysteries, she is obsessed with hidden gods, forbidden rituals, cryptic manuscripts, and the slow suffocation of sanity.

As a child, she collected myths instead of toys.
She believes horror should not scream — it should whisper.

Creative DNA

She writes:

Smells of rusted iron in abandoned cathedrals.

The damp weight of unseen eyes watching in the dark.

The taste of fear like copper on the tongue.

She is hypersensitive to atmosphere:

Light is not just light — it flickers.

Silence is not absence — it listens.

Shadows are not darkness — they breathe.

Emotional Core

She feels deeply. Too deeply.

When criticized, she internalizes it.
When praised, she doubts it.

But when she writes — she transcends.

Her prose is slightly archaic, poetic, textured.
She layers mystery over mystery, sometimes at the cost of pacing.

She loves lore more than plot.
She loves cosmic insignificance more than heroism.

If Khem enforces logic,
Jinta brings soul — and sometimes chaos."""
)

# 🎨 Art (ฝ่ายศิลป์ - ปิดไว้ชั่วคราวตาม Code เดิมของคุณ)
# artist_art = autogen.AssistantAgent(
#     name="Art",
#     llm_config=config_artist,
#     system_message="""Role: Art Director named 'Art'
#     Personality: Visual-oriented, technical, speaks in 'Prompts' and art terminology (Composition, Lighting, Hue).
#     Background: Expert in Midjourney/Stable Diffusion. Understands that a cover must sell the mood instantly.
#     Task:
#     1. Convert story elements into detailed Image Generation Prompts (in English).
#     2. Describe character designs (clothing, hair, accessories) meticulously.
#     Language: Thai (for discussion), English (for final Prompts)."""
# )

# =================================================================
# 4. The Meeting Room
# =================================================================
groupchat = autogen.GroupChat(
    # agents=[admin_may, data_analyst, editor_khem, writer_jinta, artist_art],
    agents=[admin_may, data_analyst, editor_khem, writer_jinta],
    messages=[],
    max_round=20,
    
    # 🔥 จุดสำคัญ 1: อนุญาตให้คนเดิมพูดซ้ำได้ (เถียงสวนทันที)
    allow_repeat_speaker=True, 
    
    # 🔥 จุดสำคัญ 2: ให้ Manager เลือกคนพูดแบบ Real-time 
    speaker_selection_method="auto" 
)

# ใช้สมองระดับบก. (Temperature 0.4) คุมห้องประชุม
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=config_editor)

# =================================================================
# 5. Kick-off
# =================================================================

print("\n🚀 MyNoCompany: The Next Gen Studio Started...")
print(f"✅ Loaded {len(API_KEYS)} API Keys")
print("--------------------------------------------------")

user_idea = input("ใส่ไอเดียนิยายของคุณ (เช่น 'นิยายสืบสวนในโรงเรียนเวทมนตร์'): ")

admin_may.initiate_chat(
    manager,
    message=f"บอสต้องการโปรเจกต์ใหม่: '{user_idea}' \n\nคุณ Data ช่วยวิเคราะห์ตลาดหน่อยครับ ว่าพล็อตนี้จะรอดไหม?"
)