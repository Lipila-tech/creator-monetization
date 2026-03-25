import {
  X,
  CheckCircle2,
  Clock,
  AlertCircle,
  Receipt,
  User,
  Hash,
  CreditCard,
} from "lucide-react";

const TransactionDetailModal = ({ transaction, onClose }) => {
  if (!transaction) return null;

  const statusStyles = {
    completed: {
      icon: CheckCircle2,
      color: "text-green-600",
      bg: "bg-green-50",
    },
    pending: { icon: Clock, color: "text-yellow-600", bg: "bg-yellow-50" },
    failed: { icon: AlertCircle, color: "text-red-600", bg: "bg-red-50" },
  };

  const statusKey = transaction.status?.toLowerCase() || "pending";
  const {
    icon: StatusIcon,
    color,
    bg,
  } = statusStyles[statusKey] || statusStyles.pending;

  // Parse amounts to numbers
  const amount =
    typeof transaction.amount === "string"
      ? parseFloat(transaction.amount)
      : transaction.amount || 0;

  const fee =
    typeof transaction.fee === "string"
      ? parseFloat(transaction.fee)
      : transaction.fee || 0;

  const netAmount = amount - fee;

  // Format display values
  const displayType =
    transaction.typeDisplay ||
    formatTransactionType(transaction.transactionType || transaction.type);
  const displayStatus = transaction.statusDisplay || transaction.status;
  const displayDate = new Date(transaction.createdAt).toLocaleString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 className="text-lg font-bold text-gray-900">
            Transaction Details
          </h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        {/* Amount Section */}
        <div className={`p-8 text-center ${bg}`}>
          <div className={`inline-flex p-3 rounded-full ${bg} mb-3`}>
            <StatusIcon size={32} className={color} />
          </div>
          <h2 className="text-3xl font-bold text-gray-900">
            {new Intl.NumberFormat("en-ZM", {
              style: "currency",
              currency: "ZMW",
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            }).format(Math.abs(amount))}
          </h2>
          <p
            className={`text-sm font-medium mt-1 uppercase tracking-wider ${color}`}
          >
            {displayStatus}
          </p>
          <p className="text-xs text-gray-500 mt-2">{displayDate}</p>
        </div>

        {/* Details List */}
        <div className="p-6 space-y-4">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <Receipt size={18} />
              <span className="text-sm">Type</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">
              {displayType}
            </span>
          </div>

          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <User size={18} />
              <span className="text-sm">Supporter</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">
              {transaction.supporter?.name ||
                extractSupporterFromReference(transaction.reference) ||
                "Anonymous"}
            </span>
          </div>

          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <CreditCard size={18} />
              <span className="text-sm">Provider</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">
              {transaction.provider || "Mobile Money"}
            </span>
          </div>

          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <Hash size={18} />
              <span className="text-sm">Reference</span>
            </div>
            <span className="text-sm font-mono text-gray-900 break-all max-w-[200px] text-right">
              {transaction.reference || transaction.id}
            </span>
          </div>

          <hr className="border-gray-100 my-2" />

          {/* Fee Breakdown Section - Only show if there's a fee */}
          {fee > 0 && (
            <div className="bg-gray-50 p-4 rounded-lg space-y-2">
              <div className="flex justify-between text-xs text-gray-500">
                <span>Gross Amount</span>
                <span>
                  {new Intl.NumberFormat("en-ZM", {
                    style: "currency",
                    currency: "ZMW",
                  }).format(Math.abs(amount))}
                </span>
              </div>
              <div className="flex justify-between text-xs text-red-500">
                <span>Platform Fee</span>
                <span>
                  -{" "}
                  {new Intl.NumberFormat("en-ZM", {
                    style: "currency",
                    currency: "ZMW",
                  }).format(fee)}
                </span>
              </div>
              <div className="flex justify-between text-sm font-bold text-gray-900 pt-1 border-t border-gray-200">
                <span>Net Earnings</span>
                <span>
                  {new Intl.NumberFormat("en-ZM", {
                    style: "currency",
                    currency: "ZMW",
                  }).format(Math.abs(netAmount))}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Footer Action */}
        <div className="p-6 bg-gray-50 border-t border-gray-100">
          <button
            onClick={onClose}
            className="w-full py-3 bg-white border border-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-100 transition-colors shadow-sm"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

const formatTransactionType = (type) => {
  if (!type) return "Unknown";
  return type
    .toLowerCase()
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};

// for future use - when seeing supporter is a supported feature
const extractSupporterFromReference = (reference) => {
  if (!reference) return null;
  // Example: "PAY-20260212001022-82CE02" might contain supporter info
  return null;
};

export default TransactionDetailModal;
