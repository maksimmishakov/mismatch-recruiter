"""ML Matching Engine for MisMatch Recruiter

Implements TF-IDF based resume-job matching with weighted scoring.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import logging

logger = logging.getLogger(__name__)

# Download NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')


class MatchingEngine:
    """ML Engine implementing TF-IDF matching with custom weights."""
    
    def __init__(self):
        """Initialize TF-IDF vectorizer and preprocessing tools."""
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            lowercase=True,
            min_df=1
        )
        self.stopwords = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        """Preprocess text for matching.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned and tokenized text
        """
        if not text:
            return ''
        
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in string.punctuation and token not in self.stopwords]
        return ' '.join(tokens)
    
    def extract_skills(self, text):
        """Extract known skills from text using NER.
        
        Args:
            text: Resume or job description text
            
        Returns:
            List of matched skills
        """
        KNOWN_SKILLS = [
            'python', 'javascript', 'java', 'c', 'c++', 'ruby', 'php', 'go', 'rust', 'typescript',
            'sql', 'html', 'css', 'react', 'vue', 'angular', 'django', 'flask', 'fastapi', 'nodejs', 'express',
            'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'docker', 'kubernetes',
            'aws', 'gcp', 'azure', 'jenkins', 'git', 'rest api', 'graphql', 'microservices',
            'devops', 'machine learning', 'data science', 'tensorflow', 'pytorch', 'scrum', 'agile',
            'leadership', 'communication', 'management'
        ]
        
        text_lower = text.lower()
        found_skills = []
        for skill in KNOWN_SKILLS:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def calculate_text_similarity(self, candidate_text, job_text):
        """Calculate TF-IDF cosine similarity between texts.
        
        Args:
            candidate_text: Candidate resume/profile text
            job_text: Job description text
            
        Returns:
            Similarity score 0.0 - 1.0
        """
        try:
            candidate_clean = self.preprocess_text(candidate_text)
            job_clean = self.preprocess_text(job_text)
            
            if not candidate_clean or not job_clean:
                return 0.0
            
            # TF-IDF vectorization
            texts = [candidate_clean, job_clean]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            
            # Cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
            return float(similarity[0][0])
        except Exception as e:
            logger.error(f'Error calculating text similarity: {e}')
            return 0.0
    
    def calculate_skills_match(self, candidate_skills, required_skills):
        """Calculate skills matching percentage.
        
        Args:
            candidate_skills: List of candidate skills
            required_skills: List of required skills
            
        Returns:
            Match percentage 0.0 - 1.0
        """
        if not required_skills:
            return 1.0
        
        candidate_set = {s.lower() for s in candidate_skills}
        required_set = {s.lower() for s in required_skills}
        
        matching = candidate_set & required_set
        match_percentage = len(matching) / len(required_set)
        
        return float(min(match_percentage, 1.0))
    
    def calculate_experience_match(self, candidate_years, required_years):
        """Calculate experience match score.
        
        Args:
            candidate_years: Candidate years of experience
            required_years: Required years of experience
            
        Returns:
            Match score 0.0 - 1.0
        """
        if not required_years or required_years == 0:
            return 1.0
        
        if candidate_years >= required_years:
            return 1.0
        
        match_score = candidate_years / required_years
        return float(min(match_score, 1.0))
    
    def calculate_location_match(self, candidate_location, job_location, remote=False):
        """Calculate location match score.
        
        Args:
            candidate_location: Candidate location
            job_location: Job location
            remote: Whether job is remote
            
        Returns:
            Match score 0.0 - 1.0
        """
        if not job_location:
            return 1.0
        
        if remote or candidate_location.lower() == job_location.lower():
            return 1.0
        
        # Remote score for location mismatch
        return 0.5
    
    def calculate_salary_fit(self, candidate_salary_expectation, offered_salary):
        """Calculate salary compatibility.
        
        Args:
            candidate_salary_expectation: Candidate expected salary
            offered_salary: Job offered salary
            
        Returns:
            Match score 0.0 - 1.0
        """
        if not offered_salary or not candidate_salary_expectation:
            return 0.8  # Neutral score
        
        if offered_salary >= candidate_salary_expectation:
            return 1.0  # Perfect coverage
        
        coverage = offered_salary / candidate_salary_expectation
        # Score >= 70% coverage
        if coverage >= 0.7:
            return coverage
        
        return float(coverage * 0.7)  # Max 0.49
    
    def calculate_match_score(self, candidate, job, weights=None):
        """Calculate overall match score.
        
        Args:
            candidate: Dict with candidate data
            job: Dict with job data
            weights: Dict with scoring weights
            
        Returns:
            Dict with overall score and breakdown
        """
        if weights is None:
            weights = {
                'skills': 0.40,
                'experience': 0.30,
                'location': 0.15,
                'salary': 0.10,
                'text_similarity': 0.05
            }
        
        try:
            # 1. Skills (40%)
            candidate_skills = candidate.get('skills', [])
            required_skills = job.get('required_skills', [])
            skills_score = self.calculate_skills_match(candidate_skills, required_skills)
            
            # 2. Experience (30%)
            candidate_experience = candidate.get('experience_years', 0)
            required_experience = job.get('required_experience', 0)
            experience_score = self.calculate_experience_match(candidate_experience, required_experience)
            
            # 3. Location (15%)
            candidate_location = candidate.get('location', '')
            job_location = job.get('location', '')
            job_remote = job.get('remote', False)
            location_score = self.calculate_location_match(candidate_location, job_location, job_remote)
            
            # 4. Salary (10%)
            candidate_salary = candidate.get('salary_expectation', 0)
            job_salary = job.get('salary', 0)
            salary_score = self.calculate_salary_fit(candidate_salary, job_salary)
            
            # 5. Text similarity (5%)
            candidate_text = candidate.get('resume_text', '')
            job_text = job.get('description', '')
            text_similarity = self.calculate_text_similarity(candidate_text, job_text)
            
            # Calculate overall score
            overall_score = (
                skills_score * weights['skills'] +
                experience_score * weights['experience'] +
                location_score * weights['location'] +
                salary_score * weights['salary'] +
                text_similarity * weights['text_similarity']
            )
            
            return {
                'overall_score': float(overall_score),
                'score_percentage': float(overall_score * 100),
                'breakdown': {
                    'skills': {
                        'score': float(skills_score),
                        'weight': weights['skills'],
                        'matched_count': len(set(candidate_skills) & set(required_skills)),
                        'required_count': len(set(required_skills))
                    },
                    'experience': {
                        'score': float(experience_score),
                        'weight': weights['experience'],
                        'candidate_years': candidate_experience,
                        'required_years': required_experience
                    },
                    'location': {
                        'score': float(location_score),
                        'weight': weights['location'],
                        'candidate_location': candidate_location,
                        'job_location': job_location,
                        'remote': job_remote
                    },
                    'salary': {
                        'score': float(salary_score),
                        'weight': weights['salary'],
                        'candidate_expectation': candidate_salary,
                        'offered_salary': job_salary
                    },
                    'text_similarity': {
                        'score': float(text_similarity),
                        'weight': weights['text_similarity']
                    }
                },
                'match_quality': self.determine_quality(overall_score),
                'recommendations': self.generate_recommendations(candidate, job, overall_score)
            }
        except Exception as e:
            logger.error(f'Error calculating match score: {e}')
            return {
                'overall_score': 0.0,
                'score_percentage': 0.0,
                'error': str(e)
            }
    
    def determine_quality(self, score):
        """Determine match quality based on score.
        
        Args:
            score: Overall match score
            
        Returns:
            Quality level
        """
        if score >= 0.85:
            return 'EXCELLENT'
        elif score >= 0.70:
            return 'GOOD'
        elif score >= 0.50:
            return 'FAIR'
        elif score >= 0.30:
            return 'POOR'
        else:
            return 'UNSUITABLE'
    
    def generate_recommendations(self, candidate, job, score):
        """Generate recommendations for improvement.
        
        Args:
            candidate: Candidate data
            job: Job data
            score: Overall match score
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Skills gap
        candidate_skills = set(candidate.get('skills', []))
        required_skills = set(job.get('required_skills', []))
        missing_skills = required_skills - candidate_skills
        
        if missing_skills and score < 0.9:
            recommendations.append({
                'type': 'SKILLS',
                'message': f'Missing skills: {", ".join(missing_skills)}',
                'action': 'Consider learning or training in these areas'
            })
        
        # Experience gap
        candidate_exp = candidate.get('experience_years', 0)
        required_exp = job.get('required_experience', 0)
        if candidate_exp < required_exp:
            gap = required_exp - candidate_exp
            recommendations.append({
                'type': 'EXPERIENCE',
                'message': f'Need {gap} more years of experience',
                'action': 'Gain practical experience or find similar roles'
            })
        
        # Location mismatch
        if not job.get('remote', False):
            if candidate.get('location', '').lower() != job.get('location', '').lower():
                recommendations.append({
                    'type': 'LOCATION',
                    'message': f'Location mismatch: {candidate.get("location")} vs {job.get("location")}',
                    'action': 'Consider relocation or ask about remote options'
                })
        
        return recommendations


# Singleton instance
matcher = None

def get_matcher():
    """Get singleton instance of MatchingEngine."""
    global matcher
    if matcher is None:
        matcher = MatchingEngine()
    return matcher
