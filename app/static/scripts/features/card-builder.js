import { ui } from "../ui/ui-elements.js";
import { createSentimentChart } from "./chart.js";

export function createInsightCard(insight, index) {
    const card = ui.insightCardTemplate.content.cloneNode(true).firstElementChild;
    card.style.animationDelay = `${index * 100}ms`;
    card.dataset.insightType = insight.insight_type;
    if (index === 0 || insight.severity === "Critical") { card.classList.add("lg:col-span-2"); }
    
    card.querySelector(".insight-title").textContent = insight.title;
    const severityEl = card.querySelector(".insight-severity");
    severityEl.textContent = insight.severity;
    severityEl.className += ` ${getSeverityStyles(insight.severity)}`;
    card.querySelector(".insight-severity-tooltip").textContent = getSeverityTooltipText(insight.severity);
    card.querySelector(".insight-type").textContent = insight.insight_type;
    
    const confidenceBarWidth = insight.confidence_score * 100;
    card.querySelector(".insight-confidence-bar").style.width = `${confidenceBarWidth}%`;
    card.querySelector(".insight-confidence-bar").classList.add(getConfidenceColor(insight.confidence_score));
    card.querySelector(".insight-confidence-text").textContent = `${Math.round(confidenceBarWidth)}%`;
    card.querySelector(".insight-description").textContent = insight.description;
    
    const detailsContainer = card.querySelector(".insight-details");
    detailsContainer.innerHTML = createInsightDetailsHTML(insight);
    if (insight.insight_type === "Sentiment Analysis") {
        setTimeout(() => createSentimentChart(detailsContainer.querySelector("canvas"), insight.sentiment.score), 0);
    }
    
    const groundingContainer = card.querySelector(".insight-grounding");
    if (insight.representative_snippet) { groundingContainer.innerHTML = createGroundingEvidenceHTML(insight); }
    
    const recommendationContainer = card.querySelector(".insight-recommendation");
    if (insight.actionable_recommendation) { recommendationContainer.innerHTML = createActionableRecommendationHTML(insight); }
    
    return card;
}

// --- Helper Functions for Card Building ---

function createInsightDetailsHTML(insight) {
    const cardInnerHTML = (title, content) => `<div class="themed-secondary-bg p-4 rounded-lg">${title}${content}</div>`;
    const titleHTML = (text) => `<p class="text-sm themed-text-secondary mb-1">${text}</p>`;
    const mainTextHTML = (text) => `<p class="text-3xl font-bold themed-text-primary">${text}</p>`;
    switch (insight.insight_type) {
        case "Quantitative Metric": return cardInnerHTML(titleHTML(insight.metric_name), mainTextHTML(`${insight.value}<span class="text-xl themed-text-secondary ml-1">${insight.unit || ''}</span>`));
        case "Key Theme":
            const keywordsHTML = insight.keywords.map(k => `<span class="themed-chip-bg themed-text-secondary text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full">${k}</span>`).join('');
            return `<div class="themed-secondary-bg p-4 rounded-lg flex justify-between items-center"><div>${titleHTML("Keywords")}<div class="mt-1">${keywordsHTML}</div></div><div class="text-center"><p class="text-3xl font-bold themed-text-primary">${insight.mentions}</p><p class="text-xs themed-text-secondary">Mentions</p></div></div>`;
        case "Sentiment Analysis": return `<div class="themed-secondary-bg p-4 rounded-lg"><div class="flex items-center space-x-4"><div class="w-24 h-24 flex-shrink-0"><canvas></canvas></div><div class="flex-1"><div class="tooltip-container mb-1"><p class="text-sm themed-text-secondary">Overall Sentiment</p><div class="info-icon">i</div><div class="tooltip-text">A score from -1 (very negative) to +1 (very positive). The chart shows the % positivity.</div></div><p class="text-lg font-bold themed-text-primary">${insight.sentiment.label}</p><p class="text-xs themed-text-secondary mt-1">${insight.sentiment.explanation}</p></div></div></div>`;
        case "Table Analysis": case "Code Analysis": return cardInnerHTML(titleHTML("AI Summary"), `<p class="themed-text-secondary">${insight.summary}</p>`);
        default: return '';
    }
}

function createGroundingEvidenceHTML(insight) {
    const locationsHTML = insight.locations.map(loc => `<span class="inline-block themed-chip-bg themed-text-tertiary text-xs font-medium mr-2 mb-2 px-2.5 py-1 rounded-lg">${loc.location}</span>`).join('');
    return `<div><p class="text-sm font-semibold themed-text-secondary mb-2">Grounding Evidence</p><blockquote class="themed-secondary-bg border-l-4 themed-border pl-4 py-2 rounded-r-lg mb-3"><p class="themed-text-secondary italic">"${insight.representative_snippet}"</p></blockquote><div class="flex flex-wrap">${locationsHTML}</div></div>`;
}

function createActionableRecommendationHTML(insight) { 
    return `<div class="themed-border-t pt-3"><p class="text-sm font-semibold themed-text-accent mb-2">Actionable Recommendation</p><p class="themed-text-secondary">${insight.actionable_recommendation}</p></div>`; 
}

function getSeverityStyles(severity) {
    const styles = { "Critical": "bg-red-500/20 text-red-400 border-red-500/30", "High": "bg-orange-500/20 text-orange-400 border-orange-500/30", "Medium": "bg-yellow-500/20 text-yellow-400 border-yellow-500/30", "Low": "bg-blue-500/20 text-blue-400 border-blue-500/30", "Informational": "themed-chip-bg themed-text-secondary themed-border", };
    return styles[severity] || styles["Informational"];
}

function getSeverityTooltipText(severity) {
    const descriptions = { "Critical": "Requires immediate attention.", "High": "A significant finding.", "Medium": "A noteworthy finding.", "Low": "A minor finding.", "Informational": "A general observation.", };
    return descriptions[severity] || "Severity level of this insight.";
}

function getConfidenceColor(score) { 
    if (score < 0.5) return "bg-red-500"; 
    if (score < 0.8) return "bg-yellow-500"; 
    return "bg-green-500"; 
}