# Frontend App - TipZed Monetization MVP

**React web application for creator monetization platform**

User-facing interface for creators to manage profiles, receive payments, and request payouts. Fans discover creators and send payments via mobile money.

---

## Overview
The frontend is built with React and integrates with the backend API to provide a seamless user experience. It supports multiple user roles (creators, fans, admins) and provides responsive design for mobile and desktop.

Modern React app serving all user roles:
- **Creators** - Profile management, wallet tracking, payout requests
- **patrons** - Discover creators, send payments via mobile money
- **Admins** - Dashboard for approvals and reconciliation
- **Guests** - Browse creator profiles (limited access)


**Responsive Design:**
- Mobile-first (320px+)
- Tested on iPhone 6+, Android, tablets, desktop
- Touch-friendly buttons & forms
- Fast load times (Lighthouse > 80)

---

## Setup

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

## Environment Variables

Create `.env.local` and copy keys from .env.dist

---

---

## Authentication

### Login Flow (Email + Password)
1. User enters email + password
2. Frontend calls `POST /auth/login`
3. Backend returns `access_token` + `refresh_token`
4. Store tokens in localStorage
5. Redirect to dashboard

### Google Oauth
1. User clicks "Continue with Google"
2. Frontend redirects to Google OAuth URL
3. User grants permission and is redirected back to frontend
4. Frontend calls `POST /api/v1/auth/social/google/` with authorization code
5. Backend returns `access_token` + `refresh_token` (auto-registers if new user as guest)
6. Store tokens and redirect to dashboard (role selection screen if new user)




### Token Management
- Access token: 1 hour expiry
- Refresh token: 7 days expiry
- Auto-refresh before expiry
- Logout clears tokens

---

## Responsive Design

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

## Styling

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

## Accessibility

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

## Build & Deployment

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

---

## Performance

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
lighthouse http://localhost:5173
```

---

## Common Issues

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

## Development Guidelines

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

## Support

**Frontend Issues?** → Contact George or Barnabas


---

## Contributing

**See [CONTRIBUTION.md](../CONTRIBUTION.md) for:**

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