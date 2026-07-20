import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import logo from "@/assets/images/logo.webp";
import { Menu, X } from "lucide-react";

const Header = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Define protected routes
  const isProtectedRoute = ["/creator-dashboard"].includes(pathname);

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/");
      setIsMenuOpen(false);
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const renderAvatar = () => {
    const profileImg = user?.profileImage || user?.photoURL;
    
    if (profileImg && typeof profileImg === "string") {
      return (
        <img
          src={profileImg}
          alt={`${user.name || user.email}'s profile`}
          className="w-9 h-9 rounded-full object-cover border border-gray-200"
          onError={(e) => {
            e.currentTarget.onerror = null;
            e.currentTarget.style.display = 'none';
            if (e.currentTarget.nextSibling instanceof HTMLElement) {
              e.currentTarget.nextSibling.style.display = 'flex';
            }
          }}
        />
      );
    }

    const getInitials = () => {
      if (user?.name) {
        const parts = user.name.split(" ");
        if (parts.length > 1) {
          return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return user.name.substring(0, 2).toUpperCase();
      }
      return user?.email?.[0]?.toUpperCase() || "U";
    };

    return (
      <div className="w-9 h-9 rounded-full bg-zed-green flex items-center justify-center text-white text-sm font-bold uppercase ring-2 ring-white">
        {getInitials()}
      </div>
    );
  };

  const isDashboard = pathname === "/creator-dashboard";

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Branding */}
          <Link to="/" className="flex items-center gap-3 group" onClick={() => setIsMenuOpen(false)}>
            <img 
              src={logo} 
              alt="TipZed Logo" 
              className="h-10 w-10 object-contain group-hover:opacity-80 transition-opacity"
            />
            <span 
              className="text-2xl font-black tracking-tight"
              style={{
                background: "linear-gradient(90deg, #198753 0%, #198753 25%, #FF6600 25%, #FF6600 50%, #000000 50%, #000000 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              TipZed
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {!user ? (
              <>
                <Link to="/creator-catalog" className="text-gray-600 hover:text-zed-green font-medium">
                  Explore
                </Link>
                <Link to="/help-center" className="text-gray-600 hover:text-zed-green font-medium">
                  Help
                </Link>
                <Link
                  to={pathname === "/login" ? "/register" : "/login"}
                  className="bg-zed-orange text-white px-6 py-2 rounded-xl font-bold shadow-sm hover:bg-orange-600 transition-all hover:scale-105"
                >
                  {pathname === "/login" ? "Sign Up" : "Login"}
                </Link>
              </>
            ) : (
              <div className="flex items-center space-x-6">
                {!isDashboard && (
                  <Link
                    to="/creator-dashboard"
                    className="text-sm font-bold text-gray-700 hover:text-zed-green px-4 py-2 rounded-xl transition-all border border-gray-100 hover:border-zed-green/20 bg-gray-50/50"
                  >
                    My Dashboard
                  </Link>
                )}
                <div className="flex items-center space-x-3 pl-6 border-l border-gray-200">
                  <div className="flex flex-col items-end">
                    <button
                      onClick={handleLogout}
                      className="text-[11px] text-gray-400 hover:text-red-500 uppercase tracking-wider font-bold transition-colors"
                    >
                      Logout
                    </button>
                  </div>
                  {renderAvatar()}
                </div>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-500 p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-b border-gray-100 absolute top-16 left-0 w-full shadow-lg z-50 animate-in slide-in-from-top duration-300">
          <div className="px-4 py-6 space-y-4">
            {!user ? (
              <>
              <Link
                to="/"
                className="block text-lg font-bold text-gray-800 hover:text-zed-green py-2 border-b border-gray-50"
                onClick={() => setIsMenuOpen(false)}
              >
              Home
              </Link>
                <Link
                  to="/creator-catalog"
                  className="block text-lg font-bold text-gray-800 hover:text-zed-green py-2 border-b border-gray-50"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Explore
                </Link>
                <Link
                  to="/help-center"
                  className="block text-lg font-bold text-gray-800 hover:text-zed-green py-2 border-b border-gray-50"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Help Center
                </Link>
                <div className="pt-4 flex flex-col gap-3">
                  <Link
                    to="/login"
                    className="w-full bg-gray-100 text-gray-800 py-4 rounded-2xl text-center font-black"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="w-full bg-zed-green text-white py-4 rounded-2xl text-center font-black shadow-lg shadow-green-100"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Get Started
                  </Link>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-center gap-4 mb-6 p-4 bg-gray-50 rounded-2xl">
                  {renderAvatar()}
                  <div className="flex-1 min-w-0">
                    <p className="font-black text-gray-900 truncate">
                      {user.displayName || user.name || "My Account"}
                    </p>
                    <p className="text-xs text-gray-500 truncate">{user.email}</p>
                  </div>
                </div>
                <Link
                  to="/creator-dashboard"
                  className="block text-lg font-bold text-gray-800 hover:text-zed-green py-3 border-b border-gray-50"
                  onClick={() => setIsMenuOpen(false)}
                >
                  My Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left text-lg font-bold text-red-600 py-3"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Header;

