import pytest

def test_candidate_full_flow(client, auth_token):
    '''Test complete candidate workflow'''
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Create candidate
    candidate_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'skills': ['Python', 'React'],
        'experience_years': 5
    }
    response = client.post('/api/candidates', json=candidate_data, headers=headers)
    assert response.status_code == 201
    candidate_id = response.json['id']
    
    # Get candidate
    response = client.get(f'/api/candidates/{candidate_id}', headers=headers)
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'
    
    # Update candidate
    response = client.put(f'/api/candidates/{candidate_id}', json={
        'experience_years': 6
    }, headers=headers)
    assert response.status_code == 200
    
    # Delete candidate
    response = client.delete(f'/api/candidates/{candidate_id}', headers=headers)
    assert response.status_code == 204
