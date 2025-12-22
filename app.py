from flask import Flask, jsonify, request, render_template_string
import json
import os
from datetime import datetime
import subprocess

app = Flask(__name__)

CONFIG_PATH = "config.json"
CANDIDATES_PATH = "candidates_ai_scored.json"
LETTERS_PATH = "letter_drafts.txt"

def load_config():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except:
        return {"status": "config_error"}

@app.route('/')
def dashboard():
    """Main dashboard"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI Recruiter Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            header { color: white; text-align: center; margin-bottom: 40px; padding: 40px 0; }
            header h1 { font-size: 48px; margin-bottom: 10px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s;
            }
            .card:hover { transform: translateY(-5px); }
            .card h2 { color: #333; margin-bottom: 15px; font-size: 24px; }
            .number { font-size: 42px; color: #667eea; font-weight: bold; }
            .label { color: #999; font-size: 14px; margin-top: 10px; }
            .btn {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 15px 30px;
                border-radius: 8px;
                border: none;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
                text-decoration: none;
            }
            .btn:hover { background: #5568d3; }
            .status-online { color: #2ecc71; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🤖 AI Recruiter for Lamoda</h1>
                <p>Automated talent acquisition with AI</p>
            </header>
            
            <div class="grid">
                <div class="card">
                    <h2>📊 Candidates</h2>
                    <div class="number" id="candidates">0</div>
                    <div class="label">Ready to contact</div>
                </div>
                
                <div class="card">
                    <h2>💰 Monthly Bonus</h2>
                    <div class="number" id="bonus">0₽</div>
                    <div class="label">50% realistic (50% will pass)</div>
                </div>
                
                <div class="card">
                    <h2>📈 Annual Income</h2>
                    <div class="number" id="annual">0M₽</div>
                    <div class="label">Passive income potential</div>
                </div>
                
                <div class="card">
                    <h2>🔄 System Status</h2>
                    <div style="font-size: 20px; margin-top: 10px;">
                        <span class="status-online">● Online</span>
                    </div>
                    <div class="label">24/7 Active</div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <button class="btn" onclick="refreshData()">🔄 Refresh</button>
                <a href="/api/candidates" class="btn">📋 View All</a>
            </div>
        </div>
        
        <script>
            async function loadData() {
                try {
                    const res = await fetch('/api/metrics');
                    const data = await res.json();
                    
                    document.getElementById('candidates').textContent = data.total_candidates;
                    document.getElementById('bonus').textContent = (data.monthly_bonus / 1000).toFixed(0) + 'k₽';
                    document.getElementById('annual').textContent = (data.annual_bonus / 1000000).toFixed(1) + 'M₽';
                } catch (e) {
                    console.error(e);
                }
            }
            
            function refreshData() {
                loadData();
            }
            
            loadData();
            setInterval(loadData, 60000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "service": "AI Recruitment Bot for Lamoda",
        "version": "1.0",
        "uptime": "24/7"
    })

@app.route('/api/metrics')
def metrics():
    candidates_count = 0
    if os.path.exists(CANDIDATES_PATH):
        try:
            with open(CANDIDATES_PATH) as f:
                data = json.load(f)
                candidates_count = len(data) if isinstance(data, list) else 0
        except:
            pass
    
    return jsonify({
        "total_candidates": candidates_count,
        "monthly_bonus": candidates_count * 120000 * 0.5,
        "annual_bonus": candidates_count * 120000 * 0.5 * 12,
        "avg_score": 70,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/candidates')
def get_candidates():
    if os.path.exists(CANDIDATES_PATH):
        try:
            with open(CANDIDATES_PATH) as f:
                candidates = json.load(f)
                return jsonify({
                    "count": len(candidates) if isinstance(candidates, list) else 0,
                    "candidates": candidates
                })
        except:
            pass
    
    return jsonify({"count": 0, "candidates": []})

@app.route('/api/letters')
def get_letters():
    if os.path.exists(LETTERS_PATH):
        try:
            with open(LETTERS_PATH, 'r', encoding='utf-8') as f:
                letters = f.read()
                return jsonify({
                    "status": "success",
                    "letters": letters
                })
        except:
            pass
    
    return jsonify({"status": "error", "message": "No letters found"})

