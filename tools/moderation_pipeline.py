from tools.image_preprocessor import image_preprocessor
from tools.nudity_detector import detect_nudity
from tools.nudity_exceptions_detector_gemini import detect_nudity_exceptions_with_gemini
from tools.violence_detection_gemini import detect_violence_with_gemini
from tools.drugs_detector_gemini import detect_drugs_with_gemini
from tools.alcohol_smoke_detector_gemini import detect_alcohol_smoke_with_gemini
from tools.hate_detector_gemini import detect_hate_symbols_with_gemini
from tools.text_pii_detector_gemini import detect_text_pii_with_gemini
from tools.qr_detector_gemini import detect_qr_code_with_gemini

def run_moderation_pipeline(image_path: str) -> dict:
    report = {
        "image_path": image_path,
        "results": {},
        "final_decision": "Accept"
    }

    # 1. Ingestion
    preprocessed = image_preprocessor(image_path)
    report["results"]["ingestion"] = preprocessed
    if preprocessed.get("status") != "success":
        report["final_decision"] = "Reject"
        return report

    processed_path = preprocessed["output_path"]

    # 2. Nudity Detection
    nudity = detect_nudity(processed_path)
    report["results"]["nudity"] = nudity

    # 3. Nudity Exception Detection
    nudity_exception = detect_nudity_exceptions_with_gemini(processed_path)
    report["results"]["nudity_exceptions"] = nudity_exception

    # 4. Violence Detection
    violence = detect_violence_with_gemini(processed_path)
    report["results"]["violence"] = violence

    # 5. Drugs Detection
    drugs = detect_drugs_with_gemini(processed_path)
    report["results"]["drugs"] = drugs

    # 6. Alcohol/Smoking Detection
    alcohol = detect_alcohol_smoke_with_gemini(processed_path)
    report["results"]["alcohol_smoking"] = alcohol

    # 7. Hate Symbols Detection
    hate = detect_hate_symbols_with_gemini(processed_path)
    report["results"]["hate"] = hate

    # 8. Text/PII Detection
    pii = detect_text_pii_with_gemini(processed_path)
    report["results"]["pii_text"] = pii

    # 9. QR Code Detection
    qr = detect_qr_code_with_gemini(processed_path)
    report["results"]["qr_code"] = qr

    # ⛔️ Rule-based Decision Logic
    flagged = []
    if nudity.get("label") == "unsafe":
        flagged.append("nudity")
    if "YES" in (violence.get("response_text") or "").upper():
        flagged.append("violence")
    if "YES" in (drugs.get("response_text") or "").upper():
        flagged.append("drugs")
    if "YES" in (alcohol.get("response_text") or "").upper():
        flagged.append("alcohol/smoking")
    if "YES" in (hate.get("response_text") or "").upper():
        flagged.append("hate")
    if "YES" in (pii.get("response_text") or "").upper():
        flagged.append("pii/text")
    if "YES" in (qr.get("response_text") or "").upper():
        flagged.append("qr code")

    if flagged:
        report["final_decision"] = "Flagged"
        report["violations"] = flagged

    return report
