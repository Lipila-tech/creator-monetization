import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { useAuth } from "../hooks/useAuth";
import { walletService } from "../services/walletService";
import {
  TrendingUp,
  DollarSign,
  ArrowUpRight,
  Inbox,
  ReceiptText,
} from "lucide-react";

const CreatorDashboard = () => {
  const { user } = useAuth();
  const { pathname } = useLocation();
  const isTransactionsView = pathname === "/dashboard/transactions";

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await walletService.getWalletData({ page, limit: 10 });
        setData(response);
      } catch (err) {
        console.error(err);
        setError(
          err?.response?.data?.message ||
            "Failed to load wallet data. Please try again.",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [page]);

  // Refined Loading Skeleton
  if (loading && !data) {
    return (
      <DashboardLayout title={user?.username}>
        <div className="animate-pulse space-y-8">
          <div className="space-y-3">
            <div className="h-8 bg-gray-100 w-1/4 rounded-lg"></div>
            <div className="h-4 bg-gray-50 w-1/3 rounded-lg"></div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-32 bg-gray-50 rounded-2xl border border-gray-100"
              ></div>
            ))}
          </div>
          <div className="h-64 bg-gray-50 rounded-2xl border border-gray-100"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error && !data) {
    return (
      <DashboardLayout title={user?.username ?? "Dashboard"}>
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="bg-red-50 border border-red-100 text-red-600 rounded-2xl p-8 max-w-md">
            <AlertCircle size={40} className="mx-auto mb-4" />
            <h2 className="font-black text-lg mb-2">Something went wrong</h2>
            <p className="text-sm font-medium mb-6">{error}</p>

            <button
              onClick={() => window.location.reload()}
              className="bg-red-600 text-white px-5 py-2 rounded-xl text-sm font-bold hover:opacity-90"
            >
              Retry
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title={user?.username ?? "Dashboard"}>
      {/* Page Header */}
      <div className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-gray-900 tracking-tight">
            {isTransactionsView ? "Finance History" : "Dashboard"}
          </h1>
          <p className="text-gray-500 font-medium">
            {isTransactionsView
              ? "A detailed log of your earnings and payouts."
              : `Welcome back, ${user?.username}. Here's your stats.`}
          </p>
        </div>

        {!isTransactionsView && (
          <button className="flex items-center gap-2 bg-zed-green text-white px-5 py-2.5 rounded-xl font-bold shadow-lg shadow-green-100 hover:scale-105 transition-transform active:scale-95 text-sm">
            Request Payout <ArrowUpRight size={18} />
          </button>
        )}
      </div>

      {error && (
        <div className="mb-6 rounded-xl border border-red-100 bg-red-50 px-6 py-4 text-sm font-bold text-red-600 flex items-center gap-3">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

      {/* STAT CARDS (Conditional) */}
      {!isTransactionsView && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          {[
            {
              label: "Current Balance",
              val: data?.balance,
              icon: DollarSign,
              color: "text-zed-green",
              bg: "bg-green-50",
              currency: "ZMW",
            },
            {
              label: "Total Earnings",
              val: data?.totalEarnings,
              icon: TrendingUp,
              color: "text-blue-600",
              bg: "bg-blue-50",
              currency: "ZMW",
            },
            {
              label: "Total Transactions",
              val: data?.totalTransactions,
              icon: ReceiptText,
              color: "text-purple-600",
              bg: "bg-purple-50",
            },
          ].map((stat, idx) => (
            <div
              key={idx}
              className="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-md transition-shadow group"
            >
              <div className="flex justify-between items-start">
                <div
                  className={`${stat.bg} ${stat.color} p-3 rounded-2xl transition-transform group-hover:scale-110`}
                >
                  <stat.icon size={22} />
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest text-gray-400 bg-gray-50 px-2 py-1 rounded">
                  Live
                </span>
              </div>
              <div className="mt-4">
                <p className="text-sm font-bold text-gray-400 uppercase tracking-tight">
                  {stat.label}
                </p>
                <h3 className="text-3xl font-black text-gray-900 mt-1">
                  {stat.label === "Total Transactions"
                    ? stat.val?.toLocaleString() || "0"
                    : typeof stat.val === "number"
                      ? `${data?.currency || ""} ${stat.val.toLocaleString()}`
                      : stat.val}
                </h3>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TRANSACTIONS TABLE */}
      <div className="bg-white rounded-[2rem] border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-8 border-b border-gray-50 flex justify-between items-center">
          <h2 className="text-xl font-black text-gray-900">
            Recent Transactions
          </h2>
          {loading && <LoaderSpin />}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-gray-50/50">
                {["Date", "Supporter", "Amount", "Status"].map((h) => (
                  <th
                    key={h}
                    className="px-8 py-4 text-[10px] font-black uppercase tracking-widest text-gray-400"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {error ? (
                <tr>
                  <td
                    colSpan="4"
                    className="py-16 text-center text-red-500 font-bold"
                  >
                    Failed to load transactions
                  </td>
                </tr>
              ) : data?.transactions?.length > 0 ? (
                data.transactions.map((txn) => (
                  <tr
                    key={txn.id}
                    className="hover:bg-gray-50/50 transition-colors"
                  >
                    <td className="px-8 py-5 text-sm font-bold text-gray-600">
                      {new Date(txn.date).toLocaleDateString("en-GB", {
                        day: "2-digit",
                        month: "short",
                      })}
                    </td>
                    <td className="px-8 py-5">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-zed-green/10 flex items-center justify-center text-zed-green font-bold text-xs">
                          {txn.supporter?.name?.[0] || "A"}
                        </div>
                        <span className="text-sm font-bold text-gray-900">
                          {txn.supporter?.name || "Anonymous"}
                        </span>
                      </div>
                    </td>
                    <td className="px-8 py-5 text-sm font-black text-gray-900">
                      +{data.currency} {txn.amount?.toFixed(2)}
                    </td>
                    <td className="px-8 py-5">
                      <StatusBadge status={txn.status} />
                    </td>
                  </tr>
                ))
              ) : (
                <EmptyState />
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {data?.pagination?.pages > 1 && (
          <div className="p-6 bg-gray-50/30 border-t border-gray-50 flex items-center justify-between">
            <button
              disabled={page === 1 || loading}
              onClick={() => setPage((p) => p - 1)}
              className="text-xs font-black uppercase tracking-widest disabled:opacity-30"
            >
              Previous
            </button>
            <span className="text-xs font-bold text-gray-400">
              Page {page} of {data.pagination.pages}
            </span>
            <button
              disabled={page >= data.pagination.pages || loading}
              onClick={() => setPage((p) => p + 1)}
              className="text-xs font-black uppercase tracking-widest disabled:opacity-30"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

// Sub-components to keep the main code clean
const StatusBadge = ({ status }) => {
  const styles = {
    completed: "bg-green-50 text-green-600 border-green-100",
    pending: "bg-yellow-50 text-yellow-600 border-yellow-100",
    failed: "bg-red-50 text-red-600 border-red-100",
  };
  return (
    <span
      className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter border ${styles[status] || styles.pending}`}
    >
      {status}
    </span>
  );
};

const EmptyState = () => (
  <tr>
    <td colSpan="4" className="py-20 text-center">
      <Inbox className="mx-auto text-gray-200 mb-4" size={48} strokeWidth={1} />
      <p className="text-gray-400 font-bold uppercase text-xs tracking-widest">
        No transactions yet
      </p>
    </td>
  </tr>
);

const LoaderSpin = () => (
  <div className="flex items-center text-xs font-bold text-gray-400 animate-pulse">
    <div className="animate-spin mr-2 h-3 w-3 border-2 border-zed-green border-t-transparent rounded-full"></div>
    Updating...
  </div>
);

export default CreatorDashboard;
