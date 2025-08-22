import { ui } from "../ui/ui-elements.js";
import { appState } from "../app/state.js";
import { createInsightCard } from "../features/card-builder.js";
import { destroyCharts } from "../features/chart.js";

export function displayResults(data) {
    ui.fileNameDisplay.textContent = `File: ${data.file_name} (${data.file_type_detected})`;
    ui.executiveSummaryDisplay.textContent = data.executive_summary;
    ui.modelNameDisplay.textContent = data.model_used ? `Model: ${data.model_used}` : '';
    ui.modelNameDisplay.classList.toggle("hidden", !data.model_used);
    
    // Reset UI state for dropdowns and sort direction
    ui.filterDropdown.value = "All";
    ui.sortDropdown.value = "default";
    appState.sortDirection = "desc";
    ui.sortDirectionBtn.classList.remove("sort-ascending");
    
    applyFiltersAndSorting();
}

export function applyFiltersAndSorting() {
    if (!appState.currentReportData) return;

    const filterValue = ui.filterDropdown.value;
    const sortValue = ui.sortDropdown.value;
    let processedInsights = appState.currentReportData.insights;

    // 1. Filter
    if (filterValue !== "All") {
        processedInsights = processedInsights.filter(insight => insight.insight_type === filterValue);
    }

    // 2. Sort
    const severityOrder = { "Critical": 4, "High": 3, "Medium": 2, "Low": 1, "Informational": 0 };
    const direction = appState.sortDirection === "asc" ? 1 : -1;

    if (sortValue === "severity") {
        processedInsights.sort((a, b) => ((severityOrder[a.severity] || 0) - (severityOrder[b.severity] || 0)) * direction);
    } else if (sortValue === "confidence") {
        processedInsights.sort((a, b) => (a.confidence_score - b.confidence_score) * direction);
    }
    
    // 3. Render
    destroyCharts();
    ui.insightsGrid.innerHTML = ''; 

    if (processedInsights.length === 0) {
        const noInsightsMessage = document.createElement("div");
        noInsightsMessage.id = "no-insights-message";
        noInsightsMessage.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg><h4 class="text-lg font-semibold themed-text-primary">No Insights Found</h4><p class="themed-text-secondary">There are no insights matching the selected filter.</p>`;
        ui.insightsGrid.appendChild(noInsightsMessage);
    } else {
        processedInsights.forEach((insight, index) => ui.insightsGrid.appendChild(createInsightCard(insight, index)));
    }
}