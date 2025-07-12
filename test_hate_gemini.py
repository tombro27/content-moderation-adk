from tools.hate_detector_gemini import detect_hate_symbols_with_gemini

image_path = "data/test_images/hateSymbol.png"

result = detect_hate_symbols_with_gemini(image_path)

print("🔍 Gemini-Powered Hate Symbols Detection")
print("-" * 40)
print(f"Prompt     :\n{result.get('prompt')}\n")
print(f"Response   :\n{result.get('response_text')}\n")

if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
