"""API Documentation Service - OpenAPI/Swagger specification generation and management."""

import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import json


logger = logging.getLogger(__name__)


class HTTPMethod(str, Enum):
    """HTTP methods."""
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
    OPTIONS = "options"


class ResponseType(str, Enum):
    """Response types."""
    JSON = "application/json"
    XML = "application/xml"
    PLAIN_TEXT = "text/plain"
    HTML = "text/html"


@dataclass
class Parameter:
    """API parameter definition."""
    name: str
    param_type: str
    required: bool = False
    description: str = ""
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None

    def to_dict(self) -> Dict:
        """Convert to OpenAPI parameter."""
        param_def = {
            "name": self.name,
            "in": "query",
            "required": self.required,
            "schema": {"type": self.param_type},
        }
        if self.description:
            param_def["description"] = self.description
        if self.default is not None:
            param_def["schema"]["default"] = self.default
        if self.enum:
            param_def["schema"]["enum"] = self.enum
        return param_def


@dataclass
class APIResponse:
    """API response definition."""
    status_code: int
    description: str
    response_type: ResponseType = ResponseType.JSON
    schema: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict:
        """Convert to OpenAPI response."""
        response = {"description": self.description}
        if self.schema:
            response["content"] = {
                self.response_type.value: {"schema": self.schema}
            }
        return response


@dataclass
class Endpoint:
    """API endpoint definition."""
    path: str
    method: HTTPMethod
    summary: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    parameters: List[Parameter] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    responses: List[APIResponse] = field(default_factory=list)
    auth_required: bool = False
    rate_limit: Optional[int] = None

    def to_dict(self) -> Dict:
        """Convert to OpenAPI operation."""
        operation = {
            "summary": self.summary,
            "operationId": f"{self.method.value}_{self.path.replace('/', '_')}",
        }

        if self.description:
            operation["description"] = self.description
        if self.tags:
            operation["tags"] = self.tags
        if self.parameters:
            operation["parameters"] = [p.to_dict() for p in self.parameters]
        if self.request_body:
            operation["requestBody"] = self.request_body
        if self.responses:
            operation["responses"] = {
                str(r.status_code): r.to_dict() for r in self.responses
            }
        if self.auth_required:
            operation["security"] = [{"bearerAuth": []}]

        return operation


class APIDocumentationService:
    """API documentation and OpenAPI spec generation service."""

    def __init__(
        self,
        title: str,
        version: str,
        description: str = "",
        base_url: str = "http://localhost:8000",
    ):
        self.title = title
        self.version = version
        self.description = description
        self.base_url = base_url
        self.endpoints: Dict[str, Endpoint] = {}
        self.schemas: Dict[str, Dict[str, Any]] = {}
        self.security_schemes: Dict[str, Dict[str, Any]] = {}

    def register_endpoint(self, endpoint: Endpoint) -> None:
        """Register an API endpoint.
        
        Args:
            endpoint: Endpoint definition
        """
        key = f"{endpoint.method.value}_{endpoint.path}"
        self.endpoints[key] = endpoint
        logger.info(f"Registered endpoint: {endpoint.method.value.upper()} {endpoint.path}")

    def register_schema(
        self,
        name: str,
        schema: Dict[str, Any],
    ) -> None:
        """Register a data schema.
        
        Args:
            name: Schema name
            schema: JSON Schema definition
        """
        self.schemas[name] = schema
        logger.info(f"Registered schema: {name}")

    def register_security_scheme(
        self,
        name: str,
        scheme_type: str,
        scheme: str,
        bearer_format: Optional[str] = None,
    ) -> None:
        """Register security scheme.
        
        Args:
            name: Scheme name
            scheme_type: Type (http, apiKey, oauth2, openIdConnect)
            scheme: Scheme value
            bearer_format: Bearer format (e.g., JWT)
        """
        security_scheme = {
            "type": scheme_type,
            "scheme": scheme,
        }
        if bearer_format:
            security_scheme["bearerFormat"] = bearer_format

        self.security_schemes[name] = security_scheme
        logger.info(f"Registered security scheme: {name}")

    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI 3.0.0 specification.
        
        Returns:
            OpenAPI specification dictionary
        """
        # Group endpoints by path
        paths: Dict[str, Dict] = {}
        for key, endpoint in self.endpoints.items():
            if endpoint.path not in paths:
                paths[endpoint.path] = {}
            paths[endpoint.path][endpoint.method.value] = endpoint.to_dict()

        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
            },
            "servers": [{"url": self.base_url}],
            "paths": paths,
        }

        if self.description:
            spec["info"]["description"] = self.description

        if self.schemas:
            spec["components"] = {"schemas": self.schemas}

        if self.security_schemes:
            if "components" not in spec:
                spec["components"] = {}
            spec["components"]["securitySchemes"] = self.security_schemes

        return spec

    def export_to_json(self, filename: str) -> None:
        """Export specification to JSON file.
        
        Args:
            filename: Output filename
        """
        spec = self.generate_openapi_spec()
        with open(filename, "w") as f:
            json.dump(spec, f, indent=2)
        logger.info(f"Exported OpenAPI spec to {filename}")

    def export_to_yaml(self, filename: str) -> None:
        """Export specification to YAML file.
        
        Args:
            filename: Output filename
        """
        try:
            import yaml
            spec = self.generate_openapi_spec()
            with open(filename, "w") as f:
                yaml.dump(spec, f, default_flow_style=False)
            logger.info(f"Exported OpenAPI spec to {filename}")
        except ImportError:
            logger.error("PyYAML not installed. Install with: pip install pyyaml")

    def get_endpoint_count(self) -> int:
        """Get total endpoint count.
        
        Returns:
            Number of registered endpoints
        """
        return len(self.endpoints)

    def get_endpoints_by_tag(self, tag: str) -> List[Endpoint]:
        """Get endpoints by tag.
        
        Args:
            tag: Tag name
            
        Returns:
            List of endpoints with given tag
        """
        return [
            endpoint for endpoint in self.endpoints.values()
            if tag in endpoint.tags
        ]

    def get_health_check_spec(self) -> Dict[str, Any]:
        """Get health check endpoint specification.
        
        Returns:
            Health check endpoint spec
        """
        return {
            "GET /health": {
                "summary": "Health check",
                "responses": {
                    "200": {"description": "Service is healthy"},
                    "503": {"description": "Service is unavailable"},
                },
            }
        }

    def validate_endpoint(self, endpoint: Endpoint) -> bool:
        """Validate endpoint definition.
        
        Args:
            endpoint: Endpoint to validate
            
        Returns:
            True if valid
        """
        if not endpoint.path:
            logger.warning("Endpoint path is empty")
            return False
        if not endpoint.summary:
            logger.warning(f"Endpoint {endpoint.path} has no summary")
            return False
        if endpoint.auth_required and not self.security_schemes:
            logger.warning(f"Endpoint {endpoint.path} requires auth but no schemes defined")
            return False
        return True
