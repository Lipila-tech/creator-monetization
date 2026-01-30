import Sidebar from '../components/Common/Sidebar';
import { Menu } from 'lucide-react';
import { useState } from 'react';

const DashboardLayout = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 flex">
      
      {/* Sidebar (Desktop) */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 md:ml-64 transition-all">
        
        {/* Mobile Header */}
        <header className="bg-white shadow-sm h-16 flex items-center justify-between px-4 md:hidden sticky top-0 z-20">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-gray-600">
            <Menu size={24} />
          </button>
        </header>

        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>
      
    </div>
  );
};

export default DashboardLayout;