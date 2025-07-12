import os
import sys
import requests
import tempfile
import pandas as pd
from tools.central_moderation_pipeline import run_central_moderation_pipeline, print_moderation_report
import time

# Path to the Excel file and sheet name
EXCEL_PATH = r"data/test_images/dateSetContentMod.xlsx"
SHEET_NAME = "indiamart images (rejected)"
OUTPUT_PATH = r"data/test_images/dateSetContentMod_results.xlsx"

# Define all possible violation types (flags)
VIOLATION_FLAGS = [
    "nudity", "nudity_exceptions", "violence", "drugs", "alcohol_smoking",
    "hate", "pii_text", "qr_code"
]

# Helper to download image if URL, else return local path
def get_local_image_path(image_url):
    if image_url.startswith('http://') or image_url.startswith('https://'):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            for chunk in response.iter_content(1024):
                tmp.write(chunk)
            tmp.close()
            return tmp.name
        else:
            print(f"Failed to download image: {image_url}")
            return None
    else:
        return image_url if os.path.exists(image_url) else None

def main():
    # Read Excel
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    df = df.reset_index(drop=True)
    # Ensure the column exists
    if 'image_url' not in df.columns:
        print("No 'image_url' column found!")
        return
    # Prepare output column
    if 'CM_ADK Decision' not in df.columns:
        df['CM_ADK Decision'] = ''
    
    # Before the loop, ensure columns exist
    for flag in VIOLATION_FLAGS:
        if flag not in df.columns:
            df[flag] = 0  # or False, or ""

    total_images = 0
    total_time_taken = 0.0
    per_image_times = []
    batch_start_time = time.time()
    
    for idx, row in enumerate(df.itertuples(index=False)):
        image_url = str(getattr(row, 'image_url', '')).strip()
        if not image_url:
            continue
        print(f"Processing row {idx+1}: {image_url}")
        local_path = get_local_image_path(image_url)
        if not local_path:
            print(f"  Skipping: Could not access image {image_url}")
            df.at[idx, 'CM_ADK Decision'] = 'Error'
            continue
        start_time = time.time()
        result = run_central_moderation_pipeline(local_path)
        end_time = time.time()
        elapsed = end_time - start_time
        per_image_times.append(elapsed)
        total_time_taken += elapsed
        total_images += 1
        print(f"⏱️ Time taken for this image: {elapsed:.2f} seconds")
        # Print detailed summary for this image
        print_moderation_report(result)
        decision = result.get('final_decision', '').lower()
        if decision == 'accept':
            df.at[idx, 'CM_ADK Decision'] = 'A'
        elif decision == 'reject':
            df.at[idx, 'CM_ADK Decision'] = 'R'
        else:
            df.at[idx, 'CM_ADK Decision'] = decision[:1].upper() if decision else 'Error'
        print(f"ContentModeration_ADK Decision: {df.at[idx, 'CM_ADK Decision']}")
        # Set flags for this row
        for flag in VIOLATION_FLAGS:
            # If the violation is present in the violations list, set 1, else 0
            df.at[idx, flag] = 1 if flag in result.get("violations", []) else 0
        # Clean up temp file if downloaded
        if local_path.startswith(tempfile.gettempdir()):
            try:
                os.remove(local_path)
            except Exception:
                pass
        # Save results after each image
        df.to_excel(OUTPUT_PATH, sheet_name=SHEET_NAME, index=False)
    batch_end_time = time.time()
    batch_total_time = batch_end_time - batch_start_time
    print(f"Done! Results saved to {OUTPUT_PATH}")
    print("\n================ Efficiency Metrics ================")
    print(f"Total images processed: {total_images}")
    print(f"Total batch processing time: {batch_total_time:.2f} seconds")
    if total_images > 0:
        avg_time = total_time_taken / total_images
        throughput = total_images / batch_total_time if batch_total_time > 0 else 0
        print(f"Average time per image: {avg_time:.2f} seconds")
        print(f"Throughput: {throughput:.2f} images/second")
    print("===================================================\n")

if __name__ == "__main__":
    main() 