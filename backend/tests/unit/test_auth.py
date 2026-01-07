import pytest

def test_login_success(client):
    '''Test successful login'''
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json

def test_login_invalid_password(client):
    '''Test login with invalid password'''
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_register_success(client):
    '''Test successful registration'''
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    assert response.status_code == 201
    assert response.json['email'] == 'newuser@example.com'
