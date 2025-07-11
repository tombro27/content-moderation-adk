from PIL import Image
import os

def image_preprocessor(image_path: str) -> dict:
    """
    Processes an input image for moderation.
    - Validates extension.
    - Resizes to max 1024x1024 if too large.
    - Returns image metadata and new path.

    Returns:
        {
            "status": "success",
            "original_size": (W, H),
            "new_size": (W, H),
            "format": "JPEG/PNG",
            "output_path": "path/to/output/image"
        }
    """

    allowed_exts = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in allowed_exts:
        return {"status": "error", "message": f"Unsupported file type: {ext}"}

    try:
        img = Image.open(image_path)
        original_size = img.size
        img_format = img.format

        # Resize if image is too large
        MAX_SIZE = (1024, 1024)
        img.thumbnail(MAX_SIZE)

        # Save normalized image
        output_path = image_path.replace("/data/", "/output/")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)

        return {
            "status": "success",
            "original_size": original_size,
            "new_size": img.size,
            "format": img_format,
            "output_path": output_path
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
