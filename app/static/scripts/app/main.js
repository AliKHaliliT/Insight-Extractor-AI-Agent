import { initializeEventListeners } from "../events/event-listeners.js";
import { initializeTheme } from "../ui/theme.js";
import { fetchModels } from "../api/api.js";
import { ui } from "../ui/ui-elements.js";
import { updateUIState } from "../ui/ui-state.js";

// --- App Initialization ---
document.addEventListener("DOMContentLoaded", async () => {
    // Set the initial UI state to the setup screen
    updateUIState("setup");

    // Initialize theme (dark/light mode)
    initializeTheme();

    // Setup all the user interaction event listeners
    initializeEventListeners();

    // Fetch the available AI models and populate the dropdown
    try {
        const modelsByProvider = await fetchModels();
        ui.modelSelect.innerHTML = ""; 
        for (const provider in modelsByProvider) {
            const optgroup = document.createElement("optgroup");
            optgroup.label = provider;
            modelsByProvider[provider].forEach(model => {
                const option = document.createElement("option");
                option.value = model.value;
                option.textContent = model.name;
                optgroup.appendChild(option);
            });
            ui.modelSelect.appendChild(optgroup);
        }
    } catch (error) {
        console.error("Could not load available models:", error);
        ui.modelSelect.innerHTML = "<option value=''>Could not load models</option>";
    }
});