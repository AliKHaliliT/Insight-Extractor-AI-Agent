import { ui, CSS_CLASSES } from "./ui-elements.js";

export function updateUIState(state) {
    // Add a state class to the main container to control its layout
    ui.appContainer.className = ui.appContainer.className.replace(/state-\w+/g, '').trim();
    ui.appContainer.classList.add(`state-${state}`);

    // Hide all sections first
    [ui.setupSection, ui.loadingSection, ui.resultsSection].forEach(section => {
        section.classList.add(CSS_CLASSES.hidden, CSS_CLASSES.opacityZero);
    });

    // Then reveal the target section with a fade-in
    const targetSection = ui[`${state}Section`];
    if (targetSection) {
        targetSection.classList.remove(CSS_CLASSES.hidden);
        setTimeout(() => targetSection.classList.remove(CSS_CLASSES.opacityZero), 20);
    }
}

export function displayError(message) { 
    ui.errorMessage.textContent = message; 
    ui.errorContainer.classList.remove(CSS_CLASSES.hidden); 
}

export function clearError() { 
    ui.errorContainer.classList.add(CSS_CLASSES.hidden); 
    ui.errorMessage.textContent = ''; 
}

export function handleError(error, userMessage) { 
    console.error("An error occurred:", error); 
    displayError(userMessage || `An unexpected error occurred: ${error.message}`); 
}