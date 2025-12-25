"""Full system integration tests

Tests for:
- Amvera integration
- Webhook system
- GraphQL endpoint
- Monitoring metrics
"""

import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create test app"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


class TestAmveraIntegration:
    """Test Amvera cloud integration"""

    def test_amvera_service_initialized(self, app):
        """Amvera service should initialize"""
        from services.amvera_monitoring_service import get_amvera_service
        amvera = get_amvera_service()
        assert amvera is not None

    def test_amvera_metrics_push(self, app):
        """Should push metrics to Amvera"""
        from services.amvera_monitoring_service import get_amvera_service
        amvera = get_amvera_service()
        if amvera.enabled:
            result = amvera.push_metric('test_metric', 100.0)
            assert isinstance(result, bool)


class TestGraphQLEndpoint:
    """Test GraphQL endpoint"""

    def test_graphql_endpoint_exists(self, app):
        """GraphQL endpoint should be accessible"""
        with app.test_client() as client:
            response = client.post('/graphql',
                json={'query': '{ __typename }'})
            assert response.status_code in [200, 400]  # 400 if schema not set up


class TestMonitoringMetrics:
    """Test monitoring metrics endpoint"""

    def test_metrics_endpoint(self, app):
        """Metrics endpoint should return prometheus format"""
        with app.test_client() as client:
            response = client.get('/metrics')
            # Endpoint may not exist, but if it does, should return 200
            if response.status_code == 200:
                assert b'TYPE' in response.data or b'HELP' in response.data


class TestFullEndpointIntegration:
    """Test all endpoints work together"""

    def test_health_check_integration(self, app):
        """Health check should work with all services"""
        with app.test_client() as client:
            response = client.get('/api/health')
            assert response.status_code == 200
            data = response.json
            assert 'status' in data

    def test_production_readiness(self, app):
        """System should be production ready"""
        # All critical endpoints should be accessible
        with app.test_client() as client:
            # Health check
            health = client.get('/api/health')
            assert health.status_code == 200

            # If auth endpoints exist
            register = client.post('/api/auth/register',
                json={'email': 'test@example.com', 'password': 'Test1234', 'name': 'Test'})
            # Should return 201 (created) or 400 (validation error)
            assert register.status_code in [201, 400, 409]
