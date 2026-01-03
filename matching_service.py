class AdvancedMatchingEngine:
    """
    GemNet2-style matching engine for candidate-to-job pairing
    """
    
    def __init__(self):
        self.weights = {
            'skills': 0.35,
            'experience': 0.25,
            'salary': 0.20,
            'location': 0.10,
            'education': 0.10
        }
    
    def calculate_skills_match(self, candidate_skills, required_skills):
        """
        Calculate skills match percentage (0-100)
        """
        if not required_skills:
            return 100
        
        candidate_set = set(candidate_skills or [])
        required_set = set(required_skills)
        
        if not required_set:
            return 100
        
        matched = len(candidate_set.intersection(required_set))
        match_score = (matched / len(required_set)) * 100
        return min(100, match_score)
    
    def calculate_experience_match(self, candidate_years, min_years, max_years):
        """
        Calculate experience match percentage (0-100)
        """
        if not min_years:
            return 100
        
        if candidate_years < min_years:
            return (candidate_years / min_years) * 100
        elif candidate_years > max_years:
            return 90  # Overqualified
        else:
            return 100  # Perfect match
    
    def calculate_salary_match(self, candidate_min, candidate_max, job_min, job_max):
        """
        Calculate salary compatibility (0-100)
        """
        if not job_min:
            return 100
        
        # Check if ranges overlap
        if candidate_max < job_min or candidate_min > job_max:
            return 30  # No overlap, poor match
        
        overlap_start = max(candidate_min, job_min)
        overlap_end = min(candidate_max, job_max)
        overlap = overlap_end - overlap_start
        
        total_range = (job_max - job_min) + (candidate_max - candidate_min)
        compatibility = (overlap / total_range) * 100 if total_range > 0 else 100
        return min(100, compatibility)
    
    def calculate_location_match(self, candidate_open_remote, job_remote):
        """
        Calculate location/remote compatibility (0-100)
        """
        if job_remote == 'remote':
            return 100
        if candidate_open_remote:
            return 100 if job_remote == 'hybrid' else 85
        return 50
    
    def calculate_comprehensive_match(self, candidate, job):
        """
        Calculate overall match score (0-100) using weighted algorithm
        """
        skills = self.calculate_skills_match(
            candidate.get('skills', []),
            job.get('required_skills', [])
        )
        
        experience = self.calculate_experience_match(
            candidate.get('experience_years', 0),
            job.get('min_experience', 0),
            job.get('max_experience', 20)
        )
        
        salary = self.calculate_salary_match(
            candidate.get('salary_min', 0),
            candidate.get('salary_max', 100000),
            job.get('salary_min', 0),
            job.get('salary_max', 200000)
        )
        
        location = self.calculate_location_match(
            candidate.get('open_remote', True),
            job.get('remote_type', 'onsite')
        )
        
        education = 100  # Simplified for now
        
        total_score = (
            skills * self.weights['skills'] +
            experience * self.weights['experience'] +
            salary * self.weights['salary'] +
            location * self.weights['location'] +
            education * self.weights['education']
        )
        
        return {
            'total_score': round(total_score, 2),
            'skills_score': round(skills, 2),
            'experience_score': round(experience, 2),
            'salary_score': round(salary, 2),
            'location_score': round(location, 2),
            'education_score': round(education, 2),
            'breakdown': {
                'skills': f"{skills:.1f}% (weight: {self.weights['skills']*100}%)",
                'experience': f"{experience:.1f}% (weight: {self.weights['experience']*100}%)",
                'salary': f"{salary:.1f}% (weight: {self.weights['salary']*100}%)",
                'location': f"{location:.1f}% (weight: {self.weights['location']*100}%)",
                'education': f"{education:.1f}% (weight: {self.weights['education']*100}%)"
            }
        }

