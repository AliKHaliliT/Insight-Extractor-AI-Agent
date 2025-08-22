import { ui } from "../ui/ui-elements.js"
import { appState } from "./state.js";
import { performAnalysis } from "../api/api.js";
import { displayResults } from "../features/insights.js";
import { destroyCharts } from "../features/chart.js";
import { updateUIState, clearError, handleError } from "../ui/ui-state.js";
import { handleAnalysisFileSelect } from "../features/file-handlers.js";

export async function startAnalysis() {
    if (!ui.apiKeyInput.value.trim() || !appState.currentFile) return displayError("Please provide an API key and select a file.");
    if (!ui.modelSelect.value) return displayError("Please wait for models to load or select a model.");
    
    clearError();
    updateUIState("loading");
    appState.cancelTimer = setTimeout(() => ui.cancelBtn.classList.remove("hidden"), 8000);
    appState.analysisController = new AbortController();

    try {
        const reportData = await performAnalysis(
            ui.apiKeyInput.value.trim(),
            appState.currentFile,
            ui.modelSelect.value,
            appState.analysisController.signal
        );
        appState.currentReportData = reportData;
        displayResults(reportData);
        updateUIState("results");
    } catch (error) {
        if (error.name === "AbortError") { 
            resetUI(); 
        } else { 
            handleError(error, `Analysis failed: ${error.message}`); 
            updateUIState("setup"); 
        }
    } finally {
        appState.analysisController = null;
        if (appState.cancelTimer) clearTimeout(appState.cancelTimer);
        appState.cancelTimer = null;
        ui.cancelBtn.classList.add("hidden");
    }
}

export function resetUI() {
    updateUIState("setup");
    ui.appContainer.className = "w-full max-w-7xl mx-auto state-setup";
    ui.apiKeyInput.value = '';
    ui.fileUploadInput.value = '';
    ui.reportUploadInput.value = '';
    appState.currentFile = null;
    appState.currentReportData = null;
    appState.analysisController?.abort();
    appState.analysisController = null;
    if (appState.cancelTimer) clearTimeout(appState.cancelTimer);
    appState.cancelTimer = null;
    ui.cancelBtn.classList.add("hidden");
    handleAnalysisFileSelect();
    destroyCharts();
    ui.insightsGrid.innerHTML = '';
    ui.executiveSummaryDisplay.textContent = '';
    ui.fileNameDisplay.textContent = '';
    ui.modelNameDisplay.textContent = '';
    clearError();
}