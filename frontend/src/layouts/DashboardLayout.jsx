import Sidebar from "@/components/Common/Sidebar";
import { Menu } from "lucide-react";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

const DashboardLayout = ({ children, title = "" }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { pathname } = useLocation();

  // use effect to automatically close side bar on path change (when a different dashboard item is selected)
  useEffect(() => {
    // extra time to give thr outer a split second to settle before animation
    const t = setTimeout(() => {
      setIsMobileMenuOpen(false);
    }, 50);

    return () => clearTimeout(t);
  }, [pathname]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row">
      {/* Mobile Header (Only visible on small screens) */}
      <div className="md:hidden bg-white border-b border-gray-200 p-4 flex justify-between items-center sticky top-0 z-20">
        <span className="text-xl font-bold text-green-600">{title}</span>
        <button
          onClick={() => setIsMobileMenuOpen(true)}
          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label="Open menu"
        >
          <Menu size={24} />
        </button>
      </div>

      {/* Sidebar (Hidden on mobile unless toggled, Visible on Desktop) */}
      <div
        className={`
    fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg transform
    transition-transform duration-300 ease-out
    ${isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"}
    md:relative md:translate-x-0 md:shadow-none md:border-r border-gray-200
  `}
      >
        <Sidebar
          onClose={() => setIsMobileMenuOpen(false)}
          isMobile={isMobileMenuOpen}
          showCloseButton={true}
          title={title}
        />
      </div>

      {/* Overlay for mobile when menu is open */}
      <div
        className={`
    fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden
    transition-opacity duration-300
    ${isMobileMenuOpen ? "opacity-100" : "opacity-0 pointer-events-none"}
  `}
        onClick={() => setIsMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <main className="flex-1 p-4 md:p-8 overflow-y-auto h-[calc(100vh-64px)] md:h-screen">
        <div className="max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  );
};

export default DashboardLayout;
