import google.generativeai as genai

# ==========================================
# 1. ใส่ API Key ทั้งหมดของคุณที่นี่
# ==========================================
API_KEYS = [
    "AIzaSyBUbet5_GttDdeHWPqFsoABvIaIbSxc5Kk",
    "AIzaSyBoER95iWm-8G7PE5CSon3kTzdkq_uN9uw",
    "AIzaSyBzfWWfU2ijVXLTji_WuBTyvzyOPI0vkAQ",
    "AIzaSyAajOeB_LN_Q3EyqM5R_jsBK-9wov2I3j4",
    "AIzaSyAmu8vdtLYgYf6pSIJJfnd5AQPV3cK2Zr8",
]

print(f"🔍 กำลังตรวจสอบ Model จากทั้ง {len(API_KEYS)} Keys...\n")

for index, key in enumerate(API_KEYS):
    print(f"🔑 Key #{index+1} ({key[:5]}...):")
    
    try:
        genai.configure(api_key=key)
        
        # ดึงรายชื่อ Model ทั้งหมด
        all_models = genai.list_models()
        
        found_models = []
        for m in all_models:
            # เราจะเอาเฉพาะ Model ที่คุยได้ (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                found_models.append(m.name)
        
        if found_models:
            print("   ✅ พบ Model ที่ใช้ได้:")
            for model_name in found_models:
                print(f"      - {model_name}")
        else:
            print("   ⚠️ Key นี้ใช้ได้ แต่ไม่พบ Model สำหรับ Chat")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        
    print("-" * 40)

print("\n✅ เสร็จสิ้น! ให้เลือกชื่อ Model (เช่น models/gemini-1.5-pro-latest) ไปใส่ใน Config")