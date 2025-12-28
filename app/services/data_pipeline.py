"""Data Pipeline Service - ETL and data processing orchestration
Phase 5 Step 6.5 - Streaming pipelines, batch processing, data validation
Features: DAG execution, error recovery, data quality checks
"""
import logging
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractmethod
import hashlib
from collections import defaultdict

logger = logging.getLogger(__name__)


class PipelineStatus(Enum):
    """Pipeline execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStatus(Enum):
    """Task execution status"""
    IDLE = "idle"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


@dataclass
class TaskMetadata:
    """Task metadata and configuration"""
    task_id: str
    name: str
    handler: Callable
    dependencies: List[str]
    timeout: int = 300
    retries: int = 3
    enabled: bool = True
    tags: Dict[str, str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


@dataclass
class TaskExecution:
    """Task execution record"""
    task_id: str
    status: TaskStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: float = 0.0
    error: Optional[str] = None
    retry_count: int = 0
    output: Optional[Any] = None

    @property
    def duration_seconds(self) -> float:
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return self.duration


@dataclass
class PipelineExecution:
    """Pipeline execution record"""
    pipeline_id: str
    execution_id: str
    status: PipelineStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    task_executions: Dict[str, TaskExecution] = None
    error: Optional[str] = None
    data_processed: int = 0

    def __post_init__(self):
        if self.task_executions is None:
            self.task_executions = {}

    def to_dict(self) -> Dict:
        return {
            'pipeline_id': self.pipeline_id,
            'execution_id': self.execution_id,
            'status': self.status.value,
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': (self.completed_at - self.started_at).total_seconds() 
                               if self.completed_at else 0,
            'task_count': len(self.task_executions),
            'data_processed': self.data_processed
        }


class PipelineTask(ABC):
    """Base class for pipeline tasks"""
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def validate_inputs(self, context: Dict[str, Any]) -> bool:
        pass


class DataValidationTask(PipelineTask):
    """Task for data validation and quality checks"""
    def __init__(self, schema: Dict[str, str]):
        self.schema = schema

    def execute(self, context: Dict[str, Any]) -> bool:
        data = context.get('data', {})
        return self.validate_data(data)

    def validate_inputs(self, context: Dict[str, Any]) -> bool:
        return 'data' in context

    def validate_data(self, data: Dict[str, Any]) -> bool:
        for field, expected_type in self.schema.items():
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False
            if not isinstance(data[field], eval(expected_type)):
                logger.error(f"Type mismatch for {field}")
                return False
        return True


class TransformationTask(PipelineTask):
    """Task for data transformation"""
    def __init__(self, transform_func: Callable):
        self.transform_func = transform_func

    def execute(self, context: Dict[str, Any]) -> Any:
        data = context.get('data')
        return self.transform_func(data)

    def validate_inputs(self, context: Dict[str, Any]) -> bool:
        return 'data' in context


class DAGPipeline:
    """Directed Acyclic Graph based pipeline executor"""
    def __init__(self, pipeline_id: str):
        self.pipeline_id = pipeline_id
        self.tasks: Dict[str, TaskMetadata] = {}
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.execution_history: List[PipelineExecution] = []

    def add_task(self, task_id: str, task_meta: TaskMetadata) -> None:
        self.tasks[task_id] = task_meta
        logger.info(f"Task added: {task_id}")

    def add_dependency(self, task_id: str, depends_on: str) -> None:
        if depends_on not in self.tasks:
            raise ValueError(f"Task {depends_on} not found")
        self.graph[depends_on].append(task_id)

    def _topological_sort(self) -> List[str]:
        """Topological sort for execution order"""
        visited = set()
        stack = []
        
        def visit(node: str):
            if node in visited:
                return
            visited.add(node)
            for dependent in self.graph.get(node, []):
                visit(dependent)
            stack.append(node)
        
        for task_id in self.tasks:
            visit(task_id)
        return stack

    def execute(self, context: Dict[str, Any]) -> PipelineExecution:
        """Execute the pipeline"""
        execution_id = self._generate_execution_id()
        execution = PipelineExecution(
            pipeline_id=self.pipeline_id,
            execution_id=execution_id,
            status=PipelineStatus.RUNNING,
            started_at=datetime.utcnow()
        )

        execution_order = self._topological_sort()
        
        for task_id in execution_order:
            task_meta = self.tasks[task_id]
            if not task_meta.enabled:
                execution.task_executions[task_id] = TaskExecution(
                    task_id=task_id,
                    status=TaskStatus.SKIPPED
                )
                continue

            task_exec = self._execute_task(
                task_id, task_meta, context, 
                execution.task_executions
            )
            execution.task_executions[task_id] = task_exec

            if task_exec.status == TaskStatus.FAILED:
                execution.status = PipelineStatus.FAILED
                execution.error = task_exec.error
                break

        execution.completed_at = datetime.utcnow()
        if execution.status == PipelineStatus.RUNNING:
            execution.status = PipelineStatus.COMPLETED
        
        self.execution_history.append(execution)
        logger.info(f"Pipeline execution completed: {execution_id}")
        return execution

    def _execute_task(self, task_id: str, task_meta: TaskMetadata,
                     context: Dict[str, Any],
                     prev_executions: Dict[str, TaskExecution]) -> TaskExecution:
        """Execute a single task with error handling"""
        task_exec = TaskExecution(
            task_id=task_id,
            status=TaskStatus.RUNNING,
            started_at=datetime.utcnow()
        )

        try:
            # Check dependencies
            for dep in task_meta.dependencies:
                if dep in prev_executions:
                    if prev_executions[dep].status != TaskStatus.SUCCESS:
                        task_exec.status = TaskStatus.SKIPPED
                        return task_exec

            # Execute task
            result = task_meta.handler(context)
            context[task_id] = result
            task_exec.status = TaskStatus.SUCCESS
            task_exec.output = result
        except Exception as e:
            logger.error(f"Task failed: {task_id}, {str(e)}")
            task_exec.status = TaskStatus.FAILED
            task_exec.error = str(e)

        task_exec.completed_at = datetime.utcnow()
        return task_exec

    def _generate_execution_id(self) -> str:
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{self.pipeline_id}{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get pipeline execution statistics"""
        if not self.execution_history:
            return {}
        
        last_exec = self.execution_history[-1]
        return last_exec.to_dict()


class PipelineManager:
    """Manages multiple pipelines"""
    def __init__(self):
        self.pipelines: Dict[str, DAGPipeline] = {}

    def create_pipeline(self, pipeline_id: str) -> DAGPipeline:
        pipeline = DAGPipeline(pipeline_id)
        self.pipelines[pipeline_id] = pipeline
        logger.info(f"Pipeline created: {pipeline_id}")
        return pipeline

    def execute_pipeline(self, pipeline_id: str, 
                        context: Dict[str, Any]) -> Optional[PipelineExecution]:
        if pipeline_id not in self.pipelines:
            logger.error(f"Pipeline not found: {pipeline_id}")
            return None
        
        return self.pipelines[pipeline_id].execute(context)

    def get_pipeline_stats(self, pipeline_id: str) -> Dict[str, Any]:
        if pipeline_id not in self.pipelines:
            return {}
        return self.pipelines[pipeline_id].get_execution_stats()


if __name__ == "__main__":
    logger.info("Data Pipeline Service initialized")
