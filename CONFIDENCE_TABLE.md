# 🎯 Confidence Score Reference Table

## 📊 Confidence Score Meanings

| Score Range | Level | Meaning | Keywords/Indicators | Decision Impact |
|-------------|-------|---------|-------------------|-----------------|
| **0.9** | **Very High** | Agent is extremely confident in detection | "CLEARLY", "DEFINITELY", "CERTAINLY", "OBVIOUSLY", "UNDOUBTEDLY", "WITHOUT DOUBT", "CONFIRMED", "IDENTIFIED" | Strong evidence for decision |
| **0.8** | **High** | Agent detected violation with high certainty | "YES", "VIOLATION", "DETECTED", "FOUND", "PRESENT", "SHOWS", "CONTAINS", "DISPLAYS" | Reliable detection |
| **0.6** | **Medium-High** | Agent thinks violation is likely | "LIKELY", "PROBABLY", "APPEARS", "SEEMS", "INDICATES", "SUGGESTS", "MIGHT BE" | Probable detection |
| **0.5** | **Medium** | Agent is uncertain or neutral | No specific confidence indicators found | Requires review |
| **0.4** | **Medium-Low** | Agent is uncertain about detection | "UNCERTAIN", "NOT CLEARLY", "MAYBE", "POSSIBLY", "MIGHT", "COULD BE", "UNSURE" | Weak detection |
| **0.1** | **Low** | Agent found no violations | "NO", "NOT DETECTED", "CLEAN", "SAFE", "NONE FOUND", "ABSENT", "NOT PRESENT" | Safe content |
| **0.0** | **Error** | Agent failed to process | Agent error or no response | Requires manual review |

## 🧩 Agent-Specific Confidence Calculation

### **NudeNet (Nudity Detection)**
```python
def calculate_nudity_confidence(nudity_result: dict) -> float:
    if nudity_result.get("label") == "unsafe":
        violations = nudity_result.get("violations", [])
        if violations:
            # Use actual NudeNet confidence scores
            max_confidence = max(violation.get("score", 0.5) for violation in violations)
            return max_confidence
        return 0.9  # Fallback
    else:
        return 0.1  # Safe content
```

**Confidence Sources:**
- **0.9**: Actual NudeNet violation scores (e.g., FEMALE_GENITALIA_EXPOSED: 0.85)
- **0.1**: Safe content detection
- **Fallback**: When NudeNet detects unsafe but no detailed scores available

### **Gemini-Based Agents**
All other agents use enhanced keyword analysis:

```python
def extract_confidence_from_response(response_text: str) -> float:
    # Comprehensive keyword analysis with priority scoring
    high_confidence = ["CLEARLY", "DEFINITELY", "CERTAINLY", "OBVIOUSLY", "UNDOUBTEDLY", "WITHOUT DOUBT", "CONFIRMED", "IDENTIFIED"]
    medium_high = ["YES", "VIOLATION", "DETECTED", "FOUND", "PRESENT", "SHOWS", "CONTAINS", "DISPLAYS"]
    medium = ["LIKELY", "PROBABLY", "APPEARS", "SEEMS", "INDICATES", "SUGGESTS", "MIGHT BE"]
    medium_low = ["UNCERTAIN", "NOT CLEARLY", "MAYBE", "POSSIBLY", "MIGHT", "COULD BE", "UNSURE"]
    low_confidence = ["NO", "NOT DETECTED", "CLEAN", "SAFE", "NONE FOUND", "ABSENT", "NOT PRESENT"]
```

## 📋 Confidence Score Examples

### **Violence Detection Examples**

| Response | Confidence | Explanation |
|----------|------------|-------------|
| "**Is the image violating any of the above?** YES<br>**If YES, specify the type(s) of violation**<br>1. Blood, wounds, gore, or severe injuries<br>**Briefly explain how you identified the violation(s)**<br>The image clearly depicts a human hand with a significant amount of blood and what appears to be an open, severe injury or wound on the palm." | **0.9** | Contains "CLEARLY" + "YES" + detailed explanation |
| "**Is the image violating any of the above?** YES<br>**If YES, specify the type(s) of violation**<br>1. Weapons such as guns, knives, grenades, or explosives<br>**Briefly explain how you identified the violation(s)**<br>The image shows what appears to be a firearm." | **0.8** | Contains "YES" + "SHOWS" + "APPEARS" |
| "**Is the image violating any of the above?** NO<br>**Briefly explain how you identified the violation(s)**<br>No violations detected in this image." | **0.1** | Contains "NO" + "NOT DETECTED" |

### **Nudity Detection Examples**

| NudeNet Result | Confidence | Explanation |
|----------------|------------|-------------|
| `{"label": "unsafe", "violations": [{"name": "FEMALE_GENITALIA_EXPOSED", "score": 0.87}]}` | **0.87** | Actual NudeNet confidence score |
| `{"label": "unsafe", "violations": [{"name": "MALE_GENITALIA_EXPOSED", "score": 0.92}]}` | **0.92** | Highest violation score |
| `{"label": "safe", "violations": []}` | **0.1** | Safe content detection |

### **Alcohol/Smoking Detection Examples**

| Response | Confidence | Explanation |
|----------|------------|-------------|
| "**Does the image contain any alcohol or smoking content?** YES<br>**If YES, what type(s)?**<br>1. Alcohol - beer bottles clearly visible<br>**Briefly explain how you identified the content**<br>The image clearly shows multiple beer bottles on a table." | **0.9** | Contains "CLEARLY" + "YES" + "SHOWS" |
| "**Does the image contain any alcohol or smoking content?** NO<br>**Briefly explain how you identified the content**<br>No alcohol or smoking content detected in this image." | **0.1** | Contains "NO" + "NOT DETECTED" |

## 🎯 Decision Impact by Confidence Level

### **High Confidence (0.8-0.9)**
- **Impact**: Strong evidence for decision-making
- **Action**: Can be used for automated decisions
- **Example**: Violence detection with 0.9 confidence → Strong case for rejection

### **Medium-High Confidence (0.6-0.7)**
- **Impact**: Good evidence, but may need review
- **Action**: Flag for human review
- **Example**: Drugs detection with 0.6 confidence → Flag for manual review

### **Medium Confidence (0.5)**
- **Impact**: Neutral evidence
- **Action**: Always requires human review
- **Example**: Uncertain detection → Manual review required

### **Medium-Low Confidence (0.4)**
- **Impact**: Weak evidence
- **Action**: Likely false positive, but review anyway
- **Example**: Uncertain violence detection → Review but likely safe

### **Low Confidence (0.1)**
- **Impact**: Strong evidence of safety
- **Action**: Can be trusted for safe content
- **Example**: No violations detected → Likely safe

### **Error Confidence (0.0)**
- **Impact**: No evidence available
- **Action**: Manual review required
- **Example**: Agent failure → Human review needed

## 📊 Confidence Aggregation

### **Average Confidence Calculation**
```python
avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
```

### **Weighted Confidence (by Agent Importance)**
```python
# High-priority agents get more weight
weights = {
    "nudity": 1.5,           # Critical
    "violence": 1.3,         # Critical
    "drugs": 1.2,            # Important
    "hate": 1.2,             # Important
    "alcohol_smoking": 1.0,  # Standard
    "qr_code": 0.8,          # Less critical
    "pii_text": 1.1,         # Important
    "nudity_exceptions": 1.0 # Standard
}
```

## 🔍 Confidence Validation

### **Expected Confidence Patterns**

| Violation Type | Expected High Confidence | Expected Low Confidence |
|----------------|-------------------------|------------------------|
| **Nudity** | 0.8-0.9 (when detected) | 0.1 (when safe) |
| **Violence** | 0.8-0.9 (clear violations) | 0.1 (no violence) |
| **Drugs** | 0.6-0.8 (clear paraphernalia) | 0.1 (no drugs) |
| **Alcohol** | 0.6-0.8 (clear bottles/cans) | 0.1 (no alcohol) |
| **Hate** | 0.7-0.9 (clear symbols) | 0.1 (no hate content) |

### **Confidence Quality Indicators**

- **Consistent High Confidence**: Reliable agent
- **Inconsistent Confidence**: Agent may need tuning
- **Always Low Confidence**: Agent may be too conservative
- **Always High Confidence**: Agent may be too aggressive

## 🚀 Confidence Improvement Tips

1. **Monitor Confidence Patterns**: Track which agents have consistent vs. inconsistent confidence
2. **Validate High Confidence**: Ensure high confidence predictions are actually correct
3. **Tune Keywords**: Adjust keyword lists based on actual response patterns
4. **Agent-Specific Tuning**: Different agents may need different confidence thresholds
5. **Historical Learning**: Use past results to improve confidence calculation

This enhanced confidence system provides much more nuanced and reliable confidence scoring for the moderation pipeline. 