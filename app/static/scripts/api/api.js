const API_ENDPOINTS = {
    getModels: "/api/v1/get-available-models",
    analyze: "/api/v1/analyze-document",
};

export async function fetchModels() {
    const response = await fetch(API_ENDPOINTS.getModels);
    if (!response.ok) throw new Error(`Server responded with status: ${response.status}`);
    return await response.json();
}

export async function performAnalysis(apiKey, file, model, signal) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("model_name", model);

    const response = await fetch(API_ENDPOINTS.analyze, { 
        method: "POST", 
        headers: { "Authorization": `Bearer ${apiKey}` }, 
        body: formData, 
        signal: signal 
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: `HTTP error! Status: ${response.status}` }));
        throw new Error(errorData.detail);
    }
    return await response.json();
}