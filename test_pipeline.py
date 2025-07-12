from tools.moderation_pipeline import run_moderation_pipeline

image_path = "data/test_images/nudeMen.jpg"

result = run_moderation_pipeline(image_path)

print("🛡️ Moderation Report")
print("-" * 60)
print(f"Image Path: {result.get('image_path')}")
print(f"Final Decision: {result.get('final_decision')}")
print(f"Violations: {result.get('violations', [])}\n")

print("🔍 Agent-Level Results")
print("-" * 60)
for key, value in result["results"].items():
    print(f"\n🧩 {key.upper()}")
    if isinstance(value, dict):
        for k, v in value.items():
            print(f"  {k}: {v}")
    else:
        print(f"  {value}")
