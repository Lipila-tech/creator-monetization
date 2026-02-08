import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { memo } from 'react';

// memo prevents unnecessary re-renders of the wrapper itself
const ProtectedRoute = memo(({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div 
        className="flex justify-center items-center min-h-screen bg-white"
        aria-busy="true"
        aria-label="Loading authentication"
      >
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-zed-green"></div>
      </div>
    );
  }

  // Auth Redirect with state preservation
  if (!user) {
    //pass the full location object to preserve the 'from' path 
    // for the LoginForm to use after successful sign-in.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Render children
  return <>{children}</>;
});

ProtectedRoute.displayName = 'ProtectedRoute';

export default ProtectedRoute;