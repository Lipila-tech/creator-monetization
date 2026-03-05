# Authentication & Multi-Frontend Architecture

This document describes the JWT authentication system and multi-frontend API architecture implemented in this project.

## User Types

### 1. Creator
- **Self-registration**: Can register via the public `/api/v1/auth/register/` endpoint
- **Frontend**: Accesses the creator frontend application
- **Permissions**: Cannot be staff or admin, cannot access admin dashboard
- **Model**: Extends `CustomUser` with a `CreatorProfile` for additional metadata
- **Database Fields**: `user_type='creator'`, `is_staff=False`, `is_superuser=False`


## Registration Endpoint

The `/api/v1/auth/register/` endpoint:
- **Permissions**: `AllowAny` - no authentication required
- **User Type**: All self-registered users are created as `creator` type
- **Request Body**:
  ```json
  {
    "email": "creator@example.com",
    "username": "creator_username",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Response**: Returns user data and JWT tokens (access & refresh)

## JWT Authentication

### Token Endpoints

- **Obtain Token**: `POST /api/v1/auth/token/`
  - Authenticates with email and password
  - Returns access and refresh tokens
  - Custom claims included: `user_type`, `email`, `username`, `is_staff`

- **Refresh Token**: `POST /api/v1/auth/token/refresh/`
  - Refresh access token using refresh token
  - Required when access token expires (15 minutes)

### Token Configuration

- **Access Token Lifetime**: 15 minutes
- **Refresh Token Lifetime**: 7 days
- **Rotation**: Refresh tokens rotate on each refresh
- **Blacklist**: Old refresh tokens are blacklisted

## Social Authentication

### Google OAuth 2.0

Google social login is now supported for seamless user registration and authentication.

**Configuration:**

Add to `.env`:
```env
# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GOOGLE_OAUTH_REDIRECT_URI=https://yourdomain.com/api/v1/auth/google/callback/
```

**Endpoints:**

- **Google Login URL**: `GET /api/v1/auth/google/`
  - Redirects user to Google consent screen
  - User grants permission and returns to callback URI

- **Google Callback**: `POST /api/v1/auth/google/callback/`
  - **Request Body**:
    ```json
    {
      "code": "authorization_code_from_google",
      "state": "state_parameter"
    }
    ```
  - **Response**: Returns user data and JWT tokens (access & refresh)
  - **Auto-registration**: Creates a new `creator` user if email doesn't exist
  - **Auto-login**: If user exists, returns tokens directly

**Frontend Integration:**

```html
<!-- Google Sign-In Button -->
<div id="g_id_onload"
     data-client_id="YOUR_GOOGLE_CLIENT_ID"
     data-callback="handleCredentialResponse">
</div>
<div class="g_id_signin" data-type="standard"></div>

<script>
function handleCredentialResponse(response) {
  // Send credential token to your backend
  fetch('/api/v1/auth/google/callback/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      code: response.credential,
      state: generateState()
    })
  })
  .then(res => res.json())
  .then(data => {
    // Store tokens
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    // Redirect to dashboard
    window.location.href = '/dashboard';
  });
}
</script>
```

**User Accounts:**

- Users created via Google OAuth have `user_type='creator'`
- Email is verified automatically during OAuth
- Users can link multiple authentication methods
- Password is optional for social login users

## Multi-Frontend Support

### API Client Model

The `APIClient` model manages different frontend applications:

**Fields**:
- `id`: UUID - Unique identifier
- `name`: String - Client name (e.g., "Creator Web App", "Admin Dashboard")
- `client_type`: Choice - Type of client (web, mobile, internal, partner)
- `api_key`: String - Unique API key for client identification
- `rate_limit`: Integer - Requests per hour allowed
- `is_active`: Boolean - Enable/disable client access

### Client Identification

Clients can be identified in two ways:

#### 1. API Key Header
```http
GET /api/v1/auth/profile/ HTTP/1.1
X-API-Key: sk_xxxxxxxxxxxxx
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

#### 2. Client ID Header
```http
GET /api/v1/auth/profile/ HTTP/1.1
X-Client-ID: 550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Accessing Client Information

In views, the client information is available via:
```python
def some_view(request):
    if hasattr(request, 'client'):
        client = request.client
        print(f"Request from: {client.name}")
```

### CORS Configuration

Frontend URLs are configured via environment variables:

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3001,https://app.example.com
```

## Rate Limiting

The API implements throttling:
- **Anonymous Users**: 100 requests/hour
- **Authenticated Users**: 1000 requests/hour
- **Per Client**: Enforced based on `APIClient.rate_limit`

## API Versioning

Currently using namespace-based versioning:
- Future versions can be accessed via: `/api/v1/`, `/api/v2/`, etc.

## Custom Permissions

Find custom permissions in `permissions.py`:

## Authentication Methods

- **JWT Authentication**: Primary method for all users
- **Google OAuth**: Supported for creators
- **Future**: Additional social providers, API key authentication, etc.

## API Endpoints
**Base URL**: `https://tipzed.pythonanywhere.com/`

**Check the documentation for API endpoints at:**
- swagger: https://tipzed.pythonanywhere.com/api/v1/schema/swagger-ui/
- redoc: https://tipzed.pythonanywhere.com/api/v1/schema/docs/

**Or Test in Postman Collection:**
- [Postman Collection Link]('#')

## Environment Variables

Create `.env` file and copy required variables from `.env.example`.

## Security Notes

- API Keys should be treated like passwords and rotated regularly
- JWT tokens are short-lived (15 minutes) for security
- Refresh tokens should be stored securely on the client
- CORS should only allow trusted domains in production
- Use HTTPS in production to prevent token interception


## Future Enhancements

- OAuth 2.0 / OpenID Connect support (additional providers)
- Social login (Facebook, GitHub, etc.)
- Two-factor authentication
- API usage analytics per client
- Webhook support for real-time events
- GraphQL support alongside REST
