import subprocess
import json
import os
import csv
import time

INPUT_FILE = "Downloads.txt"
OUTPUT_FILE = "Titles and Dates.csv"
SLEEP_SECONDS = 1  # Adjust delay between requests if needed

def run_yt_dlp(url):
    video_id = url.rstrip("/").split("/")[-1]
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-info-json",
        "--no-playlist",
        "--ignore-errors",
        "--no-warnings",
        "-o", "%(id)s",  # name JSON file by video ID
        url
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return video_id
    except subprocess.CalledProcessError:
        return None

def extract_metadata(video_id):
    filename = f"{video_id}.info.json"
    if not os.path.exists(filename):
        return "unavailable", "unavailable"
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    # Delete JSON file after reading
    try:
        os.remove(filename)
    except Exception:
        pass

    title = data.get("title", "unavailable")
    upload_date_raw = data.get("upload_date", "")
    if len(upload_date_raw) == 8:
        upload_date = f"{upload_date_raw[:4]}-{upload_date_raw[4:6]}-{upload_date_raw[6:]}"
    else:
        upload_date = "unavailable"

    return title, upload_date

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file '{INPUT_FILE}' not found.")
        return

    with open(INPUT_FILE, encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []

    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Processing {url}")
        video_id = run_yt_dlp(url)
        if video_id is None:
            print("  yt-dlp failed to process this URL.")
            results.append({
                "video_id": "unknown",
                "title": "unavailable",
                "upload_date": "unavailable",
                "wayback_url": url
            })
            continue

        title, upload_date = extract_metadata(video_id)
        print(f"  Title: {title}")
        print(f"  Upload Date: {upload_date}")

        results.append({
            "video_id": video_id,
            "title": title,
            "upload_date": upload_date,
            "wayback_url": url
        })

        time.sleep(SLEEP_SECONDS)

    # Write CSV with BOM so Excel opens UTF-8 correctly
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["video_id", "title", "upload_date", "wayback_url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. Results saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
