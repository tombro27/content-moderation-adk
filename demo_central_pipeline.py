#!/usr/bin/env python3
"""
Central Moderation Pipeline Demo

This script demonstrates the comprehensive content moderation pipeline
that runs all individual agents sequentially on an image.

Usage:
    python demo_central_pipeline.py [image_path]
    
Example:
    python demo_central_pipeline.py data/test_images/blood.jpg
"""

import sys
import os
from tools.central_moderation_pipeline import (
    run_central_moderation_pipeline,
    print_moderation_report,
    export_json_report
)

def main():
    """Run the central moderation pipeline demo."""
    
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "data/test_images/blood.jpg"
    
    print("🛡️ CENTRAL MODERATION PIPELINE DEMO")
    print("="*80)
    print(f"📁 Processing: {image_path}")
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        print("Available test images:")
        test_dir = "data/test_images"
        if os.path.exists(test_dir):
            for file in os.listdir(test_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"   - {test_dir}/{file}")
        return
    
    print("\n🔄 Starting Central Moderation Pipeline...")
    print("This will run all agents sequentially:")
    print("   🧹 Ingestion → 🔞 Nudity → 👙 Exceptions → 🔫 Violence")
    print("   🧪 Drugs → 🍾 Alcohol/Smoking → ☠️ Hate → 🔐 PII → 📷 QR")
    print()
    
    # Run the pipeline
    report = run_central_moderation_pipeline(image_path)
    
    # Print the comprehensive report
    print_moderation_report(report)
    
    # Export JSON report
    json_filename = f"central_pipeline_report_{os.path.basename(image_path).split('.')[0]}.json"
    export_json_report(report, json_filename)
    
    # Print summary
    print(f"\n📊 QUICK SUMMARY")
    print(f"   Image: {os.path.basename(image_path)}")
    print(f"   Decision: {report.get('final_decision')}")
    print(f"   Violations: {len(report.get('violations', []))}")
    print(f"   Status: {report.get('status')}")
    print(f"   JSON Report: {json_filename}")
    
    # Show decision explanation
    decision = report.get('final_decision')
    violations = report.get('violations', [])
    
    print(f"\n🎯 DECISION EXPLANATION:")
    if decision == "Accept":
        print("   ✅ Image passed all moderation checks")
    elif decision == "Reject":
        print("   ❌ Image contains high-priority violations requiring immediate rejection")
        if violations:
            print(f"   🚨 Violations: {', '.join(violations)}")
    elif decision == "Flag":
        print("   ⚠️ Image contains violations requiring human review")
        if violations:
            print(f"   🚨 Violations: {', '.join(violations)}")
    
    print(f"\n✅ Demo completed! Check {json_filename} for detailed results.")

if __name__ == "__main__":
    main() 