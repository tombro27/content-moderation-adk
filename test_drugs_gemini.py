from tools.drugs_detector_gemini import detect_drugs_with_gemini

image_path = "data/test_images/vapes.jpg"

result = detect_drugs_with_gemini(image_path)

print("🔍 Gemini-Powered Drugs Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
