import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const logoutUser = async () => {
    await logout();
    navigate("/");
  };

  // We can hide the login buttons if we are actually ON the login/signup pages
  const isAuthPage =
    location.pathname === "/login" || location.pathname === "/register";
  const isCreatorPage = location.pathname === "/creator-dashboard";
  const isLoggedIn = !!user;

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo - Click to go Home */}
          <Link to="/" className="flex items-center">
            {/* You can add a real <img> logo here later */}
            <span className="text-2xl font-bold text-zed-green">TipZed</span>
          </Link>

          {/* Navigation Links */}
          {!isAuthPage && !isLoggedIn && (
            <div className="flex space-x-4">
              <Link
                to="/login"
                className="text-gray-600 hover:text-zed-green font-medium px-3 py-2 rounded-md transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="bg-zed-orange text-white hover:bg-orange-600 font-medium px-4 py-2 rounded-lg transition-colors shadow-sm"
              >
                Sign Up
              </Link>
            </div>
          )}

          <div className="flex space-x-4">
            {isLoggedIn && (
              <button
                onClick={logoutUser}
                className="bg-zed-orange text-white hover:bg-orange-600 font-medium px-4 py-2 rounded-lg transition-colors shadow-sm"
              >
                Log out
              </button>
            )}

            {!isCreatorPage && isLoggedIn && (
              <Link
                to="/creator-dashboard"
                className="bg-zed-black text-white hover:bg-orange-600 font-medium px-4 py-2 rounded-lg transition-colors shadow-sm"
              >
                My Dashboard
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Header;
