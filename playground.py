import requests


API_URL = "http://localhost:8000/api/v1/analyze-document"
API_KEY = "your_api_key_here"


def analyze_document(file_path: str, model_name: str):
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        data = {"model_name": model_name}
        headers = {"Authorization": f"Bearer {API_KEY}"}

        response = requests.post(API_URL, files=files, data=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)
            return None


if __name__ == "__main__":
    report = analyze_document("path/to/file.pdf", "google:gemini-2.5-flash")
    print(report)