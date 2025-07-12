import json
import re
from typing import Dict, List, Any
from tools.image_preprocessor import image_preprocessor
from tools.nudity_detector import detect_nudity
from tools.nudity_exceptions_detector_gemini import detect_nudity_exceptions_with_gemini
from tools.violence_detection_gemini import detect_violence_with_gemini
from tools.drugs_detector_gemini import detect_drugs_with_gemini
from tools.alcohol_smoke_detector_gemini import detect_alcohol_smoke_with_gemini
from tools.hate_detector_gemini import detect_hate_symbols_with_gemini
from tools.text_pii_vision_gemini import detect_text_pii_with_gemini_vision
from tools.qr_detector_gemini import detect_qr_code_with_gemini

def extract_confidence_from_response(response_text: str) -> float:
    """Enhanced confidence extraction with more sophisticated keyword analysis."""
    if not response_text:
        return 0.0
    
    response_upper = response_text.upper()
    
    # More comprehensive confidence indicators
    high_confidence = ["CLEARLY", "DEFINITELY", "CERTAINLY", "OBVIOUSLY", "UNDOUBTEDLY", "WITHOUT DOUBT", "CONFIRMED", "IDENTIFIED"]
    medium_high = ["YES", "VIOLATION", "DETECTED", "FOUND", "PRESENT", "SHOWS", "CONTAINS", "DISPLAYS"]
    medium = ["LIKELY", "PROBABLY", "APPEARS", "SEEMS", "INDICATES", "SUGGESTS", "MIGHT BE"]
    medium_low = ["UNCERTAIN", "NOT CLEARLY", "MAYBE", "POSSIBLY", "MIGHT", "COULD BE", "UNSURE"]
    low_confidence = ["NO", "NOT DETECTED", "CLEAN", "SAFE", "NONE FOUND", "ABSENT", "NOT PRESENT"]
    
    # Count confidence indicators
    high_count = sum(1 for phrase in high_confidence if phrase in response_upper)
    medium_high_count = sum(1 for phrase in medium_high if phrase in response_upper)
    medium_count = sum(1 for phrase in medium if phrase in response_upper)
    medium_low_count = sum(1 for phrase in medium_low if phrase in response_upper)
    low_count = sum(1 for phrase in low_confidence if phrase in response_upper)
    
    # Weighted scoring with priority
    if high_count > 0:
        return 0.9
    elif medium_high_count > 0:
        return 0.8
    elif medium_count > 0:
        return 0.6
    elif medium_low_count > 0:
        return 0.4
    elif low_count > 0:
        return 0.1
    
    return 0.5  # Default confidence

def calculate_nudity_confidence(nudity_result: dict) -> float:
    """Use actual NudeNet confidence scores when available."""
    if nudity_result.get("label") == "unsafe":
        # Try to extract actual confidence from NudeNet violations
        violations = nudity_result.get("violations", [])
        if violations:
            # Use the highest confidence score from detected violations
            max_confidence = max(violation.get("score", 0.5) for violation in violations)
            return max_confidence
        return 0.9  # Fallback for unsafe without detailed scores
    else:
        return 0.1  # Safe content has low confidence for violations

def parse_violation_type(response_text: str) -> List[str]:
    """Parse violation types from Gemini response."""
    violations = []
    if not response_text:
        return violations
    
    response_upper = response_text.upper()
    
    # Violence types
    if any(word in response_upper for word in ["BLOOD", "WOUND", "GORE", "INJURY"]):
        violations.append("blood/gore")
    if any(word in response_upper for word in ["WEAPON", "GUN", "KNIFE", "EXPLOSIVE"]):
        violations.append("weapons")
    if any(word in response_upper for word in ["CORPSE", "DEAD", "HANGING", "AUTOPSY"]):
        violations.append("death/corpses")
    if any(word in response_upper for word in ["SELF-HARM", "CUTTING", "BURNING", "SUICIDAL"]):
        violations.append("self-harm")
    if any(word in response_upper for word in ["ABUSE", "TORTURE", "CRUELTY"]):
        violations.append("abuse/torture")
    
    # Drugs types
    if any(word in response_upper for word in ["DRUG", "PARAPHERNALIA", "SYRINGE", "PIPE"]):
        violations.append("drugs/paraphernalia")
    
    # Alcohol/Smoking types
    if any(word in response_upper for word in ["ALCOHOL", "BEER", "WINE", "LIQUOR"]):
        violations.append("alcohol")
    if any(word in response_upper for word in ["SMOKING", "CIGARETTE", "TOBACCO", "VAPE"]):
        violations.append("smoking")
    
    # Hate types
    if any(word in response_upper for word in ["HATE", "SYMBOL", "EXTREMIST", "RACIST"]):
        violations.append("hate symbols")
    
    # PII types
    if any(word in response_upper for word in ["PII", "PERSONAL", "IDENTIFIABLE", "PRIVATE"]):
        violations.append("personal information")
    if any(word in response_upper for word in ["THREAT", "ABUSIVE", "HARASSMENT"]):
        violations.append("threatening/abusive text")
    
    # QR types
    if any(word in response_upper for word in ["QR", "CODE", "BARCODE"]):
        violations.append("qr codes")
    
    return violations

def run_central_moderation_pipeline(image_path: str) -> Dict[str, Any]:
    """
    Run comprehensive moderation pipeline on an image.
    
    Returns:
        Dict containing:
        - status: success/error
        - final_decision: Accept/Reject/Flag
        - violations: List of detected violations
        - agent_results: Raw results from each agent
        - confidence_scores: Confidence scores for each detection
        - detailed_report: Comprehensive analysis
    """
    
    pipeline_report = {
        "status": "success",
        "image_path": image_path,
        "final_decision": "Accept",
        "violations": [],
        "agent_results": {},
        "confidence_scores": {},
        "detailed_report": {
            "ingestion": {},
            "nudity": {},
            "nudity_exceptions": {},
            "violence": {},
            "drugs": {},
            "alcohol_smoking": {},
            "hate": {},
            "pii_text": {},
            "qr_code": {}
        }
    }
    
    try:
        # 🧹 Step 1: Ingestion Agent
        print("🔄 Running Ingestion Agent...")
        ingestion_result = image_preprocessor(image_path)
        pipeline_report["agent_results"]["ingestion"] = ingestion_result
        pipeline_report["detailed_report"]["ingestion"] = ingestion_result
        
        if ingestion_result.get("status") != "success":
            pipeline_report["final_decision"] = "Reject"
            pipeline_report["violations"].append("image_processing_error")
            return pipeline_report
        
        processed_path = ingestion_result["output_path"]
        
        # 🔞 Step 2: Nudity Detection (NudeNet)
        print("🔞 Running Nudity Detection...")
        nudity_result = detect_nudity(processed_path)
        pipeline_report["agent_results"]["nudity"] = nudity_result
        pipeline_report["detailed_report"]["nudity"] = nudity_result
        
        nudity_confidence = calculate_nudity_confidence(nudity_result)
        pipeline_report["confidence_scores"]["nudity"] = nudity_confidence
        
        if nudity_result.get("label") == "unsafe":
            pipeline_report["violations"].append("nudity")
        
        # 👙 Step 3: Nudity Exception Handler (Gemini)
        print("👙 Running Nudity Exceptions Detection...")
        nudity_exception_result = detect_nudity_exceptions_with_gemini(processed_path)
        pipeline_report["agent_results"]["nudity_exceptions"] = nudity_exception_result
        pipeline_report["detailed_report"]["nudity_exceptions"] = nudity_exception_result
        
        nudity_exception_confidence = extract_confidence_from_response(
            nudity_exception_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["nudity_exceptions"] = nudity_exception_confidence
        
        # 🔫 Step 4: Violence/Gore Detection (Gemini)
        print("🔫 Running Violence Detection...")
        violence_result = detect_violence_with_gemini(processed_path)
        pipeline_report["agent_results"]["violence"] = violence_result
        pipeline_report["detailed_report"]["violence"] = violence_result
        
        violence_confidence = extract_confidence_from_response(
            violence_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["violence"] = violence_confidence
        
        if "YES" in (violence_result.get("response_text") or "").upper():
            violence_types = parse_violation_type(violence_result.get("response_text", ""))
            pipeline_report["violations"].extend(violence_types)
        
        # 🧪 Step 5: Drugs Detection (Gemini)
        print("🧪 Running Drugs Detection...")
        drugs_result = detect_drugs_with_gemini(processed_path)
        pipeline_report["agent_results"]["drugs"] = drugs_result
        pipeline_report["detailed_report"]["drugs"] = drugs_result
        
        drugs_confidence = extract_confidence_from_response(
            drugs_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["drugs"] = drugs_confidence
        
        if "YES" in (drugs_result.get("response_text") or "").upper():
            pipeline_report["violations"].append("drugs")
        
        # 🍾 Step 6: Alcohol/Smoking Detection (Gemini)
        print("🍾 Running Alcohol/Smoking Detection...")
        alcohol_result = detect_alcohol_smoke_with_gemini(processed_path)
        pipeline_report["agent_results"]["alcohol_smoking"] = alcohol_result
        pipeline_report["detailed_report"]["alcohol_smoking"] = alcohol_result
        
        alcohol_confidence = extract_confidence_from_response(
            alcohol_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["alcohol_smoking"] = alcohol_confidence
        
        if "YES" in (alcohol_result.get("response_text") or "").upper():
            alcohol_types = parse_violation_type(alcohol_result.get("response_text", ""))
            pipeline_report["violations"].extend(alcohol_types)
        
        # ☠️ Step 7: Hate Symbols Detection (Gemini)
        print(" ☠️ Running Hate Symbols Detection...")
        hate_result = detect_hate_symbols_with_gemini(processed_path)
        pipeline_report["agent_results"]["hate"] = hate_result
        pipeline_report["detailed_report"]["hate"] = hate_result
        
        hate_confidence = extract_confidence_from_response(
            hate_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["hate"] = hate_confidence
        
        if "YES" in (hate_result.get("response_text") or "").upper():
            pipeline_report["violations"].append("hate_symbols")
        
        # 🔐 Step 8: PII/Text Detection (Gemini Vision)
        print("🔐 Running PII/Text Detection...")
        pii_result = detect_text_pii_with_gemini_vision(processed_path)
        pipeline_report["agent_results"]["pii_text"] = pii_result
        pipeline_report["detailed_report"]["pii_text"] = pii_result
        
        pii_confidence = extract_confidence_from_response(
            pii_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["pii_text"] = pii_confidence
        
        if "YES" in (pii_result.get("response_text") or "").upper():
            pii_types = parse_violation_type(pii_result.get("response_text", ""))
            pipeline_report["violations"].extend(pii_types)
        
        # 📷 Step 9: QR Code Detection (Gemini)
        print("📷 Running QR Code Detection...")
        qr_result = detect_qr_code_with_gemini(processed_path)
        pipeline_report["agent_results"]["qr_code"] = qr_result
        pipeline_report["detailed_report"]["qr_code"] = qr_result
        
        qr_confidence = extract_confidence_from_response(
            qr_result.get("response_text", "")
        )
        pipeline_report["confidence_scores"]["qr_code"] = qr_confidence
        
        if "YES" in (qr_result.get("response_text") or "").upper():
            pipeline_report["violations"].append("qr_codes")
        
        # 🎯 Final Decision Logic
        pipeline_report["violations"] = list(set(pipeline_report["violations"]))  # Remove duplicates
        
        if pipeline_report["violations"]:
            # Check for high-priority violations
            high_priority = ["nudity", "blood/gore", "weapons", "death/corpses", "self-harm", "abuse/torture"]
            medium_priority = ["drugs", "hate_symbols", "threatening/abusive text"]
            low_priority = ["alcohol", "smoking", "qr_codes", "personal information"]
            
            has_high_priority = any(violation in high_priority for violation in pipeline_report["violations"])
            has_medium_priority = any(violation in medium_priority for violation in pipeline_report["violations"])
            
            if has_high_priority:
                pipeline_report["final_decision"] = "Reject"
            elif has_medium_priority:
                pipeline_report["final_decision"] = "Flag"
            else:
                pipeline_report["final_decision"] = "Flag"
        
        print("✅ Pipeline completed successfully!")
        
    except Exception as e:
        pipeline_report["status"] = "error"
        pipeline_report["final_decision"] = "Reject"
        pipeline_report["violations"].append("pipeline_error")
        pipeline_report["error_message"] = str(e)
        print(f"❌ Pipeline error: {e}")
    
    return pipeline_report

def get_confidence_table_reference() -> str:
    """Get the confidence table reference for output."""
    return """
🎯 CONFIDENCE SCORE REFERENCE TABLE
====================================

| Score Range | Level | Meaning | Keywords/Indicators |
|-------------|-------|---------|-------------------|
| **0.9** | **Very High** | Agent is extremely confident in detection | "CLEARLY", "DEFINITELY", "CERTAINLY", "OBVIOUSLY", "UNDOUBTEDLY", "WITHOUT DOUBT", "CONFIRMED", "IDENTIFIED" |
| **0.8** | **High** | Agent detected violation with high certainty | "YES", "VIOLATION", "DETECTED", "FOUND", "PRESENT", "SHOWS", "CONTAINS", "DISPLAYS" |
| **0.6** | **Medium-High** | Agent thinks violation is likely | "LIKELY", "PROBABLY", "APPEARS", "SEEMS", "INDICATES", "SUGGESTS", "MIGHT BE" |
| **0.5** | **Medium** | Agent is uncertain or neutral | No specific confidence indicators found |
| **0.4** | **Medium-Low** | Agent is uncertain about detection | "UNCERTAIN", "NOT CLEARLY", "MAYBE", "POSSIBLY", "MIGHT", "COULD BE", "UNSURE" |
| **0.1** | **Low** | Agent found no violations | "NO", "NOT DETECTED", "CLEAN", "SAFE", "NONE FOUND", "ABSENT", "NOT PRESENT" |
| **0.0** | **Error** | Agent failed to process | Agent error or no response |

📊 CONFIDENCE LEVELS EXPLAINED:
• **0.9**: Very High - Strong evidence for decision-making
• **0.8**: High - Reliable detection, can be used for automated decisions  
• **0.6**: Medium-High - Good evidence, may need review
• **0.5**: Medium - Neutral evidence, requires human review
• **0.4**: Medium-Low - Weak evidence, likely false positive
• **0.1**: Low - Strong evidence of safety
• **0.0**: Error - No evidence available, manual review required
"""

def print_moderation_report(report: Dict[str, Any]) -> None:
    """Print a formatted moderation report."""
    
    print("\n" + "="*80)
    print("🛡️ CENTRAL MODERATION PIPELINE REPORT")
    print("="*80)
    
    # Basic Info
    print(f"📁 Image Path: {report.get('image_path')}")
    print(f"📊 Status: {report.get('status')}")
    
    # Final Decision
    decision = report.get('final_decision', 'Unknown')
    if decision == "Accept":
        print(f"✅ Final Decision: {decision}")
    elif decision == "Reject":
        print(f"❌ Final Decision: {decision}")
    else:
        print(f"⚠️ Final Decision: {decision}")
    
    # Violations
    violations = report.get('violations', [])
    if violations:
        print(f"🚨 Detected Violations: {', '.join(violations)}")
    else:
        print("✅ No violations detected")
    
    print("\n" + "-"*80)
    print("🔍 DETAILED AGENT RESULTS")
    print("-"*80)
    
    # Agent Results
    agent_results = report.get('agent_results', {})
    confidence_scores = report.get('confidence_scores', {})
    
    for agent_name, result in agent_results.items():
        print(f"\n🧩 {agent_name.upper()}")
        print(f"   Status: {result.get('status', 'N/A')}")
        
        # Show confidence if available
        if agent_name in confidence_scores:
            confidence = confidence_scores[agent_name]
            print(f"   Confidence: {confidence:.2f}")
        
        # Show key results
        if agent_name == "nudity":
            label = result.get('label', 'N/A')
            print(f"   Label: {label}")
            if result.get('explanation'):
                print(f"   Explanation: {result.get('explanation')}")
        
        elif agent_name == "ingestion":
            print(f"   Original Size: {result.get('original_size', 'N/A')}")
            print(f"   New Size: {result.get('new_size', 'N/A')}")
            print(f"   Format: {result.get('format', 'N/A')}")
        
        else:
            # For Gemini-based agents
            response = result.get('response_text', 'N/A')
            if len(response) > 100:
                response = response[:100] + "..."
            print(f"   Response: {response}")
    
    print("\n" + "-"*80)
    print("📈 CONFIDENCE SCORES")
    print("-"*80)
    
    for agent, confidence in confidence_scores.items():
        print(f"   {agent}: {confidence:.2f}")
    
    print("\n" + "="*80)

def export_json_report(report: Dict[str, Any], output_path: str | None = None) -> str:
    """Export the moderation report as JSON."""
    # Add confidence table reference to the report
    report_with_reference = report.copy()
    report_with_reference["confidence_table_reference"] = {
        "description": "Confidence Score Reference Table",
        "table": {
            "0.9": {"level": "Very High", "meaning": "Agent is extremely confident in detection", "keywords": ["CLEARLY", "DEFINITELY", "CERTAINLY", "OBVIOUSLY", "UNDOUBTEDLY", "WITHOUT DOUBT", "CONFIRMED", "IDENTIFIED"]},
            "0.8": {"level": "High", "meaning": "Agent detected violation with high certainty", "keywords": ["YES", "VIOLATION", "DETECTED", "FOUND", "PRESENT", "SHOWS", "CONTAINS", "DISPLAYS"]},
            "0.6": {"level": "Medium-High", "meaning": "Agent thinks violation is likely", "keywords": ["LIKELY", "PROBABLY", "APPEARS", "SEEMS", "INDICATES", "SUGGESTS", "MIGHT BE"]},
            "0.5": {"level": "Medium", "meaning": "Agent is uncertain or neutral", "keywords": ["No specific confidence indicators found"]},
            "0.4": {"level": "Medium-Low", "meaning": "Agent is uncertain about detection", "keywords": ["UNCERTAIN", "NOT CLEARLY", "MAYBE", "POSSIBLY", "MIGHT", "COULD BE", "UNSURE"]},
            "0.1": {"level": "Low", "meaning": "Agent found no violations", "keywords": ["NO", "NOT DETECTED", "CLEAN", "SAFE", "NONE FOUND", "ABSENT", "NOT PRESENT"]},
            "0.0": {"level": "Error", "meaning": "Agent failed to process", "keywords": ["Agent error or no response"]}
        },
        "explanation": {
            "0.9": "Very High - Strong evidence for decision-making",
            "0.8": "High - Reliable detection, can be used for automated decisions",
            "0.6": "Medium-High - Good evidence, may need review",
            "0.5": "Medium - Neutral evidence, requires human review",
            "0.4": "Medium-Low - Weak evidence, likely false positive",
            "0.1": "Low - Strong evidence of safety",
            "0.0": "Error - No evidence available, manual review required"
        }
    }
    
    json_report = json.dumps(report_with_reference, indent=2, default=str)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(json_report)
        print(f"📄 Report exported to: {output_path}")
    
    return json_report 