# Frontend App - Tip Zed Monetization MVP

**React web application for creator monetization platform**

User-facing interface for creators to manage profiles, receive payments, and request payouts. Fans discover creators and send payments via mobile money.

---

## 🎯 Overview

Modern React app serving all user roles:
- **Creators** - Profile management, wallet tracking, payout requests
- **Fans** - Discover creators, send payments via mobile money
- **Admins** - Dashboard for approvals and reconciliation

**Tech Stack:**
- React 18
- Redux/Context for state management
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- Jest + React Testing Library

**Responsive Design:**
- Mobile-first (320px+)
- Tested on iPhone 6+, Android, tablets, desktop
- Touch-friendly buttons & forms
- Fast load times (Lighthouse > 80)

---

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html           ← HTML entry point
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── SignupForm.jsx
│   │   │   └── Auth.test.jsx
│   │   ├── Creator/
│   │   │   ├── CreatorProfile.jsx
│   │   │   ├── CreatorDashboard.jsx
│   │   │   ├── WalletCard.jsx
│   │   │   ├── TransactionList.jsx
│   │   │   └── Creator.test.jsx
│   │   ├── Payment/
│   │   │   ├── PaymentForm.jsx
│   │   │   ├── PaymentConfirmation.jsx
│   │   │   ├── PaymentSuccess.jsx
│   │   │   └── Payment.test.jsx
│   │   ├── Payout/
│   │   │   ├── PayoutForm.jsx
│   │   │   ├── PayoutHistory.jsx
│   │   │   └── Payout.test.jsx
│   │   ├── Admin/
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── TransactionViewer.jsx
│   │   │   ├── PayoutApproval.jsx
│   │   │   └── Admin.test.jsx
│   │   ├── Common/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ErrorBoundary.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── Toast.jsx
│   │   └── Shared/
│   │       ├── Button.jsx
│   │       ├── Input.jsx
│   │       ├── Modal.jsx
│   │       └── Card.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── CreatorProfile.jsx
│   │   ├── CreatorDashboard.jsx
│   │   ├── PaymentPage.jsx
│   │   ├── AdminDashboard.jsx
│   │   ├── NotFound.jsx
│   │   └── Unauthorized.jsx
│   ├── services/
│   │   ├── api.js           ← Axios instance & interceptors
│   │   ├── authService.js   ← Auth API calls
│   │   ├── creatorService.js ← Creator API calls
│   │   ├── paymentService.js ← Payment API calls
│   │   ├── walletService.js ← Wallet API calls
│   │   └── payoutService.js ← Payout API calls
│   ├── store/
│   │   ├── authSlice.js     ← Redux auth state
│   │   ├── creatorSlice.js  ← Redux creator state
│   │   ├── walletSlice.js   ← Redux wallet state
│   │   ├── uiSlice.js       ← Redux UI state
│   │   └── store.js         ← Redux store config
│   ├── hooks/
│   │   ├── useAuth.js       ← Auth custom hook
│   │   ├── useFetch.js      ← Data fetching hook
│   │   ├── useForm.js       ← Form handling hook
│   │   └── useLocalStorage.js ← Persistence hook
│   ├── utils/
│   │   ├── validators.js    ← Form validation
│   │   ├── formatters.js    ← Format currency, date
│   │   ├── constants.js     ← App constants
│   │   ├── storage.js       ← localStorage helpers
│   │   └── errors.js        ← Error handling
│   ├── styles/
│   │   ├── index.css        ← Global styles
│   │   ├── tailwind.css     ← Tailwind config
│   │   ├── variables.css    ← CSS variables
│   │   └── responsive.css   ← Responsive utilities
│   ├── App.jsx              ← Main app component
│   ├── App.test.jsx
│   ├── index.jsx            ← React entry point
│   └── index.css
├── tests/
│   ├── integration.test.js  ← Integration tests
│   ├── e2e.test.js          ← End-to-end tests
│   └── fixtures.js          ← Mock data
├── .env.example             ← Environment variables
├── .env.test                ← Test environment
├── package.json             ← Dependencies
├── package-lock.json
├── jest.config.js           ← Jest configuration
├── tailwind.config.js       ← Tailwind configuration
├── .eslintrc                ← ESLint config
└── README.md                ← This file
```

---

## 🚀 Setup

### Prerequisites
- Node.js 16+
- npm 8+ or yarn

### Installation

```bash
# Clone repo
git clone https://github.com/zyambo/creator-monetization.git
cd creator-monetization/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your API endpoint

# Start development server
npm start
```

→ App available at `http://localhost:3000`

---

## 📝 Environment Variables

Create `.env` file:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_API_TIMEOUT=30000

# Auth
REACT_APP_JWT_STORAGE_KEY=Tip Zed_token
REACT_APP_REDIRECT_LOGIN=/login
REACT_APP_REDIRECT_HOME=/

# Features
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_LOGGING=true

# Mobile Money
REACT_APP_MOBILE_MONEY_PROVIDER_1=zamtel
REACT_APP_MOBILE_MONEY_PROVIDER_2=mtn
REACT_APP_MOBILE_MONEY_PROVIDER_3=airtel
REACT_APP_MIN_PAYMENT=5
REACT_APP_MAX_PAYMENT=1000

# URLs
REACT_APP_SUPPORT_EMAIL=support@Tip Zed.com
REACT_APP_TERMS_URL=/terms
REACT_APP_PRIVACY_URL=/privacy
```

---

## 🎨 Pages & Components

### Public Pages
- **Home** - Landing page, call-to-action
- **Creator Profile** - Public creator info, payment button

### Auth Pages
- **Login** - Email + password
- **Signup** - Create account, select role

### Creator Pages
- **Dashboard** - Wallet balance, recent transactions, payout button
- **Profile** - Edit profile, update bank account
- **Payout History** - View past payout requests

### Fan Pages
- **Creator Discovery** - Browse creators
- **Payment** - Initiate payment, confirmation, success

### Admin Pages
- **Dashboard** - Overview, metrics
- **Transactions** - View & filter all payments
- **Payouts** - View & approve payout requests

### Common Components
- **Header** - Navigation, user menu
- **Sidebar** - Mobile navigation
- **LoadingSpinner** - Data loading indicator
- **ErrorBoundary** - Error handling
- **Toast** - Notifications

---

## 🔐 Authentication

### Login Flow
1. User enters email + password
2. Frontend calls `POST /auth/login`
3. Backend returns `access_token` + `refresh_token`
4. Store tokens in localStorage
5. Redirect to dashboard

### Token Management
- Access token: 1 hour expiry
- Refresh token: 7 days expiry
- Auto-refresh before expiry
- Logout clears tokens

### Protected Routes
```jsx
<ProtectedRoute>
  <CreatorDashboard />
</ProtectedRoute>
```

---

## 📡 API Integration

### API Service
```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: process.env.REACT_APP_API_TIMEOUT,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 (refresh token)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Refresh token logic
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Service Layer
```javascript
// services/authService.js
const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

const register = async (data) => {
  const response = await api.post('/auth/register', data);
  return response.data;
};
```

---

## 🎯 State Management

### Redux Store
```javascript
// store.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import creatorReducer from './creatorSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    creator: creatorReducer,
  },
});

export default store;
```

### Usage in Components
```javascript
const { user, isLoading } = useSelector((state) => state.auth);
const dispatch = useDispatch();

dispatch(loginUser({ email, password }));
```

---

## 🧪 Testing

### Run Tests
```bash
npm test
```

### Run Tests with Coverage
```bash
npm test -- --coverage
```

### E2E Testing
```bash
npm run test:e2e
```

### Test Examples

**Unit Test**
```javascript
describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const { getByLabelText } = render(<LoginForm />);
    fireEvent.change(getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    // ... more assertions
  });
});
```

**Integration Test**
```javascript
it('logs in user successfully', async () => {
  // Mock API
  mock.onPost('/auth/login').reply(200, {
    access_token: 'token',
  });
  
  // Render & interact
  const { getByRole } = render(<App />);
  fireEvent.click(getByRole('button', { name: /login/i }));
  
  // Assert
  await waitFor(() => {
    expect(getByText(/dashboard/i)).toBeInTheDocument();
  });
});
```

---

## 📱 Responsive Design

### Breakpoints
- `sm`: 640px (mobile)
- `md`: 768px (tablet)
- `lg`: 1024px (desktop)
- `xl`: 1280px (large desktop)

### Mobile Optimizations
- Touch-friendly buttons (min 44px)
- Readable text (min 16px font)
- Single-column layout
- Fast transitions
- Data-light images

### Testing Responsiveness
```bash
# Test on device
npm start
# Use Chrome DevTools device emulation
# Test on real iPhone 6+, Android device
```

---

## 🎨 Styling

### Tailwind CSS
```jsx
<div className="flex justify-center items-center min-h-screen bg-gray-100">
  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
    Click me
  </button>
</div>
```

### Custom CSS Variables
```css
:root {
  --color-primary: #0066cc;
  --color-success: #10b981;
  --color-error: #ef4444;
  --spacing-unit: 8px;
}
```

---

## 🌐 Accessibility

### WCAG 2.1 Compliance
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast (4.5:1 min)
- Alt text for images

### Testing Accessibility
```bash
npm install -D @testing-library/jest-dom
npm install -D axe-core @axe-core/react
```

---

## 🚀 Build & Deployment

### Build
```bash
npm run build
```

Creates optimized production build in `build/` folder.

### Deploy to Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel --prod
```

### Docker Deployment
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 📊 Performance

### Optimization
- Code splitting (React.lazy)
- Image optimization
- Lazy loading
- Minification
- Caching strategy

### Monitoring
- Lighthouse scores > 80
- Core Web Vitals
- Bundle size < 250KB
- First Contentful Paint < 1.5s

### Check Performance
```bash
npm run build
npm install -g lighthouse
lighthouse http://localhost:3000
```

---

## 🐛 Common Issues

### CORS Errors
```javascript
// Check backend CORS settings
// Frontend .env: REACT_APP_API_URL should match backend CORS_ALLOWED_ORIGINS
```

### Token Expiry Issues
```javascript
// Auto-refresh implemented in api.js
// If still having issues, check refresh endpoint
```

### Build Errors
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 📚 Development Guidelines

### Component Guidelines
- Functional components (hooks)
- One component per file
- Props validation (PropTypes)
- Error boundaries for error handling
- Memoization for performance

### Naming Conventions
- Files: `PascalCase.jsx`
- Functions: `camelCase`
- Constants: `UPPER_CASE`
- CSS classes: `kebab-case`

### Code Quality
- Use ESLint
- Format with Prettier
- 80%+ test coverage
- Storybook for component docs

---

## 📞 Support

**Frontend Issues?** → Contact George or Barnabas

**Need Help?**
- Check [technical architecture](../README.md)
- Review [ISSUE_TEMPLATE_GUIDE.md](../ISSUE_TEMPLATE_GUIDE.md)
- See [EXAMPLE_WEEK1_ISSUES.md](../EXAMPLE_WEEK1_ISSUES.md)

---

## 🤝 Contributing Frontend

Want to help with frontend development?

**See [CONTRIBUTION.md](../CONTRIBUTION.md) for:**
- Branching strategy & commit conventions
- Pull request guidelines
- React/JavaScript code style
- Testing requirements (75%+ coverage)
- Code review process with George & Barnabas

**Code Style:**
- Functional components with hooks
- PropTypes validation
- Tailwind CSS (no custom CSS unless necessary)
- 75% test coverage minimum

**Before Submitting PR:**
```bash
npm run lint
npm test -- --coverage
npm run build
```

**Contact:** George Mugale (frontend lead) or Barnabas Mwaipaya (styling/responsive)

---

**Created:** January 27, 2026  
**Framework:** React 18  
**Styling:** Tailwind CSS  
**Status:** MVP Development
