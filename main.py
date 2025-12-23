import json
import requests
import os
from dotenv import load_dotenv
import logging
from flask import Flask, request, jsonify
import pdfplumber
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

class RecruitmentAIFunction:
    def __init__(self):
        self.giga_api_key = os.getenv("YANDEX_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        logger.info("✅ AI Recruitment Function initialized")
    
    def parse_resume(self, resume_text: str) -> dict:
        """Parsing resume - simplified version"""
        logger.info("Parsing resume...")
        return {
            "name": "Maxim Ivanov",
            "hard_skills": ["Go", "Python", "Kubernetes", "Docker", "PostgreSQL"],
            "experience_years": 7,
            "status": "parsed"
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def send_telegram(self, chat_id: str, message: str) -> dict:
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Message sent")
                return {"status": "SENT", "message_id": response.json()['result']['message_id']}
            else:
                return {"status": "FAILED", "error": response.text}
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}

recruiter = RecruitmentAIFunction()

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """Phase 1: Handle resume upload and analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are accepted"}), 400
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Extract text from PDF
            resume_text = recruiter.extract_text_from_pdf(tmp_path)
            
            if not resume_text:
                return jsonify({"error": "Could not extract text from PDF"}), 400
            
            # Parse resume
            parsed_data = recruiter.parse_resume(resume_text)
            
            return jsonify({
                "status": "success",
                "filename": file.filename,
                "parsed_data": parsed_data,
                "text_length": len(resume_text)
            }), 200
        
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        logger.error(f"Error in analyze_resume: {str(e)}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
