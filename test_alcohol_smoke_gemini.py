from tools.alcohol_smoke_detector_gemini import detect_alcohol_smoke_with_gemini

image_path = "data/test_images/alcohol.jpg"

result = detect_alcohol_smoke_with_gemini(image_path)

print("🔍 Gemini-Powered Alcohol/Smoking Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
