from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pdfplumber
import io
import requests

app = FastAPI()

# GitHub HTML URL
GITHUB_HTML_URL = "https://raw.githubusercontent.com/maksimmishakov/lamoda-ai-recruiter/master/templates/index.html"

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve index.html from GitHub"""
    try:
        response = requests.get(GITHUB_HTML_URL)
        return response.text
    except:
        return "<h1>Error loading page</h1>"

@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """Upload & analyze resume from PDF"""
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files allowed"}
    
    try:
        contents = await file.read()
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        return {
            "status": "success",
            "filename": file.filename,
            "pages": len(pdf.pages),
            "text": text[:1000]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
