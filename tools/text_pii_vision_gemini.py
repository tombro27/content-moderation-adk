from tools.gemini_vision import analyze_image_with_prompt

def detect_text_pii_with_gemini_vision(image_path: str) -> dict:
    try:
        with open("configs/prompts/text_pii_vision_prompt.txt", "r") as f:
            prompt = f.read()

        return analyze_image_with_prompt(image_path, prompt)

    except Exception as e:
        return {"status": "error", "message": str(e)}
