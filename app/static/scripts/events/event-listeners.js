import { ui } from "../ui/ui-elements.js"
import { appState } from "../app/state.js";
import { toggleTheme } from "../ui/theme.js";
import { applyFiltersAndSorting } from "../features/insights.js";
import { handleAnalysisFileSelect, handleReportFileUpload } from "../features/file-handlers.js";
import { startAnalysis, resetUI } from "../app/handlers.js";
import { downloadReportAsJSON, downloadReportAsHTML } from "../features/reporting.js";

export function initializeEventListeners() {
    // Form and action buttons
    ui.apiKeyInput.addEventListener("input", checkFormValidity);
    ui.analyzeBtn.addEventListener("click", startAnalysis);
    ui.resetBtn.addEventListener("click", resetUI);
    ui.cancelBtn.addEventListener("click", () => appState.analysisController?.abort());

    // Theme toggle
    ui.themeToggleBtn.addEventListener("click", toggleTheme);
    
    // File inputs
    ui.fileUploadInput.addEventListener("change", handleAnalysisFileSelect);
    ui.reportUploadInput.addEventListener("change", handleReportFileUpload);

    // Filter and sort controls
    ui.filterDropdown.addEventListener("change", applyFiltersAndSorting);
    ui.sortDropdown.addEventListener("change", applyFiltersAndSorting);
    ui.sortDirectionBtn.addEventListener("click", () => {
        appState.sortDirection = appState.sortDirection === "desc" ? "asc" : "desc";
        ui.sortDirectionBtn.classList.toggle("sort-ascending", appState.sortDirection === "asc");
        applyFiltersAndSorting();
    });

    // Download dropdown
    ui.downloadDropdownBtn.addEventListener("click", () => ui.downloadOptions.classList.toggle("hidden"));
    document.addEventListener("click", (e) => {
        if (!e.target.closest("#download-dropdown-container")) { ui.downloadOptions.classList.add("hidden"); }
    });
    ui.downloadJsonBtn.addEventListener("click", (e) => { e.preventDefault(); downloadReportAsJSON(); ui.downloadOptions.classList.add("hidden"); });
    ui.downloadHtmlBtn.addEventListener("click", (e) => { e.preventDefault(); downloadReportAsHTML(); ui.downloadOptions.classList.add("hidden"); });

    // Drag and Drop area
    ui.dropArea.addEventListener("dragover", (e) => { e.preventDefault(); ui.dropArea.classList.add("themed-accent-border"); });
    ui.dropArea.addEventListener("dragleave", () => ui.dropArea.classList.remove("themed-accent-border"));
    ui.dropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        ui.dropArea.classList.remove("themed-accent-border");
        if (e.dataTransfer.files?.length > 0) {
            ui.fileUploadInput.files = e.dataTransfer.files;
            handleAnalysisFileSelect();
        }
    });
}

// Helper function also used by event listeners
function checkFormValidity() {
    const canAnalyze = ui.apiKeyInput.value.trim() !== '' && appState.currentFile !== null;
    ui.analyzeBtn.disabled = !canAnalyze;
    ui.analyzeBtn.classList.toggle("btn-pulsate", canAnalyze);
}