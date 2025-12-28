"""Analytics Service Tests - Comprehensive unit tests for analytics functionality."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session

from app.services.analytics_service import AnalyticsService
from app.models import Job, Candidate, MatchResult


class TestAnalyticsService:
    """Test suite for AnalyticsService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def analytics_service(self, mock_db):
        """Create an AnalyticsService instance with mock database."""
        return AnalyticsService(mock_db)

    def test_service_initialization(self, mock_db):
        """Test AnalyticsService initialization."""
        service = AnalyticsService(mock_db)
        assert service.db == mock_db

    def test_get_recruitment_metrics(self, analytics_service, mock_db):
        """Test getting recruitment metrics."""
        # Setup
        mock_db.query.return_value.count.return_value = 10
        mock_db.query.return_value.filter.return_value.count.return_value = 5
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Execute
        metrics = analytics_service.get_recruitment_metrics(days=30)
        
        # Assert
        assert metrics is not None
        assert "total_jobs" in metrics
        assert "total_candidates" in metrics
        assert metrics["period_days"] == 30

    def test_get_job_analytics(self, analytics_service, mock_db):
        """Test getting job-level analytics."""
        # Setup
        mock_jobs = [
            Mock(spec=Job, status="active"),
            Mock(spec=Job, status="filled"),
            Mock(spec=Job, status="closed")
        ]
        mock_db.query.return_value.all.return_value = mock_jobs
        mock_db.query.return_value.filter.return_value.count.return_value = 1
        
        # Execute
        analytics = analytics_service.get_job_analytics(days=30)
        
        # Assert
        assert analytics is not None
        assert "total_jobs_analyzed" in analytics
        assert "jobs_by_status" in analytics
        assert analytics["analysis_period"] == 30

    def test_get_candidate_analytics(self, analytics_service, mock_db):
        """Test getting candidate-level analytics."""
        # Setup
        mock_candidates = [
            Mock(spec=Candidate, is_qualified=True),
            Mock(spec=Candidate, is_qualified=False)
        ]
        mock_db.query.return_value.all.return_value = mock_candidates
        
        # Execute
        analytics = analytics_service.get_candidate_analytics(days=30)
        
        # Assert
        assert analytics is not None
        assert "total_candidates" in analytics
        assert "qualified_candidates" in analytics
        assert "qualified_percentage" in analytics

    def test_get_match_performance(self, analytics_service, mock_db):
        """Test getting match performance metrics."""
        # Setup
        mock_matches = [
            Mock(spec=MatchResult, is_successful=True, match_score=0.85),
            Mock(spec=MatchResult, is_successful=False, match_score=0.45),
            Mock(spec=MatchResult, is_successful=True, match_score=0.75)
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_matches
        
        # Execute
        performance = analytics_service.get_match_performance(days=30)
        
        # Assert
        assert performance is not None
        assert "total_matches" in performance
        assert "successful_matches" in performance
        assert "success_rate" in performance
        assert "avg_match_score" in performance
        assert performance["total_matches"] == 3

    def test_get_job_enrichment_impact(self, analytics_service, mock_db):
        """Test measuring job enrichment service impact."""
        # Setup
        mock_jobs_before = [Mock(spec=Job) for _ in range(10)]
        mock_jobs_after = [Mock(spec=Job) for _ in range(8)]
        mock_db.query.return_value.filter.return_value.count.return_value = 8
        
        # Execute
        impact = analytics_service.get_job_enrichment_impact()
        
        # Assert
        assert impact is not None
        assert "impact_type" in impact
        assert impact["impact_type"] == "job_enrichment"

    def test_get_matching_accuracy(self, analytics_service, mock_db):
        """Test measuring matching algorithm accuracy."""
        # Setup
        mock_matches = [
            Mock(spec=MatchResult, is_successful=True, accuracy_score=0.9),
            Mock(spec=MatchResult, is_successful=True, accuracy_score=0.85),
            Mock(spec=MatchResult, is_successful=False, accuracy_score=0.4)
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_matches
        
        # Execute
        accuracy = analytics_service.get_matching_accuracy()
        
        # Assert
        assert accuracy is not None
        assert "overall_accuracy" in accuracy
        assert "accuracy_trend" in accuracy

    def test_get_top_job_categories(self, analytics_service, mock_db):
        """Test getting top job categories by posting frequency."""
        # Setup
        mock_jobs = [
            Mock(spec=Job, category="Engineering"),
            Mock(spec=Job, category="Engineering"),
            Mock(spec=Job, category="Sales"),
            Mock(spec=Job, category="Marketing")
        ]
        mock_db.query.return_value.all.return_value = mock_jobs
        
        # Execute
        categories = analytics_service.get_top_job_categories()
        
        # Assert
        assert categories is not None
        assert "top_categories" in categories

    def test_get_candidate_skill_distribution(self, analytics_service, mock_db):
        """Test getting candidate skill distribution."""
        # Setup
        mock_candidates = [
            Mock(spec=Candidate, skills="Python,Django,PostgreSQL"),
            Mock(spec=Candidate, skills="Python,FastAPI"),
            Mock(spec=Candidate, skills="JavaScript,React")
        ]
        mock_db.query.return_value.all.return_value = mock_candidates
        
        # Execute
        distribution = analytics_service.get_candidate_skill_distribution()
        
        # Assert
        assert distribution is not None
        assert "skill_distribution" in distribution

    def test_metrics_with_invalid_days(self, analytics_service):
        """Test metrics calculation with invalid day parameter."""
        # Execute & Assert
        with pytest.raises(ValueError):
            analytics_service.get_recruitment_metrics(days=-1)

    def test_generate_analytics_report(self, analytics_service, mock_db):
        """Test generating comprehensive analytics report."""
        # Setup
        mock_db.query.return_value.count.return_value = 50
        mock_db.query.return_value.filter.return_value.count.return_value = 25
        mock_db.query.return_value.all.return_value = []
        
        # Execute
        report = analytics_service.generate_analytics_report(days=30)
        
        # Assert
        assert report is not None
        assert "report_id" in report
        assert "generated_at" in report
        assert "summary" in report

    def test_export_metrics_as_json(self, analytics_service, mock_db):
        """Test exporting metrics in JSON format."""
        # Setup
        mock_db.query.return_value.count.return_value = 10
        mock_db.query.return_value.all.return_value = []
        
        # Execute
        json_export = analytics_service.export_metrics_as_json(days=30)
        
        # Assert
        assert json_export is not None
        assert isinstance(json_export, str)

    def test_export_metrics_as_csv(self, analytics_service, mock_db):
        """Test exporting metrics in CSV format."""
        # Setup
        mock_db.query.return_value.count.return_value = 10
        mock_db.query.return_value.all.return_value = []
        
        # Execute
        csv_export = analytics_service.export_metrics_as_csv(days=30)
        
        # Assert
        assert csv_export is not None
        assert isinstance(csv_export, str)

    def test_analytics_cache_invalidation(self, analytics_service):
        """Test analytics cache invalidation."""
        # Execute
        analytics_service.invalidate_cache()
        
        # Assert - Cache should be cleared
        assert analytics_service.cache_valid is False

    def test_multiple_concurrent_requests(self, analytics_service, mock_db):
        """Test analytics service with multiple concurrent requests."""
        # Setup
        mock_db.query.return_value.count.return_value = 10
        mock_db.query.return_value.all.return_value = []
        
        # Execute multiple requests
        results = []
        for i in range(5):
            result = analytics_service.get_recruitment_metrics(days=30)
            results.append(result)
        
        # Assert
        assert len(results) == 5
        assert all(r is not None for r in results)

    def test_analytics_error_handling(self, analytics_service, mock_db):
        """Test error handling in analytics service."""
        # Setup - Simulate database error
        mock_db.query.side_effect = Exception("Database connection error")
        
        # Execute & Assert
        with pytest.raises(Exception):
            analytics_service.get_recruitment_metrics(days=30)

    def test_performance_metrics_calculation(self, analytics_service, mock_db):
        """Test performance metrics calculation accuracy."""
        # Setup
        matches = [
            Mock(spec=MatchResult, is_successful=True, match_score=0.9),
            Mock(spec=MatchResult, is_successful=True, match_score=0.8),
            Mock(spec=MatchResult, is_successful=False, match_score=0.3)
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = matches
        
        # Execute
        perf = analytics_service.get_match_performance(days=30)
        
        # Assert
        assert perf["success_rate"] == pytest.approx(66.67, 0.1)
        assert perf["avg_match_score"] == pytest.approx(0.533, 0.01)


class TestAnalyticsIntegration:
    """Integration tests for analytics functionality."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    def test_full_analytics_pipeline(self, mock_db):
        """Test complete analytics pipeline."""
        # Setup
        service = AnalyticsService(mock_db)
        mock_db.query.return_value.count.return_value = 50
        mock_db.query.return_value.all.return_value = []
        
        # Execute
        metrics = service.get_recruitment_metrics(days=30)
        job_analytics = service.get_job_analytics(days=30)
        candidate_analytics = service.get_candidate_analytics(days=30)
        
        # Assert
        assert metrics is not None
        assert job_analytics is not None
        assert candidate_analytics is not None

    def test_analytics_with_large_dataset(self, mock_db):
        """Test analytics performance with large dataset."""
        # Setup - Create large mock dataset
        service = AnalyticsService(mock_db)
        large_dataset = [Mock(spec=Job) for _ in range(1000)]
        mock_db.query.return_value.all.return_value = large_dataset
        mock_db.query.return_value.count.return_value = 1000
        
        # Execute
        analytics = service.get_job_analytics(days=30)
        
        # Assert
        assert analytics is not None
        assert "total_jobs_analyzed" in analytics
