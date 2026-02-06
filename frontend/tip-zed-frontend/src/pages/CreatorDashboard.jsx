import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { useAuth } from "../hooks/useAuth";
import { getWalletData } from "../services/walletService";
import { Eye, TrendingUp, DollarSign, Calendar, User } from "lucide-react";

const CreatorDashboard = () => {
  const { user } = useAuth();
  const location = useLocation();
  const isTransactionsView = location.pathname === "/dashboard/transactions";

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        // Pass page parameter to the API call
        const response = await getWalletData({ page, limit: 10 });
        setData(response);
      } catch (err) {
        console.error("Error fetching wallet data:", err);
        setError("Failed to load wallet data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [page]); // Re-fetch when page changes

  // Loading Skeleton
  if (loading && !data) {
    return (
      <DashboardLayout title={user.username  ?? ""}>
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 w-1/3 rounded"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="h-32 bg-gray-200 rounded-xl"></div>
            <div className="h-32 bg-gray-200 rounded-xl"></div>
            <div className="h-32 bg-gray-200 rounded-xl"></div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout title={user.username ?? ""}>
        <div className="p-4 bg-red-50 text-red-600 rounded-lg flex items-center justify-between">
          <span>{error}</span>
          <button 
            onClick={() => {
              setError(null);
              setPage(1);
            }}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title={user.username ?? ""}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          {isTransactionsView
            ? "Transaction History"
            : `Welcome back, ${user?.username || "Creator"}!`}
        </h1>
        <p className="text-gray-500">
          {isTransactionsView
            ? "View and manage your incoming payments."
            : "Here is what is happening with your content today."}
        </p>
      </div>

      {/* OVERVIEW (Cards) */}
      {!isTransactionsView && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Wallet Balance */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Current Balance
                </p>
                <h3 className="text-2xl font-bold text-gray-900 mt-2">
                  {data?.currency || 'ZMW'} {data?.balance?.toLocaleString() || '0'}
                </h3>
              </div>
              <div className="p-2 bg-green-50 rounded-lg text-green-600">
                <DollarSign size={20} />
              </div>
            </div>
          </div>

          {/* Total Earnings */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Total Earnings
                </p>
                <h3 className="text-2xl font-bold text-gray-900 mt-2">
                  {data?.currency || 'ZMW'} {data?.totalEarnings?.toLocaleString() || '0'}
                </h3>
              </div>
              <div className="p-2 bg-blue-50 rounded-lg text-blue-600">
                <TrendingUp size={20} />
              </div>
            </div>
          </div>

          {/* Total Transactions */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Total Transactions
                </p>
                <h3 className="text-2xl font-bold text-gray-900 mt-2">
                  {data?.totalTransactions || 0}
                </h3>
              </div>
              <div className="p-2 bg-purple-50 rounded-lg text-purple-600">
                <Eye size={20} />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TRANSACTIONS TABLE */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-900">
            Recent Transactions
          </h2>
          {loading && (
            <div className="flex items-center text-sm text-gray-500">
              <div className="animate-spin mr-2 h-4 w-4 border-2 border-gray-300 border-t-gray-600 rounded-full"></div>
              Loading...
            </div>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px]">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Supporter
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data?.transactions?.length > 0 ? (
                data.transactions.map((txn) => (
                  <tr key={txn.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex items-center">
                        <Calendar size={16} className="mr-2 text-gray-400" />
                        {new Date(txn.date).toLocaleDateString()}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      <div className="flex items-center">
                        <User size={16} className="mr-2 text-gray-400" />
                        {txn.supporter?.name || "Anonymous"}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">
                      {data.currency || 'ZMW'} {txn.amount?.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          txn.status === "completed"
                            ? "bg-green-100 text-green-800"
                            : txn.status === "pending"
                              ? "bg-yellow-100 text-yellow-800"
                              : "bg-red-100 text-red-800"
                        }`}
                      >
                        {txn.status}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan="4"
                    className="px-6 py-8 text-center text-gray-500"
                  >
                    No transactions found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        {data?.pagination && data.pagination.pages > 1 && (
          <div className="p-4 border-t border-gray-100 flex flex-col sm:flex-row justify-between items-center gap-4">
            <button
              disabled={page === 1 || loading}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              className="w-full sm:w-auto px-4 py-2 border rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
            >
              Previous
            </button>
            <span className="text-sm text-gray-600">
              Page {data.pagination.page} of {data.pagination.pages}
            </span>
            <button
              disabled={page >= data.pagination.pages || loading}
              onClick={() => setPage((p) => p + 1)}
              className="w-full sm:w-auto px-4 py-2 border rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default CreatorDashboard;