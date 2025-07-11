from nudenet import NudeDetector
import os

# Load the detector once globally
detector = NudeDetector()

def detect_nudity(image_path: str) -> dict:
    """
    Uses NudeNet's NudeDetector to detect nudity in an image.
    Returns:
        - status: success or error
        - violations: list of detected regions (breast, genitals, etc.)
        - explanation: reasoning
    """
    if not os.path.exists(image_path):
        return {"status": "error", "message": "Image not found"}

    try:
        detections = detector.detect(image_path)

        if not detections:
            return {
                "status": "success",
                "violations": [],
                "explanation": "No nudity or explicit content detected."
            }

        # Parse detections: each is a dict with label, score, box
        parsed = []
        for item in detections:
            parsed.append({
                "label": item["label"],
                "score": round(item["score"], 2),
                "box": item["box"]  # [x1, y1, x2, y2]
            })

        explanation = f"Detected {len(parsed)} explicit region(s): " + ", ".join(
            [f"{d['label']} ({d['score']})" for d in parsed]
        )

        return {
            "status": "success",
            "violations": parsed,
            "explanation": explanation
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
