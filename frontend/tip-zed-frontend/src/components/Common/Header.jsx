import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

const Header = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  // Define protected routes
  const isProtectedRoute = ["/creator-dashboard"].includes(pathname);

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const renderAvatar = () => {
    if (user?.profileImage) {
      return (
        <img
          src={user.profileImage}
          alt={`${user.firstName || user.email}'s profile`}
          className="w-9 h-9 rounded-full object-cover border border-gray-200"
        />
      );
    }

    const initials =
      user?.firstName && user?.lastName
        ? `${user.firstName[0]}${user.lastName[0]}`
        : user?.email?.[0]?.toUpperCase() || "U";

    return (
      <div className="w-9 h-9 rounded-full bg-zed-green flex items-center justify-center text-white text-sm font-bold uppercase ring-2 ring-white">
        {initials}
      </div>
    );
  };

  const isAuthPage = ["/login", "/register"].includes(pathname);
  const isDashboard = pathname === "/creator-dashboard";

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="flex items-center group">
            <span className="text-2xl font-bold text-zed-green group-hover:opacity-80 transition-opacity">
              TipZed
            </span>
          </Link>

          <div className="flex items-center space-x-4">
            {/* Non-authenticated state */}
            {!user && !isAuthPage && (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  className="text-gray-600 hover:text-zed-green font-medium px-3 py-2"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-zed-orange text-white px-4 py-2 rounded-lg font-medium shadow-sm hover:bg-orange-600 transition-colors"
                >
                  Sign Up
                </Link>
              </div>
            )}

            {/* Authenticated state */}
            {user && (
              <div className="flex items-center space-x-4">
                {/* Dashboard link - show when not on dashboard */}
                {!isDashboard && (
                  <Link
                    to="/creator-dashboard"
                    className="text-sm font-semibold text-gray-700 hover:text-zed-green px-3 py-2 rounded-md transition-colors border border-gray-100 hover:border-zed-green/20 bg-gray-50/50"
                  >
                    My Dashboard
                  </Link>
                )}

                {/* User menu */}
                <div className="flex items-center space-x-3 pl-4 border-l border-gray-200">
                  {/* Always show logout on protected routes */}
                  {(isProtectedRoute || !isDashboard) && (
                    <div className="hidden md:flex flex-col items-end">
                      <button
                        onClick={handleLogout}
                        className="text-[11px] text-gray-400 hover:text-red-500 uppercase tracking-wider font-bold transition-colors"
                        aria-label="Log out"
                      >
                        Logout
                      </button>
                    </div>
                  )}

                  {/* Avatar with dropdown (future enhancement) */}
                  <div className="relative group">
                    <div className="cursor-pointer hover:opacity-80 transition-opacity">
                      {renderAvatar()}
                    </div>

                    {/* Dropdown menu for mobile */}
                    <div className="md:hidden absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                      {!isDashboard && (
                        <Link
                          to="/creator-dashboard"
                          className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                        >
                          My Dashboard
                        </Link>
                      )}
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-50"
                      >
                        Log Out
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Header;
