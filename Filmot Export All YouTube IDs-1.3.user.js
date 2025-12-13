// ==UserScript==
// @name         Filmot Export All YouTube IDs
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  Collect all YouTube IDs from all pages and export as TXT after last page reached. Auto-resumes, stoppable, with custom filename.
// @match        https://filmot.com/channel/*
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(function() {
    'use strict';

    const NEXT_PAGE_SELECTOR = "a,button";
    const NEXT_PAGE_TEXT_REGEX = /next\s*page/i;
    const PAGE_LOAD_WAIT_MS = 3000;

    let collectedIDs = GM_getValue("yt_video_ids", []);
    let running = GM_getValue("yt_export_running", false);

    const exportBtn = document.createElement("button");
    updateButton();

    Object.assign(exportBtn.style, {
        position: "fixed",
        top: "20px",
        right: "20px",
        zIndex: "99999",
        padding: "10px 14px",
        border: "none",
        fontSize: "16px",
        borderRadius: "6px",
        cursor: running ? "not-allowed" : "pointer",
        boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
        color: "white"
    });
    document.body.appendChild(exportBtn);

    function updateButton() {
        if (running) {
            exportBtn.textContent = "STOP Export";
            exportBtn.style.background = "#dc3545";
            exportBtn.style.cursor = "pointer";
        } else {
            exportBtn.textContent = "Start Export";
            exportBtn.style.background = "#007bff";
            exportBtn.style.cursor = "pointer";
        }
    }

    function findNextPageButton() {
        const btn = [...document.querySelectorAll(NEXT_PAGE_SELECTOR)]
            .find(el => NEXT_PAGE_TEXT_REGEX.test(el.textContent) && !el.disabled && el.offsetParent !== null);
        return btn || null;
    }

    function extractYouTubeIDs() {
        const links = [...document.querySelectorAll("a[href*='youtube.com/watch?v=']")];
        let newIDs = [];

        links.forEach(link => {
            try {
                const url = new URL(link.href);
                const v = url.searchParams.get("v");
                if (v && !collectedIDs.includes(v)) {
                    collectedIDs.push(v);
                    newIDs.push(v);
                }
            } catch (e) {}
        });

        console.log(`[YouTube Export] Found ${newIDs.length} new IDs on this page.`);
        return newIDs.length;
    }

    function saveIDs() {
        GM_setValue("yt_video_ids", collectedIDs);
    }

    function saveRunningState(val) {
        running = val;
        GM_setValue("yt_export_running", val);
        updateButton();
    }

    function downloadIDs() {
        if (collectedIDs.length === 0) {
            alert("No YouTube IDs collected.");
            return;
        }
        const blob = new Blob([collectedIDs.join("\n")], {type: "text/plain"});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "video_ids.txt";   // <-- filename changed here
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
            URL.revokeObjectURL(url);
            a.remove();
        }, 100);
    }

    async function processPage() {
        if (!running) return;

        extractYouTubeIDs();
        saveIDs();

        const nextBtn = findNextPageButton();
        if (nextBtn) {
            console.log("[YouTube Export] Next page found. Navigating...");
            nextBtn.click();

            await new Promise(r => setTimeout(r, PAGE_LOAD_WAIT_MS));
            await processPage();
        } else {
            console.log("[YouTube Export] No Next Page button found. Exporting collected IDs.");
            saveRunningState(false);
            downloadIDs();
        }
    }

    exportBtn.onclick = () => {
        if (running) {
            // Stop export loop
            saveRunningState(false);
            alert("Export stopped by user.");
        } else {
            // Start export loop
            collectedIDs = [];
            saveIDs();
            saveRunningState(true);
            console.log("[YouTube Export] Starting export...");
            processPage();
        }
    };

    window.addEventListener("load", () => {
        if (running) {
            console.log("[YouTube Export] Auto-resuming export after navigation.");
            setTimeout(processPage, PAGE_LOAD_WAIT_MS);
        }
    });

})();
