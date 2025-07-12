from tools.gemini_vision import analyze_image_with_prompt

def detect_violence_with_gemini(image_path: str) -> dict:
    prompt = """
You are an expert visual content moderation agent.

Analyze the given image and answer whether it contains any of the following types of visual violations related to violence or harm:

1. Blood, wounds, gore, or severe injuries (human or animal)
2. Weapons such as guns, knives, grenades, or explosives
3. Corpses, dead bodies, hanging, or autopsy scenes
4. Self-harm, including cutting, burning, suicidal actions
5. Physical abuse or torture of people or animals
6. Animal cruelty or inhumane conditions (tight cages, beatings, mutilation)

Your response must be structured as follows:

- **Is the image violating any of the above?** YES or NO  
- **If YES, specify the type(s) of violation**  
- **Briefly explain how you identified the violation(s)**

Be accurate and objective. If uncertain, say "Not clearly identifiable."
"""
    return analyze_image_with_prompt(image_path, prompt)
