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

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
=======
>>>>>>> bf92ef7458baa6e02f8b2d24df29d304c808207c
