from tools.central_moderation_pipeline import (
    run_central_moderation_pipeline, 
    print_moderation_report, 
    export_json_report
)
import os
import json

def test_central_pipeline():
    """Test the central moderation pipeline with different test images."""
    
    # Test images from the data directory
    test_images = [
        "data/test_images/blood.jpg",      # Violence/Gore
        "data/test_images/nudeMen.jpg",    # Nudity
        "data/test_images/vapes.jpg",      # Smoking
        "data/test_images/alcohol.jpg",    # Alcohol
        "data/test_images/gun.jpg",        # Weapons
        "data/test_images/QR.png",         # QR Code
        "data/test_images/adhaar.png",     # PII
        "data/test_images/hateSymbol.png", # Hate Symbols
        "data/test_images/sample.jpg",     # Clean image
    ]
    
    print("🛡️ CENTRAL MODERATION PIPELINE TESTING")
    print("="*80)
    
    for i, image_path in enumerate(test_images, 1):
        if not os.path.exists(image_path):
            print(f"⚠️ Image not found: {image_path}")
            continue
            
        print(f"\n{'='*80}")
        print(f"🧪 TEST {i}: {os.path.basename(image_path)}")
        print(f"{'='*80}")
        
        # Run the central pipeline
        report = run_central_moderation_pipeline(image_path)
        
        # Print formatted report
        print_moderation_report(report)
        
        # Export JSON report
        json_filename = f"report_{os.path.basename(image_path).split('.')[0]}.json"
        json_report = export_json_report(report, json_filename)
        
        print(f"\n📊 Summary for {os.path.basename(image_path)}:")
        print(f"   Decision: {report.get('final_decision')}")
        print(f"   Violations: {len(report.get('violations', []))}")
        print(f"   Status: {report.get('status')}")
        
        # Show confidence scores summary
        confidence_scores = report.get('confidence_scores', {})
        if confidence_scores:
            avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
            print(f"   Average Confidence: {avg_confidence:.2f}")
        
        print(f"   JSON Report: {json_filename}")
        
        print("\n" + "-"*80)

def test_single_image(image_path: str = "data/test_images/blood.jpg"):
    """Test the pipeline with a single image and detailed analysis."""
    
    print("🛡️ SINGLE IMAGE MODERATION TEST")
    print("="*80)
    print(f"📁 Testing: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    # Run pipeline
    report = run_central_moderation_pipeline(image_path)
    
    # Print detailed report
    print_moderation_report(report)
    
    # Export JSON
    json_filename = f"detailed_report_{os.path.basename(image_path).split('.')[0]}.json"
    export_json_report(report, json_filename)
    
    # Additional analysis
    print("\n🔍 ADDITIONAL ANALYSIS")
    print("-"*80)
    
    # Agent performance analysis
    agent_results = report.get('agent_results', {})
    confidence_scores = report.get('confidence_scores', {})
    
    print("📈 Agent Performance:")
    for agent, confidence in confidence_scores.items():
        status = agent_results.get(agent, {}).get('status', 'N/A')
        print(f"   {agent}: {confidence:.2f} ({status})")
    
    # Violation analysis
    violations = report.get('violations', [])
    if violations:
        print(f"\n🚨 Violation Analysis:")
        for violation in violations:
            print(f"   - {violation}")
    
    # Decision rationale
    decision = report.get('final_decision')
    print(f"\n🎯 Decision Rationale:")
    if decision == "Accept":
        print("   ✅ Image passed all moderation checks")
    elif decision == "Reject":
        print("   ❌ Image contains high-priority violations")
    elif decision == "Flag":
        print("   ⚠️ Image contains medium/low-priority violations requiring review")
    
    print(f"\n📄 Full JSON report saved to: {json_filename}")

def test_pipeline_performance():
    """Test pipeline performance and timing."""
    
    import time
    
    test_image = "data/test_images/sample.jpg"
    
    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}")
        return
    
    print("⏱️ PIPELINE PERFORMANCE TEST")
    print("="*80)
    
    start_time = time.time()
    report = run_central_moderation_pipeline(test_image)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    print(f"⏱️ Total Execution Time: {execution_time:.2f} seconds")
    print(f"📊 Pipeline Status: {report.get('status')}")
    print(f"🎯 Final Decision: {report.get('final_decision')}")
    
    # Agent timing breakdown (approximate)
    agent_count = len(report.get('agent_results', {}))
    avg_agent_time = execution_time / agent_count if agent_count > 0 else 0
    
    print(f"🧩 Average time per agent: {avg_agent_time:.2f} seconds")
    print(f"📈 Total agents executed: {agent_count}")

if __name__ == "__main__":
    print("🚀 Starting Central Moderation Pipeline Tests")
    print("="*80)
    
    # Test 1: Single image with detailed analysis
    print("\n1️⃣ SINGLE IMAGE TEST")
    test_single_image("data/test_images/blood.jpg")
    
    # Test 2: Multiple images
    print("\n2️⃣ MULTIPLE IMAGES TEST")
    test_central_pipeline()
    
    # Test 3: Performance test
    print("\n3️⃣ PERFORMANCE TEST")
    test_pipeline_performance()
    
    print("\n✅ All tests completed!")
    print("📁 Check the generated JSON files for detailed reports.") 