"""Database models for resume storage and job matching."""
from datetime import datetime
import json

class ResumeRecord:
    """Model for storing resume information."""
    
    def __init__(self, candidate_id, name, email, phone, position, skills, experience, education, file_path=None):
        self.candidate_id = candidate_id
        self.name = name
        self.email = email
        self.phone = phone
        self.position = position
        self.skills = skills if isinstance(skills, list) else []
        self.experience = experience
        self.education = education
        self.file_path = file_path
        self.date_added = datetime.utcnow().isoformat()
        self.versions = []
        self.match_history = []
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'candidate_id': self.candidate_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position,
            'skills': self.skills,
            'experience': self.experience,
            'education': self.education,
            'file_path': self.file_path,
            'date_added': self.date_added,
            'versions': self.versions,
            'match_history': self.match_history
        }

class JobMatch:
    """Model for recording resume-to-job matches."""
    
    def __init__(self, candidate_id, job_id, job_title, match_score, match_status='pending'):
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.job_title = job_title
        self.match_score = match_score
        self.match_status = match_status
        self.date_matched = datetime.utcnow().isoformat()
        self.notes = []
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'job_title': self.job_title,
            'match_score': self.match_score,
            'match_status': self.match_status,
            'date_matched': self.date_matched,
            'notes': self.notes
        }

class ResumeDatabase:
    """Simple file-based resume database."""
    
    def __init__(self, data_file='resumes.json'):
        self.data_file = data_file
        self.resumes = {}
        self.matches = {}
        self.load_from_file()
    
    def load_from_file(self):
        """Load data from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.resumes = data.get('resumes', {})
                self.matches = data.get('matches', {})
        except FileNotFoundError:
            self.resumes = {}
            self.matches = {}
    
    def save_to_file(self):
        """Save data to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump({
                    'resumes': self.resumes,
                    'matches': self.matches
                }, f, indent=2)
        except Exception as e:
            print(f'Error saving to file: {e}')
    
    def add_resume(self, resume):
        """Add resume to database."""
        self.resumes[str(resume.candidate_id)] = resume.to_dict()
        self.save_to_file()
        return {'success': True, 'candidate_id': resume.candidate_id}
    
    def get_resume(self, candidate_id):
        """Get resume by candidate ID."""
        return self.resumes.get(str(candidate_id))
    
    def search_resumes(self, query):
        """Full-text search resumes."""
        results = []
        query_lower = query.lower()
        for resume_id, resume in self.resumes.items():
            if (query_lower in resume.get('name', '').lower() or
                query_lower in resume.get('position', '').lower() or
                any(query_lower in skill.lower() for skill in resume.get('skills', []))):
                results.append(resume)
        return results
    
    def record_match(self, match):
        """Record a job match."""
        match_id = f"{match.candidate_id}_{match.job_id}"
        self.matches[match_id] = match.to_dict()
        self.save_to_file()
        return {'success': True, 'match_id': match_id}
    
    def get_match_history(self, candidate_id):
        """Get all matches for a candidate."""
        results = []
        for match_id, match in self.matches.items():
            if str(match['candidate_id']) == str(candidate_id):
                results.append(match)
        return results
    
    def get_all_resumes(self):
        """Get all resumes in database."""
        return list(self.resumes.values())
