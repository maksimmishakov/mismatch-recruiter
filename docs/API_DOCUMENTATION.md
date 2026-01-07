# Mismatch Recruiter API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### Health Check
- **GET** `/health`
- **Description**: Check API health status
- **Response**: 200 OK with status information
- **Example**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-07T12:00:00Z"
}
```

### Candidates

#### Get All Candidates
- **GET** `/api/candidates`
- **Description**: Retrieve list of all candidates
- **Authentication**: Required
- **Response**: 200 OK with candidates array

#### Create Candidate
- **POST** `/api/candidates`
- **Description**: Create a new candidate
- **Authentication**: Required
- **Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "position": "Python Developer",
  "status": "pending"
}
```

#### Get Candidate Details
- **GET** `/api/candidates/{id}`
- **Description**: Get specific candidate details
- **Authentication**: Required
- **Response**: 200 OK with candidate object

#### Update Candidate
- **PUT** `/api/candidates/{id}`
- **Description**: Update candidate information
- **Authentication**: Required

#### Delete Candidate
- **DELETE** `/api/candidates/{id}`
- **Description**: Remove a candidate
- **Authentication**: Required
- **Response**: 204 No Content

## Error Responses

- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Access denied
- **404**: Not Found - Resource not found
- **422**: Unprocessable Entity - Validation failed
- **500**: Internal Server Error

