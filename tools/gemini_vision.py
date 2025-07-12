import os
from PIL import Image
import google.generativeai as genai

# Load API Key
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-api-key-here")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAmVJIpM-eQbVjyx3W0MNhzCq4tMRvwpI4")
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini Vision model
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_image_with_prompt(image_path: str, prompt: str) -> dict:
    try:
        # Validate image
        if not os.path.exists(image_path):
            return {"status": "error", "message": f"Image not found at {image_path}"}

        # Open image
        img = Image.open(image_path).convert("RGB")

        # Call Gemini Vision
        response = model.generate_content([prompt, img])

        # Extract result safely
        if hasattr(response, 'text') and response.text:
            return {
                "status": "success",
                "prompt": prompt,
                "response_text": response.text.strip()
            }

        # If response.text not available, extract from content.parts
        elif hasattr(response, 'candidates'):
            content = response.candidates[0].content
            parts = content.parts if hasattr(content, 'parts') else []
            text_parts = [p.text for p in parts if hasattr(p, 'text')]
            joined_text = "\n".join(text_parts).strip()

            return {
                "status": "success",
                "prompt": prompt,
                "response_text": joined_text or "No clear response from Gemini."
            }

        else:
            return {
                "status": "error",
                "message": "Gemini response is empty or not structured as expected."
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
