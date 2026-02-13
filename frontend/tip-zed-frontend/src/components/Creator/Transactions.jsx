import { Inbox, Info, ArrowUpRight, ArrowDownLeft, Filter } from "lucide-react";
import { useState, useMemo } from "react";
import TransactionDetailModal from "./TransactionDetailModal";

const Transactions = ({
  txnData,
  isTransactionsView,
  error,
  setPage,
  loading,
  walletData,
  page,
}) => {
  const [selectedTxn, setSelectedTxn] = useState(null);
  const [filters, setFilters] = useState({
    type: "all",
    status: "all",
    dateRange: "all",
  });

  // Normalize transaction data to handle API response format
  const normalizedTransactions = useMemo(() => {
    if (!txnData?.data) return [];

    return txnData.data.map((txn) => ({
      ...txn,
      // Ensure amount is number
      amount:
        typeof txn.amount === "string" ? parseFloat(txn.amount) : txn.amount,
      fee: typeof txn.fee === "string" ? parseFloat(txn.fee) : txn.fee,
      // Map transactionType to a consistent type for filtering
      type: mapTransactionType(txn.transactionType || txn.type),
      typeDisplay: txn.typeDisplay || txn.transactionType,
      // Ensure status is lowercase for consistent filtering
      status: (txn.status || "").toLowerCase(),
      statusDisplay: txn.statusDisplay || txn.status,
      // Use consistent date field
      createdAt: txn.createdAt || txn.date,
    }));
  }, [txnData]);

  const filteredTransactions = useMemo(() => {
    return normalizedTransactions.filter((txn) => {
      // Filter by Type
      const matchType = filters.type === "all" || txn.type === filters.type;

      // Filter by Status
      const matchStatus =
        filters.status === "all" || txn.status === filters.status.toLowerCase();

      // Filter by Date Range
      let matchDate = true;
      const txnDate = new Date(txn.createdAt);
      const now = new Date();

      if (filters.dateRange === "today") {
        matchDate = txnDate.toDateString() === now.toDateString();
      } else if (filters.dateRange === "7days") {
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(now.getDate() - 7);
        matchDate = txnDate >= sevenDaysAgo;
      } else if (filters.dateRange === "30days") {
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(now.getDate() - 30);
        matchDate = txnDate >= thirtyDaysAgo;
      }

      return matchType && matchStatus && matchDate;
    });
  }, [normalizedTransactions, filters]);

  // Calculate total pages from count (assuming 10 per page)
  const totalPages = useMemo(() => {
    if (!txnData?.count) return 1;
    return Math.ceil(txnData.count / 10);
  }, [txnData]);

  const handleResetFilters = () => {
    setFilters({ type: "all", status: "all", dateRange: "all" });
  };

  return (
    <div className="bg-white rounded-[2rem] border border-gray-100 shadow-sm overflow-hidden flex flex-col h-full">
      {/* Header */}
      <div className="p-8 border-b border-gray-50 flex justify-between items-center">
        <h2 className="text-xl font-black text-gray-900 tracking-tight">
          {isTransactionsView ? "Full Statement" : "Recent Activity"}
        </h2>
        {isTransactionsView && loading && <LoaderSpin />}
      </div>

      {/* Filter UI Bar */}
      <div className="p-4 border-b border-gray-100 bg-gray-50/30 flex flex-wrap items-end gap-3">
        <FilterSelect
          label="Type"
          value={filters.type}
          onChange={(v) => setFilters((prev) => ({ ...prev, type: v }))}
          options={[
            { value: "all", label: "All Types" },
            { value: "cash_in", label: "Cash In" },
            { value: "fee", label: "Fees" },
            { value: "payout", label: "Payouts" },
          ]}
        />

        <FilterSelect
          label="Status"
          value={filters.status}
          onChange={(v) => setFilters((prev) => ({ ...prev, status: v }))}
          options={[
            { value: "all", label: "All Status" },
            { value: "completed", label: "Completed" },
            { value: "pending", label: "Pending" },
            { value: "failed", label: "Failed" },
          ]}
        />

        <FilterSelect
          label="Timeframe"
          value={filters.dateRange}
          onChange={(v) => setFilters((prev) => ({ ...prev, dateRange: v }))}
          options={[
            { value: "all", label: "All Time" },
            { value: "today", label: "Today" },
            { value: "7days", label: "Last 7 Days" },
            { value: "30days", label: "Last 30 Days" },
          ]}
        />

        <button
          onClick={handleResetFilters}
          className="ml-auto px-3 py-2 text-xs font-bold text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-1"
        >
          <Filter size={12} /> Reset
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto flex-grow">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50/50 border-b border-gray-100">
              <th className="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-wider">
                Date
              </th>
              <th className="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-wider text-right">
                Amount
              </th>
              <th className="w-10"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {error ? (
              <tr>
                <td
                  colSpan="5"
                  className="py-16 text-center text-red-500 font-bold text-sm bg-red-50/10"
                >
                  Unable to load transactions. Please try again.
                </td>
              </tr>
            ) : filteredTransactions.length > 0 ? (
              filteredTransactions.map((txn) => (
                <TransactionRow
                  key={txn.id}
                  txn={txn}
                  currency={walletData?.currency || "ZMW"}
                  onClick={() => setSelectedTxn(txn)}
                />
              ))
            ) : (
              <EmptyState />
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination - Fixed logic */}
      {isTransactionsView && totalPages > 1 && (
        <div className="p-4 bg-gray-50 border-t border-gray-100 flex justify-between items-center sticky bottom-0">
          <button
            disabled={page === 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            className="px-4 py-2 text-xs font-bold text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            Previous
          </button>
          <span className="text-xs font-bold text-gray-500">
            Page <span className="text-gray-900">{page}</span> of {totalPages}
          </span>
          <button
            disabled={page >= totalPages}
            onClick={() => setPage((p) => p + 1)}
            className="px-4 py-2 text-xs font-bold text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            Next
          </button>
        </div>
      )}

      {selectedTxn && (
        <TransactionDetailModal
          transaction={selectedTxn}
          onClose={() => setSelectedTxn(null)}
        />
      )}
    </div>
  );
};

// Helper function to map API transaction types to our filter types
const mapTransactionType = (type) => {
  if (!type) return "unknown";

  const typeMap = {
    CASH_IN: "cash_in",
    FEE: "fee",
    PAYOUT: "payout",
    TRANSFER: "transfer",
    REFUND: "refund",
  };

  return typeMap[type] || type.toLowerCase();
};

/*Sub Components for readability */

const TransactionRow = ({ txn, currency, onClick }) => {
  const isNegative =
    txn.amount < 0 || txn.type === "fee" || txn.type === "payout";
  const absAmount = Math.abs(txn.amount);

  // Format Date safely
  const dateStr = new Date(txn.createdAt).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  // Use typeDisplay if available, otherwise format the type
  const displayType =
    txn.typeDisplay || formatTransactionType(txn.transactionType || txn.type);

  return (
    <tr
      onClick={onClick}
      className="group hover:bg-green-50/30 transition-colors cursor-pointer"
    >
      <td className="px-6 py-4 text-xs font-bold text-gray-500 group-hover:text-gray-700">
        {dateStr}
      </td>

      <td className="px-6 py-4">
        <div className="flex items-center gap-2">
          <div
            className={`p-1.5 rounded-full ${
              isNegative
                ? "bg-orange-100 text-orange-600"
                : "bg-green-100 text-green-600"
            }`}
          >
            {isNegative ? (
              <ArrowDownLeft size={14} />
            ) : (
              <ArrowUpRight size={14} />
            )}
          </div>
          <span className="text-xs font-bold capitalize text-gray-700">
            {displayType}
          </span>
        </div>
      </td>

      <td className="px-6 py-4">
        <StatusBadge status={txn.status} display={txn.statusDisplay} />
      </td>

      <td className="px-6 py-4 text-right">
        <span
          className={`text-sm font-black ${
            isNegative ? "text-gray-900" : "text-green-600"
          }`}
        >
          {isNegative ? "-" : "+"}
          {new Intl.NumberFormat("en-ZM", {
            style: "currency",
            currency: currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          }).format(absAmount)}
        </span>
      </td>

      <td className="px-4 py-4 text-center">
        <Info
          size={16}
          className="text-gray-300 group-hover:text-green-500 transition-colors"
        />
      </td>
    </tr>
  );
};

// Helper to format transaction type for display
export const formatTransactionType = (type) => {
  if (!type) return "Unknown";
  return type
    .toLowerCase()
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};

const FilterSelect = ({ label, value, onChange, options }) => (
  <div className="flex flex-col gap-1.5">
    <label className="text-[10px] font-black uppercase text-gray-400 px-1 tracking-wide">
      {label}
    </label>
    <div className="relative">
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="appearance-none w-full min-w-[140px] text-xs font-bold text-gray-700 border border-gray-200 rounded-xl px-3 py-2.5 bg-white outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all cursor-pointer"
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-400">
        <svg
          className="fill-current h-3 w-3"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
        >
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
  </div>
);

const LoaderSpin = () => (
  <div className="flex items-center gap-2 text-[10px] font-bold text-gray-400 bg-gray-50 px-3 py-1 rounded-full border border-gray-100">
    <div className="animate-spin h-3 w-3 border-2 border-green-500 border-t-transparent rounded-full"></div>
    Syncing...
  </div>
);

const EmptyState = () => (
  <tr>
    <td colSpan="5" className="py-24 text-center">
      <div className="bg-gray-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-gray-100">
        <Inbox className="text-gray-300" size={24} strokeWidth={2} />
      </div>
      <p className="text-gray-900 font-bold text-sm">No transactions found</p>
      <p className="text-gray-400 text-xs mt-1">
        Try adjusting your filters or check back later.
      </p>
    </td>
  </tr>
);

const StatusBadge = ({ status, display }) => {
  const statusLower = (status || "").toLowerCase();

  const styles = {
    completed: "bg-green-100 text-green-700 border-green-200",
    pending: "bg-amber-100 text-amber-700 border-amber-200",
    failed: "bg-red-100 text-red-700 border-red-200",
  };

  const currentStyle =
    styles[statusLower] || "bg-gray-100 text-gray-600 border-gray-200";
  const displayText = display || status || "Unknown";

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-wide border ${currentStyle}`}
    >
      {displayText}
    </span>
  );
};

export default Transactions;
