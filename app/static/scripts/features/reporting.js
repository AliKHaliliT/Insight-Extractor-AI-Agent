import { appState } from "../app/state.js";
import { ui } from "../ui/ui-elements.js";

function triggerDownload(blob, fileExtension) {
    if (!appState.currentReportData) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const safeFilename = (appState.currentReportData.file_name || "file").replace(/[^a-z0-9_.-]/gi, "_");
    a.href = url;
    a.download = `analysis_report_${safeFilename}.${fileExtension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

export function downloadReportAsJSON() {
    const jsonString = JSON.stringify(appState.currentReportData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    triggerDownload(blob, "json");
}

export async function downloadReportAsHTML() {
    if (!appState.currentReportData) return;

    // 1. Clone the results section and remove interactive UI elements
    const reportClone = ui.resultsSection.cloneNode(true);
    reportClone.classList.remove("hidden", "opacity-0");
    reportClone.querySelector("#report-actions")?.remove();
    reportClone.querySelector("#filter-sort-controls")?.remove();

    // 2. Replace each canvas with a static image of the chart
    appState.activeCharts.forEach(chartInfo => {
        const canvasInClone = reportClone.querySelector(`#${chartInfo.canvas.id}`);
        if (canvasInClone) {
            const image = new Image();
            image.src = chartInfo.instance.toBase64Image();
            image.style.width = "100%";
            image.style.height = "auto";
            image.className = canvasInClone.className;
            canvasInClone.parentNode.replaceChild(image, canvasInClone);
        }
    });

    // 3. Gather styles and create the final HTML string
    const cssStyles = Array.from(document.styleSheets).map(sheet => {
        try { return Array.from(sheet.cssRules).map(rule => rule.cssText).join(''); } catch (e) { return ''; }
    }).join("\n");

    const htmlString = `<!DOCTYPE html><html lang="en" data-theme="${localStorage.getItem("theme") || "dark"}"><head><meta charset="UTF-8"><title>Report: ${appState.currentReportData.file_name}</title><script src="https://cdn.tailwindcss.com"><\/script><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><style>body{font-family:"Inter",sans-serif;padding:2rem;}${cssStyles}<\/style></head><body><div class="w-full max-w-7xl mx-auto">${reportClone.innerHTML}</div></body></html>`;
    
    // 4. Trigger the download
    const blob = new Blob([htmlString], { type: "text/html" });
    triggerDownload(blob, "html");
}