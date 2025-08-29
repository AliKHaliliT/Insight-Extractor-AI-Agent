# Insight Extractor AI Agent
<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px;">
    <img src="https://img.shields.io/github/license/AliKHaliliT/Insight-Extractor-AI-Agent" alt="License">
    <img src="https://img.shields.io/github/last-commit/AliKHaliliT/Insight-Extractor-AI-Agent" alt="Last Commit">
    <img src="https://img.shields.io/github/issues/AliKHaliliT/Insight-Extractor-AI-Agent" alt="Open Issues">
</div>
<br/>

The **Insight Extractor AI Agent** is a model-agnostic document analysis system featuring:

- A **FastAPI** backend powered by the `pydantic-ai` framework.  
- A modern **HTML, CSS, and vanilla JavaScript UI**.  
- Support for multiple **LLM providers** (OpenAI, Anthropic, Google, etc.).  

It allows you to extract structured insights from documents of various formats. Insights are returned as consistent JSON `AnalysisReport` (`insight_extractor_ai_agent/schemas/analysis_report.py`) objects, containing thematic, code, quantitative, sentiment, and table insights.

### 👉 A working demo is available [here](https://insight-extractor-ai-agent.onrender.com/).

The demo is hosted on a hobby plan at Render.com. Free instances go to sleep after periods of inactivity, which can cause the first request to take up to 50 seconds or more. If the site feels unresponsive at first, please allow a little extra time for it to wake up.

To conserve free credits, requests are rate-limited to 1 per minute, 60 per hour, and 100 per day.

> ⚡ The quality, accuracy, and speed of analysis depend on the model you choose. For best results, use models with high context windows and reasoning capabilities (preferably adaptive reasoning).  
> 📂 Documents of any size are supported from the project side. However, your model must be able to handle them.  
> 📄 Currently, the agent is set to retry up to three times if it fails to generate a structured insight output. If it still cannot produce a proper response after three attempts, it will throw an error. Therefore, if an analysis takes longer than usual, it likely indicates that the model encountered a failure and the retry mechanism was triggered. This can occur for various reasons, including limitations in the model’s capabilities or the way the random seed was initialized for that specific session.

### You can explore output schemas in `insight_extractor_ai_agent/schemas` or view them [here](https://alikhalilit.github.io/Insight-Extractor-AI-Agent/).

**If using Gemini, you can get a free API key from [Google AI Studio](https://aistudio.google.com/).**

---

## Features

- **Model-Agnostic**: Swap models or providers without code changes.  
- **Versatile File Support**: Works with  
  - `.txt`, `.md`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.html`, `.xml`, `.py`, `.js`  
  - Extendable for more formats.  
- **Structured JSON Output**: Unified `AnalysisReport` format.  
- **Modern UI**: Lightweight web interface for uploads and results.  
- **Secure Backend**: Includes CORS, CSP, and XSS protection.  
- **Rate Limiting**: Configurable global limits, with optional Redis support.  
- **Async Architecture**: End-to-end asynchronous for maximum performance.  
- **Configurable**: Environment-based setup.  

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/AliKHaliliT/Insight-Extractor-AI-Agent.git
   cd Insight-Extractor-AI-Agent
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**

   Add configuration (or edit `app/core/config/settings.py`). You can also continue with the default values.

4. **Run the application and access the UI at `http://127.0.0.1:8000`.**

   ```bash
   uvicorn main:app --reload
   ```

**Use `http://127.0.0.1:8000/api/v1/docs` or `http://127.0.0.1:8000/api/v1/redoc` for documentation. You can also check the documentation at [here(docs)](https://alikhalilit.github.io/Insight-Extractor-AI-Agent/api/v1/docs) or [here(redoc)](https://alikhalilit.github.io/Insight-Extractor-AI-Agent/api/v1/redoc).**

---

## Configuration

Use a `.env` file to configure the application.

| Variable              | Description                    | Default                               |
| --------------------- | ------------------------------ | ------------------------------------- |
| `PROJECT_NAME`        | Name of the project            | `Insight Extractor AI Agent`          |
| `PROJECT_DESCRIPTION` | Short description              | `A backend service...`                |
| `VERSION`             | Version                        | `0.1.0`                               |
| `HANDLER_LOG_LEVEL`   | Log level for app handlers     | `DEBUG`                               |
| `ROOT_LOG_LEVEL`      | Log level for root logger      | `INFO`                                |
| `UVICORN_LOG_LEVEL`   | Log level for Uvicorn server   | `INFO`                                |
| `API_V1_PREFIX`       | API v1 prefix                  | `/api/v1`                             |
| `CORS_ORIGINS`        | Allowed CORS origins           | `["*"]`                               |
| `RATE_LIMITS`         | API rate limits                | `["1/minute", "60/hour", "100/day"]` |
| `USE_REDIS`           | Enable Redis for rate limiting | `False`                               |
| `REDIS_URL`           | Redis instance URL             | `None`                                |
| `STORAGE_TYPE`        | Storage type                   | `local`                               |

---

## Usage

### 1. Web UI

* Upload documents and generate reports.
* Download results as raw JSON or styled HTML.
* Re-upload existing JSON reports to visualize without re-analysis.

### 2. API

#### Get Available Models

```http
GET /api/v1/get-available-models
```

#### Analyze a Document

```http
POST /api/v1/analyze-document
```

**Parameters**

* `file`: Document to analyze.
* `model_name`: Model in `provider:model` format (e.g., `openai:gpt-4o`).
* `Authorization: Bearer <API_KEY>` in headers.

**Example (`curl`):**

```bash
curl -X POST "http://localhost:8000/api/v1/analyze-document" \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -F "file=@/path/to/your/document.pdf" \
  -F "model_name=<MODEL_NAME>"
```

For a Python example, see the `playground` file.

---

## Dependencies

* FastAPI
* Uvicorn
* Pydantic-AI
* Pandas
* PyMuPDF (PDF)
* python-docx (Word)
* BeautifulSoup4 (HTML/XML)
* SlowAPI (rate limiting)

See `requirements.txt` for the full list.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.