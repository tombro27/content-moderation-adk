from tools.gemini_vision import analyze_image_with_prompt

image_path = "data/test_images/violence.jpg"

prompt = """
You're an image moderation agent.
Does this image contain any of the following:
- Violence or blood
- Injuries or gore
- Dead bodies or self-harm
- Weapons (gun, knife, etc.)
Please answer YES or NO, then explain.
"""

result = analyze_image_with_prompt(image_path, prompt)

print("🔍 Gemini Analysis Result:")
print("-" * 40)
print(f"Prompt     : {result.get('prompt')}")
print(f"Response   :\n{result.get('response_text')}")
if result.get("status") != "success":
    print("❌ ERROR:", result.get("message"))
