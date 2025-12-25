"""Interview Questions Generator Service"""
import json
import os
from openai import OpenAI

class InterviewGenerator:
    """Generate personalized interview questions using GPT-4o-mini"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.client = OpenAI(api_key=api_key)
    
    def generate_questions(self, resume_data, job_description):
        """Generate 10 personalized interview questions
        
        Args:
            resume_data: dict with candidate info (years_experience, skills, etc.)
            job_description: dict with job details (title, description)
        
        Returns:
            dict with questions, total count, success status
        """
        
        prompt = f"""
        You are an experienced HR recruiter. Generate 10 interview questions:
        - 3 easy (warm-up questions)
        - 4 medium (technical/skills questions)
        - 3 hard (critical thinking questions)
        
        POSITION: {job_description.get('title', 'Unknown Position')}
        REQUIREMENTS: {job_description.get('description', 'Not specified')}
        CANDIDATE EXPERIENCE: {resume_data.get('years_experience', 0)} years
        CANDIDATE SKILLS: {', '.join(resume_data.get('skills', []))}
        
        Return ONLY a JSON array with objects containing:
        - question: the interview question
        - difficulty: 'easy', 'medium', or 'hard'
        - category: skill category being tested
        - expected_answer_hint: brief hint of what to look for
        
        Return ONLY valid JSON, no other text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content
            questions = json.loads(response_text)
            
            return {
                "success": True,
                "questions": questions,
                "total": len(questions),
                "resume_id": resume_data.get('id')
            }
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse interview questions: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Interview generation failed: {str(e)}"
            }
