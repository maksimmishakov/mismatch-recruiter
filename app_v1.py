from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': '✅ MisMatch API OK'}), 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    candidates = [
        {'id': 1, 'name': 'Ivan Petrov', 'skills': ['Python', 'JavaScript'], 'match_score': 85},
        {'id': 2, 'name': 'Maria Smirnova', 'skills': ['Java', 'Python'], 'match_score': 78},
    ]
    return jsonify({'status': 'ok', 'data': candidates}), 200

@app.route('/api/job-profiles', methods=['GET'])
def get_job_profiles():
    jobs = [
        {'id': 1, 'title': 'Senior Python Developer', 'required_skills': ['Python', 'Django'], 'salary_range': '100000-150000'},
        {'id': 2, 'title': 'Full Stack Developer', 'required_skills': ['JavaScript', 'React', 'Node.js'], 'salary_range': '80000-120000'},
    ]
    return jsonify({'status': 'ok', 'data': jobs}), 200

@app.route('/api/job-profiles', methods=['POST'])
def create_job_profile():
    data = request.get_json()
    new_job = {
        'id': 3,
        'title': data.get('job_title'),
        'required_skills': data.get('required_skills', '').split(','),
        'salary_range': data.get('salary_range'),
        'description': data.get('description')
    }
    return jsonify({'status': 'ok', 'message': 'Job profile created', 'data': new_job}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
