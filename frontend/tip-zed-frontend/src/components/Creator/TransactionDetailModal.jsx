import React from 'react';
import { X, CheckCircle2, Clock, AlertCircle, Receipt, User, Hash, CreditCard } from 'lucide-react';

const TransactionDetailModal = ({ transaction, onClose }) => {
  if (!transaction) return null;

  const statusStyles = {
    completed: { icon: CheckCircle2, color: 'text-green-600', bg: 'bg-green-50' },
    pending: { icon: Clock, color: 'text-yellow-600', bg: 'bg-yellow-50' },
    failed: { icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-50' },
  };

  const { icon: StatusIcon, color, bg } = statusStyles[transaction.status] || statusStyles.pending;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 className="text-lg font-bold text-gray-900">Transaction Details</h3>
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
            ZMW {transaction.amount?.toLocaleString(undefined, { minimumFractionDigits: 2 })}
          </h2>
          <p className={`text-sm font-medium mt-1 uppercase tracking-wider ${color}`}>
            {transaction.status}
          </p>
        </div>

        {/* Details List */}
        <div className="p-6 space-y-4">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <Receipt size={18} />
              <span className="text-sm">Type</span>
            </div>
            <span className="text-sm font-semibold text-gray-900 capitalize">{transaction.type}</span>
          </div>

          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <User size={18} />
              <span className="text-sm">Supporter</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">
              {transaction.supporter?.name || "Anonymous"}
            </span>
          </div>

          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <CreditCard size={18} />
              <span className="text-sm">Provider</span>
            </div>
            <span className="text-sm font-semibold text-gray-900">{transaction.provider || 'Mobile Money'}</span>
          </div>

          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3 text-gray-500">
              <Hash size={18} />
              <span className="text-sm">Reference</span>
            </div>
            <span className="text-sm font-mono text-gray-900">{transaction.id}</span>
          </div>

          <hr className="border-gray-100 my-2" />

          {/* Fee Breakdown Section */}
          <div className="bg-gray-50 p-4 rounded-lg space-y-2">
            <div className="flex justify-between text-xs text-gray-500">
              <span>Gross Amount</span>
              <span>ZMW {transaction.amount?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-xs text-red-500">
              <span>Platform Fee</span>
              <span>- ZMW {(transaction.fee || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm font-bold text-gray-900 pt-1 border-t border-gray-200">
              <span>Net Earnings</span>
              <span>ZMW {(transaction.amount - (transaction.fee || 0)).toFixed(2)}</span>
            </div>
          </div>
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

export default TransactionDetailModal;