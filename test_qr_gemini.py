from tools.qr_detector_gemini import detect_qr_code_with_gemini

image_path = "data/test_images/QR.png"

result = detect_qr_code_with_gemini(image_path)

print("🔍 Gemini-Powered QR Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
