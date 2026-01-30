import DashboardLayout from '../layouts/DashboardLayout';
import { useAuth } from '../context/AuthContext';
import { Eye, TrendingUp, DollarSign } from 'lucide-react';

const DashboardHome = () => {
  const { user } = useAuth();

  return (
    <DashboardLayout>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Welcome back, {user?.full_name || 'Creator'}!</h1>
        <p className="text-gray-500">Here is what is happening with your content today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        
        {/* Wallet / Earnings Card */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Earnings</p>
              <h3 className="text-2xl font-bold text-gray-900 mt-2">ZMW 1,250.00</h3>
            </div>
            <div className="p-2 bg-green-50 rounded-lg text-zed-green">
              <DollarSign size={20} />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-zed-green font-medium flex items-center">
              <TrendingUp size={14} className="mr-1" /> +12%
            </span>
            <span className="text-gray-400 ml-2">from last month</span>
          </div>
        </div>

        {/* Page Views Card */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-gray-500">Page Views</p>
              <h3 className="text-2xl font-bold text-gray-900 mt-2">3,405</h3>
            </div>
            <div className="p-2 bg-blue-50 rounded-lg text-blue-600">
              <Eye size={20} />
            </div>
          </div>
        </div>

        {/* Active Supporters Card */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
           <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-gray-500">Active Supporters</p>
              <h3 className="text-2xl font-bold text-gray-900 mt-2">128</h3>
            </div>
            <div className="p-2 bg-purple-50 rounded-lg text-purple-600">
              <TrendingUp size={20} />
            </div>
          </div>
        </div>

      </div>
    </DashboardLayout>
  );
};

export default DashboardHome;