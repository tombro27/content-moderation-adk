from tools.text_pii_vision_gemini import detect_text_pii_with_gemini_vision

image_path = "data/test_images/sample.jpg"

result = detect_text_pii_with_gemini_vision(image_path)

print("🔍 Gemini Vision-Only PII/Text Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
