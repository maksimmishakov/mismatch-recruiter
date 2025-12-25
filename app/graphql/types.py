"""GraphQL type definitions."""

import graphene
from datetime import datetime


class UserType(graphene.ObjectType):
    """GraphQL type for User."""
    id = graphene.Int()
    email = graphene.String()
    name = graphene.String()
    role = graphene.String()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    class Meta:
        name = "User"


class ResumeType(graphene.ObjectType):
    """GraphQL type for Resume."""
    id = graphene.Int()
    user_id = graphene.Int()
    filename = graphene.String()
    parsed_text = graphene.String()
    raw_text = graphene.String()
    embedding = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    class Meta:
        name = "Resume"


class JobType(graphene.ObjectType):
    """GraphQL type for Job."""
    id = graphene.Int()
    company_id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    requirements = graphene.String()
    salary_min = graphene.Float()
    salary_max = graphene.Float()
    location = graphene.String()
    url = graphene.String()
    source = graphene.String()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    class Meta:
        name = "Job"


class MatchType(graphene.ObjectType):
    """GraphQL type for Match."""
    id = graphene.Int()
    resume_id = graphene.Int()
    job_id = graphene.Int()
    match_score = graphene.Float()
    status = graphene.String()
    match_details = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    class Meta:
        name = "Match"


class PredictionType(graphene.ObjectType):
    """GraphQL type for Prediction."""
    id = graphene.Int()
    match_id = graphene.Int()
    prediction_type = graphene.String()
    confidence = graphene.Float()
    result = graphene.String()
    created_at = graphene.DateTime()

    class Meta:
        name = "Prediction"


class SubscriptionType(graphene.ObjectType):
    """GraphQL type for Subscription."""
    id = graphene.Int()
    user_id = graphene.Int()
    plan_type = graphene.String()
    status = graphene.String()
    renewal_date = graphene.DateTime()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    class Meta:
        name = "Subscription"
