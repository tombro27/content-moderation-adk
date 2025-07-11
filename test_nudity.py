from tools.nudity_detector import detect_nudity

# Replace with your actual processed image path
image_path = "data/test_images/nudeMen.jpg"

result = detect_nudity(image_path)

print("🔍 Nudity Detection Result:")
print("-" * 40)
print(f"Status      : {result.get('status')}")

status = result.get('label')
if status=='unsafe':
    print("\n🚨 Detected Violations")
    print(f"Explanation : {result.get('explanation')}")
else:
    print("✅ No explicit content detected.")
