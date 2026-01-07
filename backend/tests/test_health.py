def test_app_creation(app):
    """Test that app is created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
