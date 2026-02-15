import sys
import os

print("1. Python ที่กำลังรันอยู่คือ:")
print(sys.executable)

print("\n2. โฟลเดอร์ที่ Python กำลังมองหา Library:")
for path in sys.path:
    print(f" - {path}")

print("\n3. ลอง Import autogen...")
try:
    import autogen
    print("✅ เจอ autogen แล้ว! อยู่ที่:", autogen.__file__)
except ImportError as e:
    print("❌ ยังไม่เจอ autogen เพราะ:", e)