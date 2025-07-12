from tools.violence_detector import detect_violence

image_path = "data/test_images/gun.jpg"

result = detect_violence(image_path)

print("🔍 Violence Detection Result:")
print("-" * 40)
print(f"Status      : {result.get('status')}")
print(f"Explanation : {result.get('explanation')}")

if result.get("violence"):
    print("\n🚨 Violations Detected:")
    for v in result.get("violations", []):
        print(f" - {v['label']} (Score: {v['score']})")
else:
    print("✅ Image is clean. No violent content found.")
