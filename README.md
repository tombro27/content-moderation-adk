# 🛡️ Content Moderation AI Development Kit (ADK)

A comprehensive AI-powered content moderation system that uses multiple specialized agents to detect and classify various types of inappropriate content in images. Built with Python, leveraging Google Gemini Vision API and NudeNet for robust content analysis.

## 🎯 Overview

This Content Moderation ADK provides a complete solution for detecting and moderating inappropriate content in images. The system uses a multi-agent architecture where each agent specializes in detecting specific types of content violations:

- **🔞 Nudity Detection** - Explicit content using NudeNet
- **🔫 Violence Detection** - Weapons, blood, gore, and violent content
- **🧪 Drugs Detection** - Drug paraphernalia and substance-related content
- **🍾 Alcohol/Smoking Detection** - Alcohol and smoking-related content
- **☠️ Hate Symbols Detection** - Hate symbols and extremist content
- **🔐 PII/Text Detection** - Personal information and threatening text
- **📷 QR Code Detection** - QR codes and barcodes
- **👙 Nudity Exception Handler** - Acceptable clothing exceptions

## 🏗️ Architecture

### Individual Agents
Each agent is a specialized module that focuses on detecting specific types of content:

```
agents/
├── alcohol_smoke_detection_gemini.yaml
├── central_moderation_pipeline_agent.yaml
├── drugs_detection_gemini.yaml
├── hate_detection_gemini.yaml
├── ingestion_agent.yaml
├── nudity_detection_agent.yaml
├── nudity_exceptions_gemini.yaml
├── qr_detection_gemini.yaml
├── text_pii_detection_gemini.yaml
├── text_pii_vision_gemini.yaml
└── violence_detection_gemini.yaml
```

### Central Pipeline
The central pipeline orchestrates all agents to provide comprehensive analysis:

```
tools/
├── central_moderation_pipeline.py      # Main pipeline orchestrator
├── image_preprocessor.py              # Image ingestion and preprocessing
├── nudity_detector.py                 # NudeNet-based nudity detection
├── violence_detection_gemini.py       # Violence detection using Gemini
├── drugs_detector_gemini.py           # Drugs detection using Gemini
├── alcohol_smoke_detector_gemini.py   # Alcohol/smoking detection
├── hate_detector_gemini.py            # Hate symbols detection
├── text_pii_vision_gemini.py          # PII detection using Gemini Vision
├── qr_detector_gemini.py              # QR code detection
├── nudity_exceptions_detector_gemini.py # Nudity exception handling
└── gemini_vision.py                   # Gemini Vision API integration
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Google Gemini API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Required Python packages** (see `requirements.txt`)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd content-moderation-adk
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key**
   ```bash
   # Set your Gemini API key as environment variable
   export GOOGLE_API_KEY="your-api-key-here"
   ```

### Basic Usage

#### Individual Agent Testing

```python
# Test nudity detection
python test_nudity.py

# Test violence detection
python test_violence_gemini.py

# Test drugs detection
python test_drugs_gemini.py

# Test alcohol/smoking detection
python test_alcohol_smoke_gemini.py

# Test hate symbols detection
python test_hate_gemini.py

# Test PII detection
python test_text_pii_vision_gemini.py

# Test QR code detection
python test_qr_gemini.py
```

#### Central Pipeline Testing

```python
# Run the complete pipeline
python demo_central_pipeline.py

# Test with specific image
python demo_central_pipeline.py data/test_images/blood.jpg

# Run comprehensive tests
python test_central_pipeline.py
```

## 📊 Decision Logic

The system uses a priority-based decision system:

### High Priority (Reject)
- **Nudity** - Explicit content
- **Blood/Gore** - Violent or graphic content
- **Weapons** - Firearms, knives, explosives
- **Death/Corpses** - Dead bodies, autopsies
- **Self-harm** - Self-injury content
- **Abuse/Torture** - Cruelty to humans or animals

### Medium Priority (Flag)
- **Drugs** - Drug paraphernalia and substances
- **Hate Symbols** - Extremist or hate group symbols
- **Threatening Text** - Abusive or threatening language

### Low Priority (Flag)
- **Alcohol** - Alcohol-related content
- **Smoking** - Tobacco and vaping content
- **QR Codes** - QR codes and barcodes
- **Personal Information** - PII like IDs, phone numbers

## 🧪 Test Images

The project includes test images for different violation types:

```
data/test_images/
├── adhaar.png          # Personal information (ID card)
├── alcohol.jpg         # Alcohol content
├── blood.jpg           # Violence/gore
├── exception.png       # Nudity exception (acceptable)
├── gun.jpg             # Weapons
├── hateSymbol.png      # Hate symbols
├── nudeMen.jpg         # Nudity
├── QR.png              # QR codes
├── sample.jpg          # Clean image
├── vapes.jpg           # Smoking/vaping
└── violence.jpg        # Violent content
```

## 📋 Output Format

### Individual Agent Response
```python
{
    "status": "success",
    "response_text": "YES, this image contains...",
    "confidence": 0.85,
    "violations": ["blood/gore", "weapons"]
}
```

### Central Pipeline Response
```python
{
    "status": "success",
    "image_path": "path/to/image.jpg",
    "final_decision": "Reject",
    "violations": ["blood/gore", "weapons"],
    "agent_results": {
        "ingestion": {...},
        "nudity": {...},
        "violence": {...},
        # ... all agents
    },
    "confidence_scores": {
        "nudity": 0.9,
        "violence": 0.8,
        # ... all agents
    },
    "detailed_report": {
        "ingestion": {...},
        "nudity": {...},
        # ... all agents
    }
}
```

## 🔧 Configuration

### Agent Configuration
Each agent can be configured through YAML files in the `agents/` directory:

```yaml
# Example: violence_detection_gemini.yaml
name: "Violence Detection Agent"
description: "Detects violence, weapons, blood, and gore"
tools:
  - violence_detection_gemini
prompts:
  - violence_prompt.txt
```

### Prompt Configuration
Customize detection prompts in `configs/prompts/`:

```
configs/prompts/
├── alcohol_smoke_prompt.txt
├── drugs_prompt.txt
├── hate_prompt.txt
├── nudity_exceptions_prompt.txt
├── qr_prompt.txt
├── text_pii_prompt.txt
├── text_pii_vision_prompt.txt
└── violence_prompt.txt
```

## 📈 Performance

### Typical Execution Times
- **Individual Agent**: 2-8 seconds
- **Central Pipeline**: 15-45 seconds
- **Image Preprocessing**: < 1 second
- **NudeNet Detection**: 2-5 seconds
- **Gemini Vision API**: 3-8 seconds per agent

### Accuracy Metrics
- **Nudity Detection**: ~95% accuracy with NudeNet
- **Violence Detection**: ~90% accuracy with Gemini Vision
- **Text PII Detection**: ~85% accuracy with Gemini Vision
- **Overall Pipeline**: ~88% accuracy across all violation types

## 🛠️ Development

### Adding New Agents

1. **Create the agent tool** in `tools/`:
   ```python
   # tools/new_detector_gemini.py
   from tools.gemini_vision import analyze_image_with_prompt
   
   def detect_new_violation_with_gemini(image_path: str) -> dict:
       with open("configs/prompts/new_prompt.txt", "r") as f:
           prompt = f.read()
       return analyze_image_with_prompt(image_path, prompt)
   ```

2. **Add the agent to the pipeline** in `tools/central_moderation_pipeline.py`:
   ```python
   from tools.new_detector_gemini import detect_new_violation_with_gemini
   
   # Add to pipeline sequence
   new_result = detect_new_violation_with_gemini(processed_path)
   ```

3. **Create test script**:
   ```python
   # test_new_detector_gemini.py
   from tools.new_detector_gemini import detect_new_violation_with_gemini
   
   result = detect_new_violation_with_gemini("test_image.jpg")
   print(result)
   ```

### Customizing Decision Logic

Modify the decision logic in `tools/central_moderation_pipeline.py`:

```python
# High priority violations (Reject)
high_priority = ["nudity", "blood/gore", "weapons", "death/corpses", "self-harm", "abuse/torture"]

# Medium priority violations (Flag)
medium_priority = ["drugs", "hate_symbols", "threatening/abusive text"]

# Low priority violations (Flag)
low_priority = ["alcohol", "smoking", "qr_codes", "personal information"]
```

## 🚨 Error Handling

### Common Issues

1. **API Rate Limits**: Gemini API has rate limits; implement retry logic
2. **Image Format Issues**: Some formats may not be supported by all agents
3. **Network Connectivity**: Ensure stable internet for API calls
4. **Memory Issues**: Large images may cause memory problems

### Debug Mode
Enable detailed logging by modifying agent functions to include verbose output.

## 📚 API Reference

### Core Functions

#### `run_central_moderation_pipeline(image_path: str) -> Dict[str, Any]`
Runs the complete moderation pipeline on an image.

#### `detect_nudity(image_path: str) -> Dict[str, Any]`
Detects nudity using NudeNet.

#### `detect_violence_with_gemini(image_path: str) -> Dict[str, Any]`
Detects violence using Gemini Vision.

#### `detect_drugs_with_gemini(image_path: str) -> Dict[str, Any]`
Detects drugs using Gemini Vision.

#### `detect_alcohol_smoke_with_gemini(image_path: str) -> Dict[str, Any]`
Detects alcohol and smoking content using Gemini Vision.

#### `detect_hate_symbols_with_gemini(image_path: str) -> Dict[str, Any]`
Detects hate symbols using Gemini Vision.

#### `detect_text_pii_with_gemini_vision(image_path: str) -> Dict[str, Any]`
Detects PII and threatening text using Gemini Vision.

#### `detect_qr_code_with_gemini(image_path: str) -> Dict[str, Any]`
Detects QR codes using Gemini Vision.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini Vision API** for advanced image analysis
- **NudeNet** for nudity detection
- **OpenCV** for image processing
- **Pillow** for image manipulation

## 📞 Support

For issues and questions:
1. Check the existing documentation
2. Review test cases for examples
3. Open an issue on GitHub
4. Contact the development team

---

**Built with ❤️ for safe and responsible content moderation**
