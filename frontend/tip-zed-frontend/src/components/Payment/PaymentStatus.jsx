import { Loader2, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';

const PaymentStatus = ({ status, amount, error, onRetry, onClose }) => {
  
  // 1. PROCESSING STATE (Waiting for STK Push)
  if (status === 'PROCESSING') {
    return (
      <div className="text-center py-8">
        <div className="relative inline-block">
          <div className="absolute inset-0 bg-yellow-100 rounded-full animate-ping opacity-75"></div>
          <div className="relative bg-yellow-50 p-4 rounded-full mb-6 inline-flex">
            <Loader2 size={48} className="text-yellow-500 animate-spin" />
          </div>
        </div>
        
        <h3 className="text-xl font-bold text-gray-900 mb-2">Check your phone!</h3>
        <p className="text-gray-500 max-w-xs mx-auto mb-8">
          We've sent a prompt to your mobile number. Please enter your PIN to authorize the payment of <span className="font-bold text-gray-900">K{amount}</span>.
        </p>

        <div className="bg-blue-50 text-blue-700 text-sm px-4 py-3 rounded-lg flex items-start gap-3 text-left">
          <span className="text-xl">💡</span>
          <p>Did the prompt not appear? Dial *115# to check pending transactions manually.</p>
        </div>
      </div>
    );
  }

  // 2. SUCCESS STATE
  if (status === 'SUCCESS') {
    return (
      <div className="text-center py-8 animate-in zoom-in duration-300">
        <div className="bg-green-50 p-4 rounded-full mb-6 inline-flex">
          <CheckCircle size={48} className="text-green-500" />
        </div>
        
        <h3 className="text-2xl font-bold text-gray-900 mb-2">Thank You!</h3>
        <p className="text-gray-500 mb-8">
          Your tip of <span className="font-bold text-gray-900">K{amount}</span> has been received successfully.
        </p>

        <button 
          onClick={onClose}
          className="w-full bg-zed-black text-white py-3.5 rounded-xl font-bold hover:bg-gray-800 transition-colors"
        >
          Done
        </button>
      </div>
    );
  }

  // 3. ERROR STATE
  if (status === 'ERROR') {
    return (
      <div className="text-center py-8">
        <div className="bg-red-50 p-4 rounded-full mb-6 inline-flex">
          <AlertCircle size={48} className="text-red-500" />
        </div>
        
        <h3 className="text-xl font-bold text-gray-900 mb-2">Payment Failed</h3>
        <p className="text-gray-500 mb-8 max-w-xs mx-auto">
          {error || "Something went wrong. Please check your balance or try a different number."}
        </p>

        <div className="flex gap-3">
          <button 
            onClick={onClose}
            className="flex-1 px-4 py-3.5 border border-gray-200 text-gray-700 rounded-xl font-bold hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button 
            onClick={onRetry}
            className="flex-1 bg-zed-green text-white py-3.5 rounded-xl font-bold hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
          >
            <RefreshCw size={18} /> Try Again
          </button>
        </div>
      </div>
    );
  }

  return null;
}

export default PaymentStatus;