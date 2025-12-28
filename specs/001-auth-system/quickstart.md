# Quickstart: Authentication and Access Control System

## Overview
This guide will help you set up and run the authentication and access control system in the existing Docusaurus project.

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- npm or yarn package manager
- Access to backend API (FastAPI) with authentication endpoints
- Database (PostgreSQL/Neon) configured for user storage

## Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart python-oauth2
   ```

3. **Set up environment variables**:
   Create a `.env` file with:
   ```env
   SECRET_KEY=your-super-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   DATABASE_URL=postgresql://user:password@localhost/dbname
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   MAIL_SERVER=smtp.example.com
   MAIL_USERNAME=your_email@example.com
   MAIL_PASSWORD=your_email_password
   ```

4. **Run the backend server**:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

## Frontend Setup

1. **Navigate to the Docusaurus directory**:
   ```bash
   cd frontend/docusaurus
   ```

2. **Install dependencies** (if any new ones are needed):
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment configuration**:
   Create or update `.env` file with API endpoint:
   ```env
   REACT_APP_AUTH_API_ENDPOINT=https://your-backend-api.com/v1/auth
   REACT_APP_API_ENDPOINT=https://your-backend-api.com/v1
   ```

## Running the Development Server

1. **Start the Docusaurus development server**:
   ```bash
   npm run start
   # or
   yarn start
   ```

2. **Access the authentication pages**:
   - Registration: `/register`
   - Login: `/login`
   - Forgot Password: `/forgot-password`
   - Reset Password: `/reset-password`

## Key Components

The authentication system consists of these main React components:

- `AuthContext.js`: Global authentication state management
- `useAuth.js`: Custom hook for authentication state
- `Login.jsx`: Login form component
- `Register.jsx`: Registration form component
- `AuthGuard.jsx`: Route protection component
- `NavbarAuth.jsx`: Navigation bar with auth status
- `OAuthButtons.jsx`: Social login buttons
- `ForgotPassword.jsx`: Password reset request form
- `ResetPassword.jsx`: Password reset form

## Integration with Existing Pages

The auth guard can be applied to protect existing pages:

```jsx
import AuthGuard from '../components/Auth/AuthGuard';

// In your page component
<AuthGuard>
  <ProtectedContent />
</AuthGuard>
```

## Configuration

The authentication system can be configured with props:

```jsx
<AuthGuard
  redirectPath="/login"
  requireAuth={true}
  fallback={<div>Loading...</div>}
>
  <ProtectedPageContent />
</AuthGuard>
```

## Building for Production

1. **Build the Docusaurus site**:
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Serve the built site**:
   ```bash
   npm run serve
   # or
   yarn serve
   ```

## Testing Authentication

1. **Register a new user** at `/register`
2. **Login** at `/login`
3. **Access protected content** to verify authentication works
4. **Test social login** with Google/GitHub buttons
5. **Test password reset** flow
6. **Verify token refresh** functionality

## Troubleshooting

- **Token Issues**: Verify that JWT secrets match between frontend and backend
- **CORS Errors**: Ensure backend allows requests from your frontend origin
- **OAuth Redirects**: Check that OAuth callback URLs are properly configured
- **Database Connection**: Verify database credentials and connectivity
- **Email Issues**: Check SMTP settings for password reset functionality