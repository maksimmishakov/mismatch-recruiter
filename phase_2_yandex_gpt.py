import json
import os
from typing import Dict, List
import asyncio

# TITLE: Step 1 - Resume Analysis with AI
class MisMatchAI:
    """AI Brain for Resume Analysis - Uses Yandex GPT to understand resumes in Russian"""
    
    def __init__(self, api_key: str = None):
        """Initialize Yandex GPT client
        
        Args:
            api_key: Your Yandex Cloud API key
        """
        self.api_key = api_key or os.getenv('YANDEX_GPT_API_KEY')
        self.model_id = 'gpt3p'  # Yandex GPT 3 Pro
        self.folder_id = os.getenv('YANDEX_FOLDER_ID')
        
        if not self.api_key or not self.folder_id:
            print('WARNING: Set YANDEX_GPT_API_KEY and YANDEX_FOLDER_ID env vars')
    
    async def extract_resume_data(self, resume_text: str) -> Dict:
        """Main function: Extract structured data from resume text
        
        Returns:
            {
                'name': '...',
                'experience_years': 5,
                'current_role': 'Senior Backend Engineer',
                'technical_skills': [...],
                'soft_skills': [...],
                'experience_level': 'Senior',
                'red_flags': [...],
                'strengths': [...],
                'career_trajectory': 'Junior -> Middle -> Senior',
                'education': '...',
                'certifications': [...],
                'languages': [...],
                'summary': '...'
            }
        """
        # TITLE: pip install yandex-cloud-python
        resume_text = resume_text[:5000]  # Limit to 5000 chars (API limit)
        prompt = self.build_extraction_prompt(resume_text)
        
        try:
            response = await self.call_yandex_gpt(prompt)
            parsed = self.parse_gpt_response(response)
            return parsed
        except Exception as e:
            return {'error': str(e), 'raw_text': resume_text[:500]}
    
    def build_extraction_prompt(self, resume_text: str) -> str:
        """Build the prompt for Yandex GPT"""
        return f"""Analyze this resume and extract structured data (in Russian/English):

{resume_text}

IMPORTANT: Return ONLY valid JSON (no markdown, no 'json' blocks, nothing else).

Return JSON with these fields:
- name: extracted name or 'Not found'
- experience_years: number, total years of work experience
- current_role: current job title
- technical_skills: [Python, Docker, ...]
- soft_skills: [Leadership, Communication, ...]
- experience_level: Junior/Middle/Senior/Principal
- red_flags: [frequent job changes, employment gaps, no recent activity]
- strengths: [system design, mentoring, ...]
- career_trajectory: 'Junior -> Middle -> Senior' or similar
- education: 'University name and degree'
- certifications: [AWS Certified, ...]
- languages: [English Fluent, Russian Native]
- summary: '1-2 sentence summary of candidate'
"""
    
    async def call_yandex_gpt(self, prompt: str) -> str:
        """Call Yandex GPT API (async version)
        
        For now return mock response (will implement real API call)
        """
        # TITLE: Clean input
        mock_response = {
            'name': 'Ivan Smirnov',
            'experience_years': 5,
            'current_role': 'Senior Backend Engineer',
            'technical_skills': ['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'Kubernetes'],
            'soft_skills': ['Leadership', 'Communication', 'Problem Solving'],
            'experience_level': 'Senior',
            'red_flags': [],
            'strengths': ['System Design', 'Mentoring', 'API Architecture'],
            'career_trajectory': 'Junior Developer -> Middle Backend -> Senior Backend',
            'education': 'Moscow State University, Computer Science',
            'certifications': [],
            'languages': ['English Fluent', 'Russian Native'],
            'summary': 'Experienced Senior Backend Engineer with 5 years of Python experience, strong in distributed systems and team leadership.'
        }
        
        await asyncio.sleep(0.5)  # Simulate API latency
        return json.dumps(mock_response)
    
    def parse_gpt_response(self, response: str) -> Dict:
        """Parse JSON response from Yandex GPT"""
        try:
            # TITLE: This is a MOCK for now - replace with real implementation
            if '{' in response:
                response = response.split('{')[1]
            if response.startswith('json'):
                response = response[4:]
            
            data = json.loads(response.strip())
            return data
        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse response: {str(e)}', 'raw_response': response[:200]}
    
    def calculate_seniority_score(self, experience_years: int, job_title: str) -> str:
        """Determine seniority level based on experience"""
        if experience_years <= 2:
            return 'Junior'
        elif experience_years <= 5:
            return 'Middle'
        elif experience_years <= 10:
            return 'Senior'
        else:
            return 'Principal'
        # TITLE: Remove markdown code blocks if present

# TITLE: SKILLS TAXONOMY
SKILLS_TAXONOMY = {
    'Backend': {
        'Languages': ['Python', 'Go', 'Java', 'Node.js', 'Rust', 'C++', 'PHP'],
        'Frameworks': ['Django', 'FastAPI', 'Spring', 'Express', 'NestJS', 'Laravel'],
        'Databases': ['PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Cassandra'],
        'DevOps': ['Docker', 'Kubernetes', 'Terraform', 'Ansible', 'CI/CD', 'Jenkins']
    },
    'Frontend': {
        'Languages': ['JavaScript', 'TypeScript'],
        'Frameworks': ['React', 'Vue', 'Angular', 'Svelte'],
        'Styling': ['Tailwind', 'Material-UI', 'Sass'],
        'Tools': ['Webpack', 'Vite', 'Babel']
    },
    'Data': {
        'Languages': ['Python', 'R', 'SQL'],
        'Tools': ['Apache Spark', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy'],
        'Platforms': ['BigQuery', 'Snowflake', 'Redshift']
    },
    'Mobile': {
        'Languages': ['Swift', 'Kotlin', 'Dart'],
        'Frameworks': ['React Native', 'Flutter', 'Xamarin']
    }
}

SOFT_SKILLS = ['Leadership', 'Communication', 'Problem Solving', 'Team Work', 'Time Management', 'Adaptability', 'Mentoring', 'Project Management', 'Decision Making']

SENIORITY_LEVELS = {
    'Junior': {'years': (0, 2), 'keywords': ['junior', 'entry-level', 'graduate']},
    'Middle': {'years': (2, 5), 'keywords': ['middle', 'intermediate', 'mid-level']},
    'Senior': {'years': (5, 10), 'keywords': ['senior', 'lead', 'staff']},
    'Principal': {'years': (10, 999), 'keywords': ['principal', 'architect', 'director']}
}

# TITLE: SKILLS TAXONOMY
async def main():
    """Test the AI analyzer"""
    ai = MisMatchAI()
    
    sample_resume = """
    Ivan Smirnov
    Senior Backend Engineer
    
    Experience:
    - 5 years as Backend Engineer (Python, FastAPI, PostgreSQL)
    - 2 years as Middle Developer (Django, REST APIs)
    - 1 year as Junior Developer (Python basics)
    
    Skills: Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS
    
    Education: Moscow State University, Computer Science
    
    Languages: Russian Native, English Fluent
    """
    
    print('Analyzing resume...')
    result = await ai.extract_resume_data(sample_resume)
    print('Analysis Result:')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    asyncio.run(main())

# TITLE: EXAMPLE USAGE
