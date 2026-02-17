import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  ArrowRightLeft,
  X,
  LogOut,
  UserPen,
  UserCog,
} from "lucide-react";
import { useAuth } from "../../hooks/useAuth";
import { useCreatorOnboarding } from "../../hooks/useCreatorOnboarding";

const Sidebar = ({ onClose, showCloseButton = false, title = "TipZed" }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout, user } = useAuth();
  const { missingSteps } = useCreatorOnboarding(user);

  const menuItems = [
    { icon: LayoutDashboard, label: "Overview", path: "/creator-dashboard" },
    {
      icon: ArrowRightLeft,
      label: "Transactions",
      path: "/creator-dashboard/transactions",
    },
    {
      icon: UserPen,
      label: "Edit Profile",
      path: "/creator-dashboard/edit-profile",
    },
    {
      icon: UserCog,
      label: "Guide",
      path: "/creator-dashboard/guide",
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
        className={`p-6 border-b border-gray-100 flex justify-between items-center ${
          !showCloseButton && "hidden md:flex"
        }`}
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

      {/* Navigation Section */}
      <div className="flex-1 overflow-y-auto py-4 px-2 space-y-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          const requiresAttention =
            (item.path === "/creator-dashboard/edit-profile" &&
              missingSteps.find((step) => step.link === item.path)) ||
            (item.path === "/creator-dashboard/guide" &&
              missingSteps.length > 0);

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`relative flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                isActive
                  ? "bg-zed-green text-white shadow-md shadow-green-100"
                  : "text-gray-500 hover:bg-gray-50 hover:text-gray-900"
              }`}
            >
              <div className="relative">
                <item.icon size={18} strokeWidth={isActive ? 2.5 : 2} />

                {requiresAttention && (
                  <span className="absolute -top-1 -right-1 flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500 border-2 border-white"></span>
                  </span>
                )}
              </div>

              {item.label}
            </Link>
          );
        })}
      </div>

      {/* Footer Section - Will now be pushed to the bottom */}
      <div className="p-4 border-t border-gray-50 mt-auto">
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