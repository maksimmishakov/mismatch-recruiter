# System Architecture

## Overview
The MisMatch Recruitment Bot is built on a modern, scalable microservices architecture designed for high availability and performance.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Web Server**: Uvicorn
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **API**: RESTful with async/await
- **LLM**: OpenAI GPT-4o-mini for interview question generation

### Deployment
- **Platform**: Yandex Cloud / Amvera
- **Container**: Docker
- **CI/CD**: GitHub Actions
- **Infrastructure**: Kubernetes-ready deployment

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  (Web Browser / Mobile App / External API Consumers)            │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────────────────┐
│                      API Gateway                                │
│  (FastAPI Application)                                          │
│  - Authentication & Authorization                               │
│  - Rate Limiting                                                │
│  - Request Validation                                           │
└────┬──────────┬──────────┬──────────┬──────────┬────────────────┘
     │          │          │          │          │
┌────▼──┐ ┌────▼──┐ ┌────▼──┐ ┌────▼──┐ ┌────▼──┐
│ Auth  │ │Question│ │Candidate│ │Evaluation│ │Utils │
│Routes │ │Routes │ │Routes │ │Routes │ │Routes │
└────┬──┘ └────┬──┘ └────┬──┘ └────┬──┘ └────┬──┘
     │         │         │         │         │
     └─────────┼─────────┼─────────┼─────────┘
               │         │         │
     ┌─────────▼─────────▼─────────▼─────────┐
     │       Business Logic Layer             │
     │  ┌──────────────────────────────────┐ │
     │  │ Interview Question Generator    │ │ Calls GPT-4o-mini
     │  │ - Job matching                  │ │ for intelligent
     │  │ - Question synthesis            │ │ question generation
     │  │ - Difficulty calibration        │ │
     │  └──────────────────────────────────┘ │
     │  ┌──────────────────────────────────┐ │
     │  │ Candidate Evaluation Service    │ │ Evaluates responses
     │  │ - Answer analysis               │ │ using AI
     │  │ - Score calculation             │ │
     │  │ - Recommendation generation     │ │
     │  └──────────────────────────────────┘ │
     │  ┌──────────────────────────────────┐ │
     │  │ User Management Service         │ │
     │  │ - Authentication                │ │
     │  │ - Permission handling           │ │
     │  └──────────────────────────────────┘ │
     └──────────┬──────────┬──────────────────┘
                │          │
     ┌──────────▼──┐  ┌────▼──────────┐
     │   Redis     │  │  PostgreSQL   │
     │   Cache     │  │   Database    │
     │             │  │               │
     │ - Questions │  │ - Users       │
     │ - Sessions  │  │ - Interviews  │
     │ - Scores    │  │ - Candidates  │
     │             │  │ - Responses   │
     │             │  │ - Evaluations│
     └─────────────┘  └───────────────┘
```

## Key Components

### 1. Authentication Layer
- JWT-based token authentication
- Bearer token validation on all endpoints
- Session management with Redis
- User role-based access control

### 2. API Routes
- `routes/auth.py`: Authentication endpoints
- `routes/questions.py`: Interview question endpoints
- `routes/candidates.py`: Candidate management
- `routes/evaluations.py`: Evaluation endpoints

### 3. Services
- `services/interview_generator.py`: Question generation logic
- `services/candidate_service.py`: Candidate operations
- `services/evaluation_service.py`: Answer evaluation

### 4. Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password_hash VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Candidates Table
```sql
CREATE TABLE candidates (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    experience_years INTEGER,
    skills JSON,
    job_position VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Interviews Table
```sql
CREATE TABLE interviews (
    id UUID PRIMARY KEY,
    candidate_id UUID REFERENCES candidates(id),
    job_description TEXT,
    question_count INTEGER DEFAULT 5,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

## Data Flow

### Interview Question Generation Flow
1. User submits job description and candidate profile
2. System validates authentication and input
3. Caches are checked for similar previous questions (Redis)
4. If cache miss, GPT-4o-mini generates personalized questions
5. Questions are cached for future use
6. Response is returned to client with question IDs

### Candidate Evaluation Flow
1. User submits candidate responses to questions
2. System validates interview session
3. Responses are processed with GPT-4o-mini
4. AI evaluation generates scores and feedback
5. Results are persisted to PostgreSQL
6. Evaluation report is returned

## Caching Strategy

### Redis Cache Keys
- `questions:{job_id}:{difficulty}`: Cached interview questions
- `session:{user_id}`: Active user sessions
- `evaluation:{interview_id}`: Cached evaluation results
- TTL: 24 hours for questions, 30 days for evaluations

## Scalability Considerations

### Horizontal Scaling
- Stateless API design allows multiple instances
- PostgreSQL read replicas for high query volume
- Redis cluster for distributed caching
- Load balancing across API instances

### Performance Optimization
- Database query optimization with indices
- Redis caching layer for frequently accessed data
- Async/await for non-blocking I/O
- Connection pooling for database and Redis

## Security

### Authentication
- JWT tokens with 24-hour expiration
- Refresh token mechanism
- HTTPS-only communication

### Data Protection
- Password hashing with bcrypt
- SQL injection prevention with parameterized queries
- CORS policies for cross-origin requests
- Rate limiting per API key

## Deployment Architecture

### Development
- Local PostgreSQL and Redis instances
- FastAPI development server
- Hot reloading enabled

### Production
- Containerized deployment on Yandex Cloud
- Managed PostgreSQL service
- Managed Redis service
- CI/CD pipeline via GitHub Actions
- Automated testing on every push

### Monitoring
- Application logs to CloudWatch/Yandex Cloud Logs
- Error tracking with Sentry
- Performance metrics tracking
- Health check endpoints

## Environment Variables

```ini
# Database
DATABASE_URL=postgresql://user:password@host:5432/Mismatch

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# API
JWT_SECRET=your-secret-key
API_TIMEOUT=30
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_PERIOD=3600
```

## Future Enhancements

1. **Microservices Split**: Separate question generation and evaluation into independent services
2. **Message Queue**: Implement message queue (RabbitMQ/Kafka) for async processing
3. **GraphQL**: Add GraphQL API alongside REST
4. **ML Model**: Train custom models for specialized interview types
5. **Multi-language**: Support multiple languages for questions
6. **Video Interviews**: Integrate video interview capabilities
7. **Reporting**: Advanced analytics and recruitment reports

## Conclusion

This architecture provides a solid foundation for a scalable, maintainable recruitment platform with modern best practices in API design, data management, and deployment strategies.n
