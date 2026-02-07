import { useEffect, useState, useMemo } from "react";
import { useLocation } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { useAuth } from "../hooks/useAuth";
import { getWalletData } from "../services/walletService";
import { Eye, TrendingUp, DollarSign, RefreshCw, Info   } from "lucide-react";
import TransactionDetailModal from "../components/Creator/TransactionDetailModal";

const CreatorDashboard = () => {
  const { user } = useAuth();
  const location = useLocation();
  const isTransactionsView = location.pathname === "/dashboard/transactions";

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [selectedTxn, setSelectedTxn] = useState(null);
  const [filters, setFilters] = useState({
    type: "all",
    status: "all",
    dateRange: "all", // options: 'all', 'today', '7days', '30days'
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getWalletData({ page, limit: 10, ...filters });
      setData(response);
    } catch (err) {
      setError("Failed to load wallet data. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchData();
  }, [page]);

  const filteredTransactions = useMemo(() => {
    if (!data?.transactions) return [];

    return data.transactions.filter((txn) => {
      // Filter by Type
      const matchType = filters.type === "all" || txn.type === filters.type;

      // Filter by Status
      const matchStatus =
        filters.status === "all" || txn.status === filters.status;

      // Filter by Date Range
      let matchDate = true;
      const txnDate = new Date(txn.date);
      const now = new Date();

      if (filters.dateRange === "today") {
        matchDate = txnDate.toDateString() === now.toDateString();
      } else if (filters.dateRange === "7days") {
        const sevenDaysAgo = new Date(now.setDate(now.getDate() - 7));
        matchDate = txnDate >= sevenDaysAgo;
      } else if (filters.dateRange === "30days") {
        const thirtyDaysAgo = new Date(now.setDate(now.getDate() - 30));
        matchDate = txnDate >= thirtyDaysAgo;
      }

      return matchType && matchStatus && matchDate;
    });
  }, [data, filters]);

  // Loading Skeleton
  if (loading && !data) {
    return (
      <DashboardLayout title={user.username ?? ""}>
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
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {isTransactionsView
              ? "Transaction History"
              : `Welcome back, ${user?.username}!`}
          </h1>
          <p className="text-gray-500">
            {isTransactionsView
              ? "Track your earnings and payouts."
              : "Real-time overview of your wallet."}
          </p>
        </div>
        <button
          onClick={fetchData}
          className="p-2 text-gray-500 hover:text-green-600 transition-colors"
          title="Refresh Data"
        >
          <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
        </button>
      </div>

      {/* OVERVIEW (Cards) */}
      {!isTransactionsView && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-sm font-medium text-gray-500">
              Available Balance
            </p>
            <h3 className="text-2xl font-bold text-green-600 mt-2">
              ZMW {data?.balance?.available?.toLocaleString() || "0.00"}
            </h3>
            {data?.balance?.pending > 0 && (
              <p className="text-xs text-yellow-600 mt-1 font-medium">
                + ZMW {data.balance.pending.toLocaleString()} pending
              </p>
            )}
          </div>
          {/* Wallet Balance */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-gray-500">
                  Current Balance
                </p>
                <h3 className="text-2xl font-bold text-gray-900 mt-2">
                  {data?.currency || "ZMW"}{" "}
                  {data?.balance?.toLocaleString() || "0"}
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
                  {data?.currency || "ZMW"}{" "}
                  {data?.totalEarnings?.toLocaleString() || "0"}
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
        {/* 3. Filter UI Bar */}
        <div className="p-4 border-b border-gray-100 bg-gray-50/50 flex flex-wrap gap-4">
          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-bold uppercase text-gray-400 px-1">
              Type
            </label>
            <select
              value={filters.type}
              onChange={(e) =>
                setFilters((f) => ({ ...f, type: e.target.value }))
              }
              className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white outline-none focus:ring-2 ring-green-500/20"
            >
              <option value="all">All Types</option>
              <option value="tip">Tips Received</option>
              <option value="payout">Payouts</option>
              <option value="fee">Fees</option>
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-bold uppercase text-gray-400 px-1">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) =>
                setFilters((f) => ({ ...f, status: e.target.value }))
              }
              className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white outline-none focus:ring-2 ring-green-500/20"
            >
              <option value="all">All Status</option>
              <option value="completed">Completed</option>
              <option value="pending">Pending</option>
              <option value="failed">Failed</option>
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-bold uppercase text-gray-400 px-1">
              Timeframe
            </label>
            <select
              value={filters.dateRange}
              onChange={(e) =>
                setFilters((f) => ({ ...f, dateRange: e.target.value }))
              }
              className="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-white outline-none focus:ring-2 ring-green-500/20"
            >
              <option value="all">All Time</option>
              <option value="today">Today</option>
              <option value="7days">Last 7 Days</option>
              <option value="30days">Last 30 Days</option>
            </select>
          </div>

          <button
            onClick={() =>
              setFilters({ type: "all", status: "all", dateRange: "all" })
            }
            className="mt-auto mb-1 text-xs text-gray-400 hover:text-green-600 font-medium"
          >
            Reset Filters
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px]">
            {/* ... Thead ... */}
            <tbody className="divide-y divide-gray-100">
              {filteredTransactions.length > 0 ? (
                filteredTransactions.map((txn) => (
                  <tr
                    key={txn.id}
                    onClick={() => setSelectedTxn(txn)}
                    className="hover:bg-gray-50 transition-colors cursor-pointer"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold">
                      <span
                        className={
                          txn.type === "payout"
                            ? "text-red-600"
                            : "text-green-600"
                        }
                      >
                        {txn.type === "payout" ? "-" : "+"} ZMW{" "}
                        {txn.amount?.toFixed(2)}
                      </span>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <Info size={16} className="text-gray-400 inline" />
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan="4"
                    className="px-6 py-12 text-center text-gray-400 italic"
                  >
                    No transactions match your filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
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


      {/* Detail Modal */}
      {selectedTxn && (
        <TransactionDetailModal
          transaction={selectedTxn}
          onClose={() => setSelectedTxn(null)}
        />
      )}

    </DashboardLayout>
  );
};
export default CreatorDashboard;
