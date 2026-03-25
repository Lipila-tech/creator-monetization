## 🚀 Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm (v9 or higher)

### Environment Configuration

1. **Copy the environment template:**
```bash
cp .env.dist .env
```

2. **Configure the environment variables in `.env`:**
```env
# The base URL for the API service
# Use '/api/v1' if using a proxy setup
# Use 'http://localhost:8000/api/v1' for local backend development
VITE_API_URL=/api/v1

# Request timeout in milliseconds
VITE_API_TIMEOUT=15000

# API Client Key (obtain from Django Admin panel)
VITE_API_CLIENT_KEY=your_client_key_here
```

**Important:** Make sure to set `VITE_API_URL` before running the development server. The application requires this to connect to the backend API.

### How to Run the Frontend (TipZed)

1. **Navigate to the frontend directory:**
```bash
cd frontend/tip-zed-frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment (if not already done):**
```bash
cp .env.dist .env
# Edit .env with your API configuration
```

4. **Start the development server:**
```bash
npm run dev
```

5. **Open in browser:**
Visit http://localhost:5173 to see the TipZed landing page.

### API Integration

The frontend automatically handles authentication and token refresh:

- **Login/Register endpoints:** All authentication requests are sent to `/api/v1/auth/`
- **Token refresh:** Automatic token refresh is handled when access tokens expire
- **Error handling:** Failed requests with expired tokens automatically trigger refresh token flow

For API configuration issues, verify:
- `VITE_API_URL` is set correctly in `.env`
- The backend service is running and accessible
- `VITE_API_CLIENT_KEY` matches your Django Admin configuration
