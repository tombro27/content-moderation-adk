# 🛡️ Central Moderation Pipeline

A comprehensive content moderation pipeline that runs all individual agents sequentially on each image to provide detailed analysis and decision-making.

## 🎯 Overview

The Central Moderation Pipeline orchestrates all individual content moderation agents to provide a complete analysis of images with:

- **Sequential Agent Execution**: Runs all agents in order
- **Confidence Scoring**: Extracts confidence levels from agent responses
- **Violation Classification**: Categorizes detected violations by type
- **Decision Logic**: Provides Accept/Reject/Flag decisions based on violation priority
- **Detailed Reporting**: Comprehensive JSON reports with all agent results
- **Performance Metrics**: Execution timing and agent performance analysis

## 🧩 Agent Pipeline

The pipeline runs the following agents in sequence:

1. **🧹 Ingestion Agent** → Resize, format, and normalize images
2. **🔞 Nudity Detection** → Detect explicit content using NudeNet
3. **👙 Nudity Exception Handler** → Check for acceptable clothing exceptions
4. **🔫 Violence/Gore Detection** → Detect violence, weapons, blood, gore
5. **🧪 Drugs Detection** → Detect drug-related content and paraphernalia
6. **🍾 Alcohol/Smoking Detection** → Detect alcohol and smoking content
7. **☠️ Hate Symbols Detection** → Detect hate symbols and extremist content
8. **🔐 PII/Text Detection** → Extract and analyze text for PII and abuse
9. **📷 QR Code Detection** → Detect QR codes and barcodes

## 📊 Decision Logic

The pipeline uses a priority-based decision system:

### High Priority (Reject)
- Nudity
- Blood/Gore
- Weapons
- Death/Corpses
- Self-harm
- Abuse/Torture

### Medium Priority (Flag)
- Drugs
- Hate Symbols
- Threatening/Abusive Text

### Low Priority (Flag)
- Alcohol
- Smoking
- QR Codes
- Personal Information

## 🚀 Usage

### Basic Usage

```python
from tools.central_moderation_pipeline import run_central_moderation_pipeline

# Run the complete pipeline
report = run_central_moderation_pipeline("path/to/image.jpg")

# Check the decision
print(f"Decision: {report['final_decision']}")
print(f"Violations: {report['violations']}")
```

### Demo Script

```bash
# Test with a specific image
python demo_central_pipeline.py data/test_images/blood.jpg

# Test with default image
python demo_central_pipeline.py
```

### Comprehensive Testing

```bash
# Run all tests
python test_central_pipeline.py
```

## 📋 Output Format

The pipeline returns a comprehensive dictionary with:

```python
{
    "status": "success",                    # Pipeline execution status
    "image_path": "path/to/image.jpg",     # Input image path
    "final_decision": "Reject",            # Accept/Reject/Flag
    "violations": ["blood/gore", "nudity"], # Detected violations
    "agent_results": {                     # Raw results from each agent
        "ingestion": {...},
        "nudity": {...},
        "violence": {...},
        # ... all agents
    },
    "confidence_scores": {                 # Confidence scores for each agent
        "nudity": 0.9,
        "violence": 0.8,
        # ... all agents
    },
    "detailed_report": {                   # Detailed analysis
        "ingestion": {...},
        "nudity": {...},
        # ... all agents
    }
}
```

## 📄 JSON Export

The pipeline can export detailed reports as JSON:

```python
from tools.central_moderation_pipeline import export_json_report

# Export to file
export_json_report(report, "moderation_report.json")

# Get JSON string
json_string = export_json_report(report)
```

## 🎨 Formatted Reports

Print beautiful formatted reports:

```python
from tools.central_moderation_pipeline import print_moderation_report

# Print comprehensive report
print_moderation_report(report)
```

## 📈 Features

### Confidence Scoring
- Extracts confidence levels from Gemini responses
- Uses keyword analysis for confidence estimation
- Provides confidence scores for all agents

### Violation Classification
- Categorizes violations by type (blood/gore, weapons, etc.)
- Removes duplicate violations
- Provides detailed violation descriptions

### Performance Monitoring
- Tracks execution time for each agent
- Provides average processing time
- Monitors agent success/failure rates

### Error Handling
- Graceful handling of agent failures
- Continues pipeline execution on partial failures
- Provides detailed error messages

## 🧪 Testing

### Test Images
The pipeline includes test images for different violation types:

- `blood.jpg` - Violence/Gore
- `nudeMen.jpg` - Nudity
- `vapes.jpg` - Smoking
- `alcohol.jpg` - Alcohol
- `gun.jpg` - Weapons
- `QR.png` - QR Codes
- `adhaar.png` - PII
- `hateSymbol.png` - Hate Symbols
- `sample.jpg` - Clean image

### Test Scripts

1. **Single Image Test**: `test_single_image()`
2. **Multiple Images Test**: `test_central_pipeline()`
3. **Performance Test**: `test_pipeline_performance()`

## 🔧 Configuration

### Agent Configuration
Each agent can be configured through their respective YAML files in the `agents/` directory.

### Decision Thresholds
Modify the decision logic in `tools/central_moderation_pipeline.py`:

```python
# High priority violations (Reject)
high_priority = ["nudity", "blood/gore", "weapons", "death/corpses", "self-harm", "abuse/torture"]

# Medium priority violations (Flag)
medium_priority = ["drugs", "hate_symbols", "threatening/abusive text"]

# Low priority violations (Flag)
low_priority = ["alcohol", "smoking", "qr_codes", "personal information"]
```

## 📊 Performance

Typical execution times:
- **Total Pipeline**: 10-30 seconds
- **Per Agent**: 1-5 seconds
- **Ingestion**: < 1 second
- **Nudity Detection**: 2-5 seconds
- **Gemini Agents**: 3-8 seconds each

## 🛠️ Troubleshooting

### Common Issues

1. **PII Detection Errors**: May occur with corrupted images or OCR failures
2. **Gemini API Limits**: Rate limiting may affect response times
3. **Image Format Issues**: Some formats may not be supported by all agents

### Debug Mode
Enable detailed logging by modifying the pipeline to print more verbose output.

## 📚 API Reference

### Main Functions

#### `run_central_moderation_pipeline(image_path: str) -> Dict[str, Any]`
Runs the complete moderation pipeline on an image.

**Parameters:**
- `image_path`: Path to the image file

**Returns:**
- Comprehensive moderation report dictionary

#### `print_moderation_report(report: Dict[str, Any]) -> None`
Prints a formatted moderation report.

#### `export_json_report(report: Dict[str, Any], output_path: str = None) -> str`
Exports the report as JSON.

**Parameters:**
- `report`: Moderation report dictionary
- `output_path`: Optional file path for export

**Returns:**
- JSON string representation of the report

## 🤝 Contributing

To add new agents to the pipeline:

1. Create the agent YAML file in `agents/`
2. Implement the agent tool in `tools/`
3. Add the agent to the pipeline in `tools/central_moderation_pipeline.py`
4. Update the decision logic if needed
5. Add test cases

## 📄 License

This project is part of the Content Moderation ADK (Agent Development Kit). 