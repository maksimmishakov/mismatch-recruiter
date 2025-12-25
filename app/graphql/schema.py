"""GraphQL schema with queries and mutations."""

import graphene
from app.graphql.types import UserType, ResumeType, JobType, MatchType, PredictionType, SubscriptionType
from app.models import User, Resume, Job, Match, Prediction, Subscription
from app.database import SessionLocal
from app.logger import get_logger

logger = get_logger("graphql")


class Query(graphene.ObjectType):
    """GraphQL root query."""
    
    # User queries
    user = graphene.Field(UserType, user_id=graphene.Int(required=True))
    users = graphene.List(UserType, limit=graphene.Int(default_value=100), offset=graphene.Int(default_value=0))
    
    # Resume queries
    resume = graphene.Field(ResumeType, resume_id=graphene.Int(required=True))
    user_resumes = graphene.List(ResumeType, user_id=graphene.Int(required=True))
    
    # Job queries
    job = graphene.Field(JobType, job_id=graphene.Int(required=True))
    search_jobs = graphene.List(JobType, title=graphene.String(), location=graphene.String(), limit=graphene.Int(default_value=50))
    
    # Match queries
    match = graphene.Field(MatchType, match_id=graphene.Int(required=True))
    matches_for_resume = graphene.List(MatchType, resume_id=graphene.Int(required=True), min_score=graphene.Float(default_value=0.6))
    
    def resolve_user(self, info, user_id):
        try:
            db = SessionLocal()
            user = db.query(User).filter(User.id == user_id).first()
            db.close()
            return user
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def resolve_users(self, info, limit=100, offset=0):
        try:
            db = SessionLocal()
            users = db.query(User).limit(limit).offset(offset).all()
            db.close()
            return users
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def resolve_resume(self, info, resume_id):
        try:
            db = SessionLocal()
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            db.close()
            return resume
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def resolve_user_resumes(self, info, user_id):
        try:
            db = SessionLocal()
            resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
            db.close()
            return resumes
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def resolve_job(self, info, job_id):
        try:
            db = SessionLocal()
            job = db.query(Job).filter(Job.id == job_id).first()
            db.close()
            return job
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def resolve_search_jobs(self, info, title=None, location=None, limit=50):
        try:
            db = SessionLocal()
            query = db.query(Job)
            if title:
                query = query.filter(Job.title.ilike(f"%{title}%"))
            if location:
                query = query.filter(Job.location.ilike(f"%{location}%"))
            jobs = query.limit(limit).all()
            db.close()
            return jobs
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def resolve_match(self, info, match_id):
        try:
            db = SessionLocal()
            match = db.query(Match).filter(Match.id == match_id).first()
            db.close()
            return match
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def resolve_matches_for_resume(self, info, resume_id, min_score=0.6):
        try:
            db = SessionLocal()
            matches = db.query(Match).filter(Match.resume_id == resume_id, Match.match_score >= min_score).order_by(Match.match_score.desc()).all()
            db.close()
            return matches
        except Exception as e:
            logger.error(f"Error: {e}")
            return []


class CreateUserMutation(graphene.Mutation):
    """Create user mutation."""
    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        password = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    user_id = graphene.Int()
    
    @staticmethod
    def mutate(root, info, email, name, password):
        try:
            db = SessionLocal()
            user = User(email=email, name=name, password=password)
            db.add(user)
            db.commit()
            user_id = user.id
            db.close()
            return CreateUserMutation(success=True, message="User created", user_id=user_id)
        except Exception as e:
            logger.error(f"Error: {e}")
            return CreateUserMutation(success=False, message=str(e))


class CreateMatchMutation(graphene.Mutation):
    """Create match mutation."""
    class Arguments:
        resume_id = graphene.Int(required=True)
        job_id = graphene.Int(required=True)
        match_score = graphene.Float(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    match_id = graphene.Int()
    
    @staticmethod
    def mutate(root, info, resume_id, job_id, match_score):
        try:
            db = SessionLocal()
            match = Match(resume_id=resume_id, job_id=job_id, match_score=match_score, status="active")
            db.add(match)
            db.commit()
            match_id = match.id
            db.close()
            return CreateMatchMutation(success=True, message="Match created", match_id=match_id)
        except Exception as e:
            logger.error(f"Error: {e}")
            return CreateMatchMutation(success=False, message=str(e))


class Mutation(graphene.ObjectType):
    """GraphQL mutations."""
    create_user = CreateUserMutation.Field()
    create_match = CreateMatchMutation.Field()


# Create GraphQL schema
schema = graphene.Schema(query=Query, mutation=Mutation)
