"""Service Orchestrator - Coordinating microservices
Phase 5 Step 6.3 - Service mesh, dependency management, circuit breaker
Features: Service registry, health checks, load balancing
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    INITIALIZING = "initializing"


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class ServiceInstance:
    """Service instance metadata"""
    service_id: str
    instance_id: str
    host: str
    port: int
    status: ServiceStatus = ServiceStatus.INITIALIZING
    health_check_interval: int = 30
    last_health_check: Optional[datetime] = None
    consecutive_failures: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def is_healthy(self) -> bool:
        return self.status == ServiceStatus.HEALTHY


@dataclass
class CircuitBreaker:
    """Circuit breaker implementation"""
    service_id: str
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout: int = 60
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None

    def record_success(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.open()

    def open(self) -> None:
        self.state = CircuitState.OPEN
        logger.warning(f"Circuit breaker opened for {self.service_id}")

    def reset(self) -> None:
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        logger.info(f"Circuit breaker reset for {self.service_id}")

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                return True
            return False
        return True  # HALF_OPEN

    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return True
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout


class LoadBalancer:
    """Simple load balancer with round-robin and health-aware selection"""
    def __init__(self):
        self.current_index: Dict[str, int] = {}

    def select_instance(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        """Select healthy instance with round-robin"""
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            logger.error(f"No healthy instances available")
            return None

        service_id = healthy[0].service_id
        current = self.current_index.get(service_id, 0)
        selected = healthy[current % len(healthy)]
        self.current_index[service_id] = (current + 1) % len(healthy)
        return selected


class ServiceRegistry:
    """Registry for service discovery"""
    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.load_balancer = LoadBalancer()

    def register_service(self, instance: ServiceInstance) -> None:
        if instance.service_id not in self.services:
            self.services[instance.service_id] = []
            self.circuit_breakers[instance.service_id] = CircuitBreaker(
                service_id=instance.service_id
            )
        self.services[instance.service_id].append(instance)
        logger.info(f"Service registered: {instance.service_id}/{instance.instance_id}")

    def deregister_service(self, service_id: str, instance_id: str) -> None:
        if service_id in self.services:
            self.services[service_id] = [
                i for i in self.services[service_id] 
                if i.instance_id != instance_id
            ]
            if not self.services[service_id]:
                del self.services[service_id]

    def get_service_instance(self, service_id: str) -> Optional[ServiceInstance]:
        instances = self.services.get(service_id, [])
        return self.load_balancer.select_instance(instances)

    def update_health(self, service_id: str, instance_id: str, 
                     status: ServiceStatus) -> None:
        if service_id in self.services:
            for instance in self.services[service_id]:
                if instance.instance_id == instance_id:
                    instance.status = status
                    instance.last_health_check = datetime.utcnow()
                    
                    if status == ServiceStatus.HEALTHY:
                        instance.consecutive_failures = 0
                        cb = self.circuit_breakers.get(service_id)
                        if cb:
                            cb.record_success()
                    else:
                        instance.consecutive_failures += 1
                        cb = self.circuit_breakers.get(service_id)
                        if cb:
                            cb.record_failure()
                    break


@dataclass
class ServiceDependency:
    """Service dependency graph"""
    from_service: str
    to_service: str
    required: bool = True
    timeout: int = 30


class DependencyResolver:
    """Resolve and validate service dependencies"""
    def __init__(self):
        self.dependencies: List[ServiceDependency] = []

    def add_dependency(self, dep: ServiceDependency) -> None:
        self.dependencies.append(dep)

    def get_dependencies(self, service_id: str) -> List[str]:
        return [
            dep.to_service for dep in self.dependencies
            if dep.from_service == service_id
        ]

    def check_circular_dependencies(self) -> bool:
        """Check for circular dependencies in the graph"""
        visited = set()
        rec_stack = set()

        def has_cycle(service: str) -> bool:
            visited.add(service)
            rec_stack.add(service)

            for dep_service in self.get_dependencies(service):
                if dep_service not in visited:
                    if has_cycle(dep_service):
                        return True
                elif dep_service in rec_stack:
                    return True

            rec_stack.remove(service)
            return False

        all_services = set()
        for dep in self.dependencies:
            all_services.add(dep.from_service)
            all_services.add(dep.to_service)

        for service in all_services:
            if service not in visited:
                if has_cycle(service):
                    return True
        return False


class ServiceOrchestrator:
    """Main orchestrator coordinating all services"""
    def __init__(self):
        self.registry = ServiceRegistry()
        self.dependency_resolver = DependencyResolver()
        self.health_check_interval = 30

    def register_service(self, service_id: str, instances: List[Dict[str, Any]]) -> None:
        for idx, instance_config in enumerate(instances):
            instance = ServiceInstance(
                service_id=service_id,
                instance_id=f"{service_id}-{idx}",
                host=instance_config['host'],
                port=instance_config['port'],
                metadata=instance_config.get('metadata', {})
            )
            self.registry.register_service(instance)

    def add_dependency(self, from_service: str, to_service: str, 
                      required: bool = True) -> None:
        dep = ServiceDependency(
            from_service=from_service,
            to_service=to_service,
            required=required
        )
        self.dependency_resolver.add_dependency(dep)

    def get_service_url(self, service_id: str) -> Optional[str]:
        instance = self.registry.get_service_instance(service_id)
        if instance and instance.is_healthy:
            cb = self.registry.circuit_breakers.get(service_id)
            if cb and cb.can_execute():
                return instance.url
        return None

    async def start_health_checks(self) -> None:
        """Start periodic health checks for all services"""
        logger.info("Starting health check cycle")
        while True:
            for service_id, instances in self.registry.services.items():
                for instance in instances:
                    status = await self._check_instance_health(instance)
                    self.registry.update_health(
                        instance.service_id, 
                        instance.instance_id, 
                        status
                    )
            await asyncio.sleep(self.health_check_interval)

    async def _check_instance_health(self, instance: ServiceInstance) -> ServiceStatus:
        try:
            # Simulated health check
            logger.debug(f"Health check: {instance.service_id}/{instance.instance_id}")
            return ServiceStatus.HEALTHY
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return ServiceStatus.UNHEALTHY

    def get_orchestration_status(self) -> Dict[str, Any]:
        return {
            'services': {
                service_id: {
                    'instances': len(instances),
                    'healthy': sum(1 for i in instances if i.is_healthy),
                    'status': instances[0].status.value if instances else None
                }
                for service_id, instances in self.registry.services.items()
            },
            'circuit_breakers': {
                service_id: cb.state.value
                for service_id, cb in self.registry.circuit_breakers.items()
            },
            'timestamp': datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    logger.info("Service Orchestrator initialized")
