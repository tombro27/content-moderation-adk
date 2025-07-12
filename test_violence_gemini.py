from tools.violence_detection_gemini import detect_violence_with_gemini

image_path = "data/test_images/blood.jpg"

result = detect_violence_with_gemini(image_path)

print("🔍 Gemini-Powered Violence Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
