"""Dependency Injection & Configuration Management Service."""

import os
import json
import logging
from typing import Dict, Any, Type, TypeVar, Callable, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import importlib


logger = logging.getLogger(__name__)

T = TypeVar("T")


class EnvironmentType(str, Enum):
    """Environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class ServiceConfig:
    """Service configuration."""
    name: str
    class_path: str
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    singleton: bool = True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "class_path": self.class_path,
            "dependencies": self.dependencies,
            "config": self.config,
            "singleton": self.singleton,
        }


class ServiceRegistry:
    """Service registry for dependency injection."""

    def __init__(self):
        """Initialize service registry."""
        self.services: Dict[str, ServiceConfig] = {}
        self.singletons: Dict[str, Any] = {}
        self.factories: Dict[str, Callable] = {}

    def register(
        self,
        name: str,
        class_path: str,
        dependencies: Optional[List[str]] = None,
        singleton: bool = True,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register a service.
        
        Args:
            name: Service name
            class_path: Full class path (module.ClassName)
            dependencies: List of dependency service names
            singleton: Whether to instantiate once
            config: Configuration dictionary
        """
        self.services[name] = ServiceConfig(
            name=name,
            class_path=class_path,
            dependencies=dependencies or [],
            singleton=singleton,
            config=config or {},
        )
        logger.info(f"Registered service: {name}")

    def register_factory(
        self,
        name: str,
        factory: Callable,
        dependencies: Optional[List[str]] = None,
    ) -> None:
        """Register a factory function.
        
        Args:
            name: Factory name
            factory: Callable that creates the service
            dependencies: List of dependency service names
        """
        self.factories[name] = factory
        self.services[name] = ServiceConfig(
            name=name,
            class_path="<factory>",
            dependencies=dependencies or [],
            singleton=False,
        )
        logger.info(f"Registered factory: {name}")

    def resolve(self, name: str) -> Any:
        """Resolve a service by name.
        
        Args:
            name: Service name
            
        Returns:
            Service instance
        """
        if name not in self.services:
            raise ValueError(f"Service not registered: {name}")

        # Check singleton cache
        if self.services[name].singleton and name in self.singletons:
            return self.singletons[name]

        # Resolve factory
        if name in self.factories:
            instance = self.factories[name]()
            if self.services[name].singleton:
                self.singletons[name] = instance
            return instance

        # Resolve class
        service_config = self.services[name]
        dependencies = self._resolve_dependencies(service_config.dependencies)
        instance = self._instantiate_class(
            service_config.class_path,
            dependencies,
            service_config.config,
        )

        if service_config.singleton:
            self.singletons[name] = instance

        return instance

    def _resolve_dependencies(self, dependency_names: List[str]) -> Dict[str, Any]:
        """Resolve dependencies.
        
        Args:
            dependency_names: List of dependency names
            
        Returns:
            Dictionary of resolved dependencies
        """
        dependencies = {}
        for dep_name in dependency_names:
            dependencies[dep_name] = self.resolve(dep_name)
        return dependencies

    def _instantiate_class(
        self,
        class_path: str,
        dependencies: Dict[str, Any],
        config: Dict[str, Any],
    ) -> Any:
        """Instantiate a class.
        
        Args:
            class_path: Full class path
            dependencies: Resolved dependencies
            config: Configuration
            
        Returns:
            Class instance
        """
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)

        # Merge dependencies and config
        init_kwargs = {**config, **dependencies}
        return cls(**init_kwargs)

    def get_all_services(self) -> Dict[str, Dict]:
        """Get all registered services.
        
        Returns:
            Dictionary of services
        """
        return {name: config.to_dict() for name, config in self.services.items()}


class ConfigurationManager:
    """Application configuration manager."""

    def __init__(self, env: str = None):
        """Initialize configuration manager.
        
        Args:
            env: Environment type. If None, read from ENV variable.
        """
        self.env = env or os.getenv("ENV", EnvironmentType.DEVELOPMENT)
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from environment and files."""
        config_file = f"config/{self.env}.json"

        # Load from environment variables
        for key, value in os.environ.items():
            if key.startswith("APP_"):
                config_key = key[4:].lower()
                self.config[config_key] = self._parse_value(value)

        # Load from config file
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                file_config = json.load(f)
                self.config.update(file_config)

        logger.info(f"Configuration loaded for environment: {self.env}")

    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse configuration value.
        
        Args:
            value: String value to parse
            
        Returns:
            Parsed value
        """
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value

    def is_production(self) -> bool:
        """Check if production environment.
        
        Returns:
            True if production
        """
        return self.env == EnvironmentType.PRODUCTION

    def is_testing(self) -> bool:
        """Check if testing environment.
        
        Returns:
            True if testing
        """
        return self.env == EnvironmentType.TESTING
