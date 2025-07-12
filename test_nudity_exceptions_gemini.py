from tools.nudity_exceptions_detector_gemini import detect_nudity_exceptions_with_gemini

image_path = "data/test_images/exception.png"

result = detect_nudity_exceptions_with_gemini(image_path)

print("🔍 Gemini-Powered Nudity Exception Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
