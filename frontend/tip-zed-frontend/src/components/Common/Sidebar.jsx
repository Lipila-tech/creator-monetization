import { Link, useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, ArrowRightLeft, X, LogOut } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";

const Sidebar = ({
  onClose,
  isMobile = false,
  showCloseButton = false,
  title = "TipZed",
}) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();

  const menuItems = [
    { icon: LayoutDashboard, label: "Overview", path: "/dashboard" },
    {
      icon: ArrowRightLeft,
      label: "Transactions",
      path: "/dashboard/transactions",
    },
  ];

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <div className="h-full flex flex-col bg-white border-r border-gray-100">
      {/* Header Section */}
      <div
        className={`p-6 border-b border-gray-100 flex justify-between items-center ${!showCloseButton && "hidden md:flex"}`}
      >
        <span className="text-xl font-bold text-zed-green">{title}</span>
        {showCloseButton && (
          <button
            onClick={onClose}
            className="md:hidden p-2 text-gray-400 hover:bg-gray-50 rounded-full"
          >
            <X size={20} />
          </button>
        )}
      </div>

      {/* Navigation Section (expands to fill space) */}
      <nav className="flex-1 px-4 py-6 space-y-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => isMobile && onClose?.()}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                isActive
                  ? "bg-zed-green text-white shadow-md shadow-green-100"
                  : "text-gray-500 hover:bg-gray-50 hover:text-gray-900"
              }`}
            >
              <item.icon size={18} strokeWidth={isActive ? 2.5 : 2} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer Section (Fixed the stretched button here) */}
      <div className="p-4 border-t border-gray-50">
        <button
          onClick={handleLogout}
          className="flex items-center justify-center gap-2 w-full px-4 py-3 text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
