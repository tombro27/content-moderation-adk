import torch
from torchvision import models, transforms
from PIL import Image
import os

# Load model once
model = models.resnet50(pretrained=True)
model.eval()

# Load ImageNet class labels
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABELS_FILE = "imagenet_classes.txt"

if not os.path.exists(LABELS_FILE):
    import urllib.request
    urllib.request.urlretrieve(LABELS_URL, LABELS_FILE)

with open(LABELS_FILE) as f:
    idx_to_labels = [line.strip() for line in f.readlines()]

# Tags related to violence
VIOLENT_KEYWORDS = [
    'blood', 'gore', 'wound', 'gun', 'rifle', 'weapon', 'revolver', 'missile',
    'knife', 'machete', 'grenade', 'corpse', 'bullet', 'projectile', 'armor', 'assault'
]

# Preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def detect_violence(image_path: str) -> dict:
    if not os.path.exists(image_path):
        return {"status": "error", "message": "Image not found"}

    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = preprocess(image).unsqueeze(0)  # Add batch dim

        with torch.no_grad():
            outputs = model(input_tensor)

        probs = torch.nn.functional.softmax(outputs[0], dim=0)
        top5 = torch.topk(probs, 5)

        flagged = []
        for i in range(top5.indices.size(0)):
            label = idx_to_labels[top5.indices[i]]
            prob = round(probs[top5.indices[i]].item(), 2)
            for keyword in VIOLENT_KEYWORDS:
                if keyword in label.lower():
                    flagged.append({"label": label, "score": prob})
                    break

        if flagged:
            explanation = f"Detected violence-related content: {', '.join([f['label'] for f in flagged])}"
            return {
                "status": "success",
                "violence": True,
                "violations": flagged,
                "explanation": explanation
            }
        else:
            return {
                "status": "success",
                "violence": False,
                "violations": [],
                "explanation": "No violence-related content detected."
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}
