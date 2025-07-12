from tools.gemini_vision import analyze_image_with_prompt

def detect_qr_code_with_gemini(image_path: str) -> dict:
    with open("configs/prompts/qr_prompt.txt", "r") as f:
        prompt = f.read()

    return analyze_image_with_prompt(image_path, prompt)
