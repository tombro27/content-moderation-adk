import os
import sys
import requests
import tempfile
import pandas as pd
from tools.central_moderation_pipeline import run_central_moderation_pipeline, print_moderation_report

# Path to the Excel file and sheet name
EXCEL_PATH = r"data/test_images/dateSetContentMod.xlsx"
SHEET_NAME = "indiamart images (rejected)"
OUTPUT_PATH = r"data/test_images/dateSetContentMod_results.xlsx"

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
        result = run_central_moderation_pipeline(local_path)
        # Print detailed summary for this image
        print_moderation_report(result)
        decision = result.get('final_decision', '').lower()
        if decision == 'accept':
            df.at[idx, 'CM_ADK Decision'] = 'A'
        elif decision == 'reject':
            df.at[idx, 'CM_ADK Decision'] = 'R'
        else:
            df.at[idx, 'CM_ADK Decision'] = decision[:1].upper() if decision else 'Error'
        print(f"ContentModeratio_ADK Decision: {df.at[idx, 'CM_ADK Decision']}")
        # Clean up temp file if downloaded
        if local_path.startswith(tempfile.gettempdir()):
            try:
                os.remove(local_path)
            except Exception:
                pass
        # Save results after each image
        df.to_excel(OUTPUT_PATH, sheet_name=SHEET_NAME, index=False)
    print(f"Done! Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 