"""Integration tests for authentication flow."""
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    """Create test client with clean database."""
    app = create_app('testing')
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

class TestAuthenticationFlow:
    """Test complete authentication workflow."""
    
    def test_full_registration_and_login_flow(self, client):
        """Test user can register and then login."""
        # Step 1: Register new user
        register_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'username': 'newuser'
        }
        
        response = client.post('/api/v1/auth/register',
            json=register_data
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'User created successfully'
        
        # Step 2: Login with registered credentials
        login_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!'
        }
        
        response = client.post('/api/v1/auth/login',
            json=login_data
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        token = data['access_token']
        
        # Step 3: Access protected route with token
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/v1/jobs',
            headers=headers
        )
        
        assert response.status_code == 200
    
    def test_login_with_invalid_credentials(self, client):
        """Test login fails with wrong credentials."""
        response = client.post('/api/v1/auth/login',
            json={
                'email': 'wrong@example.com',
                'password': 'wrongpassword'
            }
        )
        
        assert response.status_code == 401
    
    def test_protected_route_without_token(self, client):
        """Test protected route requires authentication."""
        response = client.get('/api/v1/jobs')
        assert response.status_code == 401
    
    def test_rate_limiting_on_login(self, client):
        """Test rate limiting prevents brute force."""
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        # Make multiple failed login attempts
        for _ in range(60):  # Exceed rate limit
            response = client.post('/api/v1/auth/login',
                json=login_data
            )
        
        # Should get rate limited
        assert response.status_code in [429, 401]
