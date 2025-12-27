# YouTube Channel Wayback Machine Archive Tools

A set of tools for finding **deleted or privated YouTube videos** preserved on the  
**Internet Archive / Wayback Machine** from a specific YouTube channel.

This workflow helps identify which videos still have **playable archived MP4 pages** and retrieves metadata such as **title, upload date, and uploader**.

---

## Requirements

### Must Have
- [Python](https://www.python.org/downloads/)
- [Yt-Dlp](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation)
- **openpyxl**

```bash
pip install openpyxl
```
### Optional
- **Tampermonkey Extension/Addon**
  
Or you can just export all urls page by page on https://filmot.com/channel/ then join them together using your own script or manually

- **Excel/Google Sheets**

You can use any program that handles editing and filtering spreadsheets file such as xlsx,csv,...

---

## How to Use

[![Watch the video](https://img.youtube.com/vi/ISzYs-peogU/0.jpg)](https://youtu.be/ISzYs-peogU)


- **Web archive.py**

  Prepare a file named **video_ids.txt** containing video ids on each line + **Web archive.py** in the same folder then run the script. It will combine the ids with https://web.archive.org/web/1oe_/http://wayback-fakeurl.archive.org/yt/{insert_id_here} to check which video id has a playable mp4 archive page.

  <img width="180" height="173" alt="image" src="https://github.com/user-attachments/assets/1c7af25e-aa77-4d10-9576-f57dbd9734a2" />
  
  <img width="119" height="44" alt="image" src="https://github.com/user-attachments/assets/57512c38-6831-4fd8-aefe-aed6ff4077bb" />

- **Excel/Google Sheets**

  Open the **xlsx file**, filter out all the unavailable video ids, then copy all the web archive links, then paste them into **Downloads.txt**

- **Retrieve Titles+Dates+Uploader.py**
  
  Prepare **Downloads.txt** as above and also have **Retrieve Titles+Dates+Uploader.py** in the same folder, then run it. It uses yt-dlp to extract the titles, upload dates, and uploader of each video id, which is really slow; a faster way is to scrape each page with a script(which I don't know how to make due to Cloudflare mitigation) or with an userscript you can make in 5mins using **ChatGPT**

  <img width="226" height="44" alt="image" src="https://github.com/user-attachments/assets/8cd5a850-6304-45e2-adf6-bdd0eeba4762" />


---




