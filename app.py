from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello! RankPO is running!</h1>'

@app.route('/api/status')
def status():
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
