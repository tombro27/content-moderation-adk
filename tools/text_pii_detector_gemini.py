import pytesseract
from PIL import Image
from tools.gemini_vision import analyze_image_with_prompt

# Optional: Set Tesseract path (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_text_pii_with_gemini(image_path: str) -> dict:
    try:
        # Extract text using Tesseract
        text = pytesseract.image_to_string(Image.open(image_path))

        if not text.strip():
            return {
                "status": "success",
                "prompt": "",
                "response_text": "No readable text found in image."
            }

        # Load Gemini prompt
        with open("configs/prompts/text_pii_prompt.txt", "r") as f:
            prompt = f.read()

        full_prompt = f"{prompt}\n\nExtracted Text:\n{text}"

        # Send to Gemini
        response = analyze_image_with_prompt(image_path, full_prompt)

        # Include extracted text for reference
        response["extracted_text"] = text
        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}
