# Blog Management API Documentation

## Overview

The Blog Management API is a RESTful API built with Django REST Framework that provides authentication, blog post management, and user features.

**Base URL**: `http://localhost:8000/api/`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication Endpoints

#### 1. User Registration

**POST** `/auth/register/`

Register a new user account.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully. Please check your email to verify your account.",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_verified": false
    }
}
```

**Error Response (400 Bad Request):**
```json
{
    "username": ["A user with that username already exists."],
    "email": ["A user with that email already exists."],
    "password": ["This password is too short. It must contain at least 8 characters."]
}
```

#### 2. User Login

**POST** `/auth/login/`

Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_verified": true
    }
}
```

**Error Response (401 Unauthorized):**
```json
{
    "error": "Invalid credentials."
}
```

#### 3. Check Authentication

**GET** `/auth/check-auth/`

Check if the current user is authenticated.

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Error Response (401 Unauthorized):**
```json
{
    "error": "User not authenticated."
}
```

#### 4. Email Verification

**POST** `/auth/verify-email/<token>/`

Verify user email with the provided token.

**Response (200 OK):**
```json
{
    "message": "Email verified successfully."
}
```

**Error Response (400 Bad Request):**
```json
{
    "error": "Invalid or expired verification token."
}
```

#### 5. Resend Verification Email

**POST** `/auth/resend-verification/`

Resend verification email to user.

**Request Body:**
```json
{
    "email": "john@example.com"
}
```

**Response (200 OK):**
```json
{
    "message": "Verification email sent successfully."
}
```

#### 6. Forgot Password

**POST** `/auth/forgot-password/`

Send password reset email to user.

**Request Body:**
```json
{
    "email": "john@example.com"
}
```

**Response (200 OK):**
```json
{
    "message": "Password reset email sent successfully."
}
```

#### 7. Reset Password

**POST** `/auth/reset-password/<token>/`

Reset password with the provided token.

**Request Body:**
```json
{
    "password": "newpassword123"
}
```

**Response (200 OK):**
```json
{
    "message": "Password reset successfully."
}
```

### Blog Endpoints

#### 1. Get All Posts

**GET** `/blog/posts/`

Get a paginated list of blog posts.

**Query Parameters:**
- `page`: Page number (default: 1)
- `search`: Search in title, content, or author
- `category`: Filter by category ID
- `tag`: Filter by tag ID
- `status`: Filter by status (published, draft, all)

**Response (200 OK):**
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/blog/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Getting Started with Django",
            "slug": "getting-started-with-django",
            "content": "Django is a high-level Python web framework...",
            "excerpt": "Learn how to get started with Django...",
            "author": {
                "id": 1,
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe"
            },
            "category": {
                "id": 1,
                "name": "Programming",
                "slug": "programming"
            },
            "tags": [
                {
                    "id": 1,
                    "name": "Django",
                    "slug": "django"
                }
            ],
            "status": "published",
            "featured_image": "http://localhost:8000/media/blog_images/django.jpg",
            "reading_time": 5,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### 2. Get Post by ID

**GET** `/blog/posts/<id>/`

Get a specific blog post by ID.

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Getting Started with Django",
    "slug": "getting-started-with-django",
    "content": "Django is a high-level Python web framework...",
    "excerpt": "Learn how to get started with Django...",
    "author": {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "category": {
        "id": 1,
        "name": "Programming",
        "slug": "programming"
    },
    "tags": [
        {
            "id": 1,
            "name": "Django",
            "slug": "django"
        }
    ],
    "status": "published",
    "featured_image": "http://localhost:8000/media/blog_images/django.jpg",
    "reading_time": 5,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### 3. Get Post by Slug

**GET** `/blog/posts/by-slug/<slug>/`

Get a specific blog post by slug.

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Getting Started with Django",
    "slug": "getting-started-with-django",
    "content": "Django is a high-level Python web framework...",
    "excerpt": "Learn how to get started with Django...",
    "author": {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "category": {
        "id": 1,
        "name": "Programming",
        "slug": "programming"
    },
    "tags": [
        {
            "id": 1,
            "name": "Django",
            "slug": "django"
        }
    ],
    "status": "published",
    "featured_image": "http://localhost:8000/media/blog_images/django.jpg",
    "reading_time": 5,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### 4. Create Post

**POST** `/blog/posts/`

Create a new blog post (requires authentication).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Request Body:**
```json
{
    "title": "My New Blog Post",
    "content": "This is the content of my new blog post...",
    "excerpt": "A brief excerpt of the post",
    "category": 1,
    "tags": [1, 2],
    "status": "draft",
    "featured_image": null
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "title": "My New Blog Post",
    "slug": "my-new-blog-post",
    "content": "This is the content of my new blog post...",
    "excerpt": "A brief excerpt of the post",
    "author": {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "category": {
        "id": 1,
        "name": "Programming",
        "slug": "programming"
    },
    "tags": [
        {
            "id": 1,
            "name": "Django",
            "slug": "django"
        },
        {
            "id": 2,
            "name": "Python",
            "slug": "python"
        }
    ],
    "status": "draft",
    "featured_image": null,
    "reading_time": 2,
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

#### 5. Update Post

**PATCH** `/blog/posts/<id>/`

Update an existing blog post (requires authentication and ownership).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Request Body:**
```json
{
    "title": "Updated Blog Post Title",
    "content": "Updated content...",
    "status": "published"
}
```

**Response (200 OK):**
```json
{
    "id": 2,
    "title": "Updated Blog Post Title",
    "slug": "updated-blog-post-title",
    "content": "Updated content...",
    "excerpt": "A brief excerpt of the post",
    "author": {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "category": {
        "id": 1,
        "name": "Programming",
        "slug": "programming"
    },
    "tags": [
        {
            "id": 1,
            "name": "Django",
            "slug": "django"
        }
    ],
    "status": "published",
    "featured_image": null,
    "reading_time": 2,
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:30:00Z"
}
```

#### 6. Delete Post

**DELETE** `/blog/posts/<id>/`

Delete a blog post (requires authentication and ownership).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (204 No Content):**
No content returned.

#### 7. Publish Post

**POST** `/blog/posts/<id>/publish/`

Publish a draft post (requires authentication and ownership).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (200 OK):**
```json
{
    "message": "Post published successfully."
}
```

#### 8. Unpublish Post

**POST** `/blog/posts/<id>/unpublish/`

Unpublish a published post (requires authentication and ownership).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (200 OK):**
```json
{
    "message": "Post unpublished successfully."
}
```

#### 9. Get My Posts

**GET** `/blog/my-posts/`

Get current user's posts (requires authentication).

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "My First Post",
            "slug": "my-first-post",
            "content": "This is my first blog post...",
            "excerpt": "A brief excerpt...",
            "author": {
                "id": 1,
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe"
            },
            "category": {
                "id": 1,
                "name": "Programming",
                "slug": "programming"
            },
            "tags": [],
            "status": "published",
            "featured_image": null,
            "reading_time": 3,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

#### 10. Get Categories

**GET** `/blog/categories/`

Get all categories.

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Programming",
        "slug": "programming",
        "description": "Programming and development articles"
    },
    {
        "id": 2,
        "name": "Technology",
        "slug": "technology",
        "description": "Technology news and updates"
    }
]
```

#### 11. Get Tags

**GET** `/blog/tags/`

Get all tags.

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Django",
        "slug": "django"
    },
    {
        "id": 2,
        "name": "Python",
        "slug": "python"
    },
    {
        "id": 3,
        "name": "Web Development",
        "slug": "web-development"
    }
]
```

## Error Codes

### HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **204 No Content**: Request successful, no content returned
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Common Error Responses

#### 400 Bad Request
```json
{
    "field_name": ["Error message for this field."]
}
```

#### 401 Unauthorized
```json
{
    "error": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
    "error": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
    "error": "Resource not found."
}
```

#### 500 Internal Server Error
```json
{
    "error": "An unexpected error occurred."
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **Blog endpoints**: 100 requests per minute
- **File uploads**: 10 requests per minute

## File Uploads

### Image Upload

For featured images, use multipart/form-data:

```
Content-Type: multipart/form-data

{
    "title": "Post Title",
    "content": "Post content",
    "featured_image": <file>
}
```

**Supported formats**: JPG, PNG, GIF
**Maximum size**: 5MB

## Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response format:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/blog/posts/?page=2",
    "previous": null,
    "results": [...]
}
```

## Search and Filtering

### Search

Use the `search` parameter to search in post titles, content, and author names:

```
GET /api/blog/posts/?search=django
```

### Filtering

Filter posts by various criteria:

```
GET /api/blog/posts/?category=1&status=published&tag=2
```

**Available filters:**
- `category`: Category ID
- `tag`: Tag ID
- `status`: published, draft, or all
- `author`: Author ID

## Testing

### Test Endpoints

Run the test suite:

```bash
python manage.py test tests/
```

### Test Coverage

Generate coverage report:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## SDK Examples

### Python (requests)

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Register user
response = requests.post(f"{BASE_URL}/auth/register/", {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
})

# Login
response = requests.post(f"{BASE_URL}/auth/login/", {
    "email": "test@example.com",
    "password": "testpass123"
})

token = response.json()["token"]

# Create post
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/blog/posts/", {
    "title": "My Post",
    "content": "Post content",
    "status": "draft"
}, headers=headers)
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api";

// Register user
const registerResponse = await fetch(`${BASE_URL}/auth/register/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'testuser',
        email: 'test@example.com',
        password: 'testpass123',
        first_name: 'Test',
        last_name: 'User'
    })
});

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        email: 'test@example.com',
        password: 'testpass123'
    })
});

const { token } = await loginResponse.json();

// Create post
const postResponse = await fetch(`${BASE_URL}/blog/posts/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        title: 'My Post',
        content: 'Post content',
        status: 'draft'
    })
});
```

## Support

For API support and questions:

- **Email**: support@blogmanagement.com
- **Documentation**: https://docs.blogmanagement.com
- **GitHub Issues**: https://github.com/your-repo/issues
