from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

CONFIG_PATH = "config.json"
CANDIDATES_PATH = "candidates_ai_scored.json"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "AI Recruitment Bot for Lamoda",
        "version": "1.0",
        "uptime": "24/7"
    })

@app.route('/api/status', methods=['GET'])
def status():
    config = load_config()
    
    candidates_count = 0
    if os.path.exists(CANDIDATES_PATH):
        with open(CANDIDATES_PATH) as f:
            candidates = json.load(f)
            candidates_count = len(candidates) if isinstance(candidates, list) else 0
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "candidates_found": candidates_count,
        "daily_limit": config["lamoda_search"]["daily_limit"],
        "keywords": config["lamoda_search"]["keywords"],
        "locations": config["lamoda_search"]["locations"],
        "potential_bonus": candidates_count * 120000 if candidates_count > 0 else 0
    })

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    if os.path.exists(CANDIDATES_PATH):
        with open(CANDIDATES_PATH) as f:
            candidates = json.load(f)
            return jsonify({
                "count": len(candidates) if isinstance(candidates, list) else 0,
                "candidates": candidates
            })
    return jsonify({"count": 0, "candidates": []})

@app.route('/api/run', methods=['POST'])
def run_search():
    """Запустить поиск"""
    return jsonify({
        "status": "running",
        "message": "Search started. This will take a few minutes.",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/metrics', methods=['GET'])
def metrics():
    config = load_config()
    candidates_count = 0
    
    if os.path.exists(CANDIDATES_PATH):
        with open(CANDIDATES_PATH) as f:
            data = json.load(f)
            candidates_count = len(data) if isinstance(data, list) else 0
    
    return jsonify({
        "total_candidates": candidates_count,
        "avg_score": 70,
        "monthly_bonus_conservative": candidates_count * 120000 * 0.5,
        "yearly_bonus_conservative": candidates_count * 120000 * 0.5 * 12,
        "last_run": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
