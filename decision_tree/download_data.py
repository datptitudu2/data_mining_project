import os
import sys
import urllib.request
import time

DEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
TITANIC_DIR = os.path.join(DEST_DIR, "titanic")
EMAIL_DIR = os.path.join(DEST_DIR, "email_spam")

os.makedirs(TITANIC_DIR, exist_ok=True)
os.makedirs(EMAIL_DIR, exist_ok=True)

DOWNLOADS = [
    {
        "name": "Titanic - train.csv",
        "url": "https://raw.githubusercontent.com/minsuk-heo/kaggle-titanic/master/input/train.csv",
        "dest": os.path.join(TITANIC_DIR, "train.csv")
    },
    {
        "name": "Titanic - test.csv",
        "url": "https://raw.githubusercontent.com/minsuk-heo/kaggle-titanic/master/input/test.csv",
        "dest": os.path.join(TITANIC_DIR, "test.csv")
    },
    {
        "name": "Titanic - gender_submission.csv",
        "url": "https://raw.githubusercontent.com/minsuk-heo/kaggle-titanic/master/input/gender_submission.csv",
        "dest": os.path.join(TITANIC_DIR, "gender_submission.csv")
    },
    {
        "name": "Email Spam - emails.csv",
        "url": "https://raw.githubusercontent.com/KapadiaNaitik/DSDA-Emails/main/emails.csv",
        "dest": os.path.join(EMAIL_DIR, "emails.csv")
    }
]

def download_file(name, url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"[SKIP] {name} already exists ({os.path.getsize(dest):,} bytes) at {dest}")
        return
    print(f"[DOWNLOADING] {name} from {url}...")
    start = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
        total_size = response.getheader('Content-Length')
        total_size = int(total_size) if total_size else None
        downloaded = 0
        chunk_size = 1024 * 512 # 512KB chunks
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            downloaded += len(chunk)
            out_file.write(chunk)
            if total_size:
                percent = downloaded * 100 / total_size
                sys.stdout.write(f"\r  -> Progress: {downloaded:,} / {total_size:,} bytes ({percent:.1f}%)")
            else:
                sys.stdout.write(f"\r  -> Downloaded: {downloaded:,} bytes")
            sys.stdout.flush()
    elapsed = time.time() - start
    print(f"\n[DONE] Saved {name} to {dest} in {elapsed:.2f}s ({os.path.getsize(dest):,} bytes)")

if __name__ == "__main__":
    print("=== Downloading Datasets for Decision Tree ===")
    for item in DOWNLOADS:
        download_file(item["name"], item["url"], item["dest"])
    print("\nAll datasets downloaded successfully!")
