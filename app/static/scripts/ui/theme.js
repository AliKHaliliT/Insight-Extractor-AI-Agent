import { ui } from "./ui-elements.js";
import { redrawAllCharts } from "../features/chart.js";

export function initializeTheme() {
    const preferredTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", preferredTheme);
    updateThemeIcons(preferredTheme);
}

export function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeIcons(newTheme);
    redrawAllCharts();
}

function updateThemeIcons(theme) {
    if (theme === "light") {
        ui.themeIconSun.classList.add("hidden");
        ui.themeIconMoon.classList.remove("hidden");
    } else {
        ui.themeIconSun.classList.remove("hidden");
        ui.themeIconMoon.classList.add("hidden");
    }
}