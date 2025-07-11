from nudenet import NudeDetector
import os

# Load detector once globally
detector = NudeDetector()

def detect_nudity(image_path: str) -> dict:
    """
    Uses NudeNet (NudeDetector) to classify an image for nudity.
    Returns:
        - status: success or error
        - label: one of ['safe', 'unsafe']
        - unsafe_score: float (0 to 1) - Represents the highest confidence of any nudity detected.
        - explanation: reason
    """
    if not os.path.exists(image_path):
        return {"status": "error", "message": f"Image not found at: {image_path}"}

    try:
        # NudeDetector.detect returns a list of dictionaries,
        # where each dictionary represents a detected object.
        detections = detector.detect(image_path)

        unsafe_score = 0.0
        is_unsafe = False
        explanation_parts = []

        if not detections:
            # No nudity detected by NudeNet
            label = 'safe'
            explanation = "NudeNet did not detect any nudity."
        else:
            # Iterate through detections to find the highest 'unsafe' score
            # and build an explanation.
            for detection in detections:
                score = detection.get('score', 0.0)
                label_detected = detection.get('class', 'unknown')

                # We consider any detection of a nudity-related class as potentially 'unsafe'.
                # The score from NudeDetector represents the confidence of that specific detection.
                if score > unsafe_score:
                    unsafe_score = score

                is_unsafe = True # If any detection exists, it's considered unsafe for this logic
                explanation_parts.append(f"{label_detected} (score: {score:.2f})")

            label = 'unsafe'
            # Combine explanations for multiple detections
            explanation = f"NudeNet detected: {'; '.join(explanation_parts)}. Highest confidence: {unsafe_score:.2f}"


        # You might want to adjust the threshold for 'unsafe' based on your requirements.
        # For NudeDetector, if there are *any* detections, it implies 'unsafe'.
        # The 'unsafe_score' here represents the highest confidence among all detections.
        # If you need a single binary score, you might take the max score of all nudity classes.

        return {
            "status": "success",
            "label": label,
            "unsafe_score": round(unsafe_score, 2),
            "explanation": explanation
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}