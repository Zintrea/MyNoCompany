import sys
import os

print("--- 🔍 Detective Python ---")
print(f"1. Current Directory: {os.getcwd()}")
print(f"2. Python Executable: {sys.executable}")
print("3. Looking for libraries in these paths:")
for p in sys.path:
    print(f"   - {p}")

print("\n4. Attempting import...")
try:
    import autogen
    print("✅ SUCCESS! Found autogen at:", autogen.__file__)
except ImportError as e:
    print("❌ FAILED! Error details:", e)
    
    # เช็คว่ามีไฟล์ชื่อซ้ำไหม
    files = os.listdir(".")
    if "autogen.py" in files:
        print("😱 FOUND IT! You have a file named 'autogen.py' here. Rename it!")
    elif "autogen" in files:
        print("😱 FOUND IT! You have a folder named 'autogen' here. Rename it!")