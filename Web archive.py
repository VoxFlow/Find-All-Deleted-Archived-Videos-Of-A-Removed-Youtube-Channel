import requests
import csv

def check_redirects(file_path, output_csv, max_retries=3):
    base_url = "https://web.archive.org/web/1oe_/http://wayback-fakeurl.archive.org/yt/{}"
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; VideoCheckBot/1.0)"
    }

    with open(file_path, 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['video_id', 'result'])

        for vid in video_ids:
            url = base_url.format(vid)
            attempt = 0
            while attempt <= max_retries:
                try:
                    # Send request without following redirects
                    resp = session.get(url, headers=headers, allow_redirects=False, timeout=10)

                    if resp.status_code in range(300, 399):
                        # It redirects -> save original URL
                        writer.writerow([vid, url])
                        print(f"{vid}: Redirects -> {url}")
                    else:
                        # No redirect
                        writer.writerow([vid, "unavailable."])
                        print(f"{vid}: No redirect -> unavailable.")
                    break  # done with this video ID

                except requests.RequestException as e:
                    attempt += 1
                    if attempt > max_retries:
                        writer.writerow([vid, f"Error - {e}"])
                        print(f"{vid}: Error after {max_retries} retries - {e}")
                    else:
                        wait_time = 2 ** attempt
                        print(f"{vid}: Attempt {attempt} failed with error: {e}. Retrying in {wait_time}s...")
                        import time
                        time.sleep(wait_time)

if __name__ == "__main__":
    input_file = "video_ids.txt"
    output_file = "results.csv"
    check_redirects(input_file, output_file)
