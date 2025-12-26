import requests
import time
from openpyxl import Workbook

def check_redirects(file_path, output_xlsx, max_retries=3):
    base_url = "https://web.archive.org/web/1oe_/http://wayback-fakeurl.archive.org/yt/{}"
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; VideoCheckBot/1.0)"
    }

    with open(file_path, 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]

    total = len(video_ids)

    wb = Workbook()
    ws = wb.active
    ws.title = "Results"
    ws.append(["video_id", "result"])

    for index, vid in enumerate(video_ids, start=1):
        url = base_url.format(vid)
        attempt = 0

        while attempt <= max_retries:
            try:
                resp = session.get(
                    url,
                    headers=headers,
                    allow_redirects=False,
                    timeout=10
                )

                if 300 <= resp.status_code < 400:
                    ws.append([vid, url])
                    print(f"[{index}/{total}] {vid}: redirect -> {url}")
                else:
                    ws.append([vid, "unavailable"])
                    print(f"[{index}/{total}] {vid}: unavailable")
                break

            except requests.RequestException:
                attempt += 1
                if attempt > max_retries:
                    ws.append([vid, "unavailable"])
                    print(f"[{index}/{total}] {vid}: error after retries")
                else:
                    time.sleep(2 ** attempt)

    wb.save(output_xlsx)

if __name__ == "__main__":
    check_redirects("video_ids.txt", "results.xlsx")
