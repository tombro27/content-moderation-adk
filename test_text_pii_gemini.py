import pytesseract
from PIL import Image
from tools.gemini_vision import analyze_image_with_prompt
import os

# ✅ Set this path if you're on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_text_pii_with_gemini(image_path: str) -> dict:
    try:
        # Check if image exists
        if not os.path.exists(image_path):
            return {"status": "error", "message": f"Image not found: {image_path}"}

        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(Image.open(image_path))

        if not text.strip():
            return {
                "status": "success",
                "prompt": "",
                "response_text": "No readable text found in image.",
                "extracted_text": ""
            }

        # Load Gemini prompt
        prompt_path = "configs/prompts/text_pii_prompt.txt"
        if not os.path.exists(prompt_path):
            return {"status": "error", "message": f"Prompt file not found: {prompt_path}"}

        with open(prompt_path, "r") as f:
            base_prompt = f.read()

        # Final prompt to send to Gemini
        full_prompt = f"{base_prompt.strip()}\n\nExtracted Text:\n{text.strip()}"

        # Send to Gemini
        gemini_result = analyze_image_with_prompt(image_path, full_prompt)

        # Merge response
        return {
            "status": gemini_result.get("status", "error"),
            "prompt": full_prompt,
            "response_text": gemini_result.get("response_text", ""),
            "extracted_text": text.strip()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "prompt": "",
            "response_text": "",
            "extracted_text": ""
        }
