import joblib
from sklearn.preprocessing import StandardScaler

class SalaryPredictor:
    def __init__(self):
        # Load pre-trained model (обучить на реальных данных)
        self.model = joblib.load('models/salary_model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
    
    def predict(self, resume_data, location='Russia'):
        """Predict salary based on skills, experience, location"""
        
        features = self._extract_features(resume_data)
        scaled_features = self.scaler.transform([features])
        
        salary = self.model.predict(scaled_features)[0]
        confidence = self.model.predict_proba(scaled_features).max()
        
        return {
            "expected_salary": int(salary),
            "range_min": int(salary * 0.8),
            "range_max": int(salary * 1.2),
            "currency": "RUB" if location == "Russia" else "USD",
            "confidence": round(confidence * 100),
            "market_percentile": self._get_percentile(salary)
        }
    
    def _extract_features(self, resume_data):
        """Convert resume data to ML features"""
        # Years of experience
        exp = resume_data.get('years_experience', 0)
        
        # Skill premiums
        skill_premium = 0
        premium_skills = {
            'Python': 50000, 'Go': 60000, 'Rust': 70000,
            'Kubernetes': 40000, 'AWS': 35000
        }
        for skill in resume_data.get('skills', []):
            skill_premium += premium_skills.get(skill, 0)
        
        # Education bonus
        edu_bonus = 15000 if 'degree' in resume_data else 0
        
        # Stability multiplier
        stability = 1.0 if resume_data.get('job_changes', 0) < 3 else 0.85
        
        return [exp, skill_premium, edu_bonus, stability]
    
    def _get_percentile(self, salary):
        """Calculate market percentile (placeholder)"""
        return 50
