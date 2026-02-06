import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  // Wait for Auth Check to finish
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-white">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-zed-green"></div>
      </div>
    );
  }

  // If no user, redirect to Login
  if (!user) {
    console.log("away");
    // redirect them back after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If user exists, render the protected page
  return children;
};

export default ProtectedRoute;