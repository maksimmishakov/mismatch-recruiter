"""Unit tests for authentication endpoints."""

import pytest
from flask import json


class TestAuthEndpoints:
    """Test suite for authentication endpoints."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'username': 'testuser',
            'first_name': 'Test', 'last_name': 'User'
        }
        
        response = client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user_id' in data
        assert data['email'] == 'test@example.com'
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email."""
        payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'username': 'testuser',
            'first_name': 'Test', 'last_name': 'User'
        }
        
        # First registration
        client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Second registration with same email
        response = client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 409  # Conflict
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        payload = {
            'email': 'invalid-email',
            'password': 'TestPass123!',
            'username': 'testuser',
            'first_name': 'Test', 'last_name': 'User'
        }
        
        response = client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400  # Bad Request
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        payload = {
            'email': 'test@example.com',
            'password': 'weak',  # No uppercase, no digits, no special chars
            'username': 'testuser',
            'first_name': 'Test', 'last_name': 'User'
        }
        
        response = client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_login_success(self, client):
        """Test successful user login."""
        # Register first
        register_payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'username': 'testuser',
            'first_name': 'Test', 'last_name': 'User'
        }
        client.post(
            '/api/auth/register',
            data=json.dumps(register_payload),
            content_type='application/json'
        )
        
        # Login
        login_payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        login_payload = {
            'email': 'nonexistent@example.com',
            'password': 'WrongPass123!'
        }
        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 401  # Unauthorized
    
    def test_get_current_user(self, client):
        """Test getting current user information."""
        # Register and login
        register_payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'username': 'testuser',
            'first_name': 'Test', 'last_name': 'User'
        }
        client.post(
            '/api/auth/register',
            data=json.dumps(register_payload),
            content_type='application/json'
        )
        
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'TestPass123!'
            }),
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['access_token']
        
        # Get current user
        response = client.get(
            '/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'test@example.com'
