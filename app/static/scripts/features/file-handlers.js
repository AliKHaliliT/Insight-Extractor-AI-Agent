import { ui } from "../ui/ui-elements.js";
import { appState } from "../app/state.js";
import { displayResults } from "./insights.js";
import { updateUIState, handleError } from "../ui/ui-state.js";

export function handleAnalysisFileSelect() {
    if (ui.fileUploadInput.files.length > 0) {
        appState.currentFile = ui.fileUploadInput.files[0];
        ui.dropAreaText.innerHTML = `<span class="font-semibold" style="color: #2dd4bf;">${appState.currentFile.name}</span> selected`;
    } else {
        appState.currentFile = null;
        ui.dropAreaText.innerHTML = `<span class="font-semibold themed-text-accent">Click to upload</span> or drag and drop`;
    }
    // Directly call the validity check function from the eventListeners module
    // This is a small exception to the single-responsibility rule for practicality.
    const canAnalyze = ui.apiKeyInput.value.trim() !== '' && appState.currentFile !== null;
    ui.analyzeBtn.disabled = !canAnalyze;
    ui.analyzeBtn.classList.toggle("btn-pulsate", canAnalyze);
}

export function handleReportFileUpload() {
    const file = ui.reportUploadInput.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
        try {
            const reportData = JSON.parse(event.target.result);
            if (reportData.file_name && reportData.executive_summary && Array.isArray(reportData.insights)) {
                appState.currentReportData = reportData;
                displayResults(reportData);
                updateUIState("results");
            } else { throw new Error("Invalid report file format."); }
        } catch (error) { handleError(error, `Failed to load report: ${error.message}`); }
    };
    reader.onerror = () => handleError(reader.error, "Failed to read the report file.");
    reader.readAsText(file);
}