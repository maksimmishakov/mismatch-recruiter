"""Swagger/OpenAPI documentation configuration."""
from flask import Flask
from flasgger import Swagger, swag_from
from typing import Dict, Any


# Swagger configuration
SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}

# OpenAPI template
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "MisMatch Recruiter API",
        "description": "API для платформы подбора персонала MisMatch. "
                       "Включает эндпоинты для управления резюме, вакансиями, "
                       "анализом кандидатов и мэтчингом.",
        "contact": {
            "name": "MisMatch Support",
            "email": "support@mismatch.ru",
            "url": "https://github.com/maksimmishakov/mismatch-recruiter"
        },
        "version": "1.0.0",
        "termsOfService": "/terms",
    },
    "host": "api.mismatch.ru",
    "basePath": "/api/v1",
    "schemes": [
        "https",
        "http"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header",
            "description": "API Key for authentication"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "tags": [
        {
            "name": "Authentication",
            "description": "Операции аутентификации и авторизации"
        },
        {
            "name": "Users",
            "description": "Управление пользователями"
        },
        {
            "name": "Resumes",
            "description": "Управление резюме кандидатов"
        },
        {
            "name": "Jobs",
            "description": "Управление вакансиями"
        },
        {
            "name": "Matching",
            "description": "Анализ и подбор кандидатов"
        },
        {
            "name": "Analytics",
            "description": "Аналитика и отчеты"
        },
        {
            "name": "Health",
            "description": "Проверка состояния системы"
        }
    ],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "user@example.com"
                },
                "name": {
                    "type": "string",
                    "example": "Иван Иванов"
                },
                "subscription_plan": {
                    "type": "string",
                    "enum": ["free", "basic", "premium", "enterprise"],
                    "example": "premium"
                },
                "is_active": {
                    "type": "boolean",
                    "example": True
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2026-02-07T22:00:00Z"
                }
            }
        },
        "Resume": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "user_id": {
                    "type": "integer",
                    "example": 1
                },
                "file_path": {
                    "type": "string",
                    "example": "/uploads/resume_123.pdf"
                },
                "parsed_data": {
                    "type": "object",
                    "properties": {
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["Python", "Flask", "SQL"]
                        },
                        "experience_years": {
                            "type": "integer",
                            "example": 3
                        },
                        "education": {
                            "type": "string",
                            "example": "МГУ, Факультет ВМК"
                        }
                    }
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "Job": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "title": {
                    "type": "string",
                    "example": "Senior Python Developer"
                },
                "description": {
                    "type": "string",
                    "example": "Требуется опытный Python разработчик"
                },
                "requirements": {
                    "type": "object",
                    "properties": {
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"},
                            "example": ["Python", "Django", "PostgreSQL"]
                        },
                        "experience": {
                            "type": "string",
                            "example": "3+ years"
                        }
                    }
                },
                "salary_min": {
                    "type": "integer",
                    "example": 150000
                },
                "salary_max": {
                    "type": "integer",
                    "example": 250000
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "Match": {
            "type": "object",
            "properties": {
                "resume_id": {
                    "type": "integer",
                    "example": 1
                },
                "job_id": {
                    "type": "integer",
                    "example": 1
                },
                "score": {
                    "type": "number",
                    "format": "float",
                    "minimum": 0,
                    "maximum": 100,
                    "example": 85.5
                },
                "matching_factors": {
                    "type": "object",
                    "properties": {
                        "skills_match": {"type": "number", "example": 90.0},
                        "experience_match": {"type": "number", "example": 80.0},
                        "location_match": {"type": "number", "example": 100.0}
                    }
                }
            }
        },
        "Error": {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string",
                    "example": "Invalid request"
                },
                "message": {
                    "type": "string",
                    "example": "Missing required field: email"
                },
                "status": {
                    "type": "string",
                    "example": "error"
                }
            }
        },
        "Success": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Operation successful"
                },
                "status": {
                    "type": "string",
                    "example": "success"
                },
                "data": {
                    "type": "object"
                }
            }
        }
    },
    "responses": {
        "400": {
            "description": "Bad Request - Invalid input parameters",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "401": {
            "description": "Unauthorized - Authentication required",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "403": {
            "description": "Forbidden - Insufficient permissions",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "404": {
            "description": "Not Found - Resource not found",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "429": {
            "description": "Too Many Requests - Rate limit exceeded",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "500": {
            "description": "Internal Server Error",
            "schema": {"$ref": "#/definitions/Error"}
        }
    }
}


def init_swagger(app: Flask) -> Swagger:
    """Initialize Swagger documentation for Flask app.
    
    Args:
        app: Flask application instance
        
    Returns:
        Swagger instance
    """
    swagger = Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)
    return swagger


def get_swagger_spec(endpoint: str, **kwargs) -> Dict[str, Any]:
    """Generate Swagger spec for an endpoint.
    
    Args:
        endpoint: Endpoint name
        **kwargs: Additional spec parameters
        
    Returns:
        Swagger specification dictionary
    """
    return {
        "tags": kwargs.get("tags", ["General"]),
        "summary": kwargs.get("summary", ""),
        "description": kwargs.get("description", ""),
        "parameters": kwargs.get("parameters", []),
        "responses": kwargs.get("responses", {}),
        "security": kwargs.get("security", [{"Bearer": []}])
    }
