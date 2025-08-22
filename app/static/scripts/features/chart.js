import { appState } from "../app/state.js";

export function createSentimentChart(canvasElement, score) {
    if (!canvasElement || !canvasElement.getContext) return;
    
    if (!canvasElement.id) {
        canvasElement.id = `chart-${Math.random().toString(36).substring(2, 9)}`;
    }

    const ctx = canvasElement.getContext("2d");
    const isDarkMode = (document.documentElement.getAttribute("data-theme") || "dark") === "dark";
    const chart = new Chart(ctx, {
        type: "doughnut",
        data: { datasets: [{ data: [(score + 1) / 2, 1 - ((score + 1) / 2)], backgroundColor: [score > 0.2 ? "rgb(52, 211, 153)" : score < -0.2 ? "rgb(248, 113, 113)" : "rgb(250, 204, 21)", isDarkMode ? "#334155" : "#e2e8f0"], borderColor: isDarkMode ? "#0f172a" : "#f1f5f9", borderWidth: 2, cutout: "70%" }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { enabled: false } }, animation: { animateRotate: true, duration: 1500 } },
        plugins: [{ id: "doughnutText", afterDraw(chart) {
            const { ctx, width, height } = chart;
            ctx.restore();
            ctx.font = "bold 1.2rem Inter";
            ctx.fillStyle = isDarkMode ? "#f1f5f9" : "#1e293b";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(`${Math.round(((score + 1) / 2) * 100)}%`, width / 2, height / 2);
            ctx.save();
        }}]
    });
    appState.activeCharts.push({ instance: chart, canvas: canvasElement, score: score });
}

export function destroyCharts() { 
    appState.activeCharts.forEach(chart => chart.instance.destroy()); 
    appState.activeCharts = []; 
}

export function redrawAllCharts() {
    const chartsToRedraw = [...appState.activeCharts];
    destroyCharts();
    chartsToRedraw.forEach(chartInfo => createSentimentChart(chartInfo.canvas, chartInfo.score));
}