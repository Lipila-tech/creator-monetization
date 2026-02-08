import {
  CheckCircle,
  AlertCircle,
  RefreshCw,
  Smartphone,
  Clock,
  Loader2,
} from "lucide-react";

export default function PaymentStatus({
  status,
  amount,
  error,
  isLoading,
  onRetry,
  onVerify,
  onClose,
}) {
  // PROCESSING STATE (Action Required)
  if (status === "PROCESSING") {
    return (
      <div className="text-center py-6">
        <div className="relative inline-block mb-6">
          <div className="relative bg-blue-50 p-4 rounded-full">
            <Smartphone size={48} className="text-blue-600" />
          </div>
        </div>

        <h3 className="text-xl font-bold text-gray-900 mb-2">
          Authorize Payment
        </h3>
        <p className="text-gray-500 text-sm max-w-xs mx-auto mb-8">
          A prompt has been sent to your phone. Please enter your PIN to send{" "}
          <span className="font-bold text-gray-900">K{amount}</span>.
        </p>

        <div className="flex flex-col gap-3">
          <button
            onClick={onVerify}
            disabled={isLoading}
            className="w-full bg-zed-black text-white py-3.5 rounded-xl font-bold hover:bg-gray-800 transition-colors flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <Loader2 className="animate-spin" size={20} />
            ) : (
              "I've Completed Payment"
            )}
          </button>

          <button
            onClick={onRetry}
            className="w-full bg-gray-100 text-gray-700 py-3.5 rounded-xl font-bold hover:bg-gray-200 transition-colors"
          >
            Payment Failed / Retry
          </button>
        </div>
      </div>
    );
  }

  // PENDING STATE (Payment sent but not yet reflected)
  if (status === "PENDING") {
    return (
      <div className="text-center py-8">
        <div className="bg-yellow-50 p-4 rounded-full mb-6 inline-flex">
          <Clock size={48} className="text-yellow-600" />
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          Still Processing
        </h3>
        <p className="text-gray-500 mb-8 px-4">
          Tips can sometimes take a few minutes to reflect. Don't worry, your
          support is on its way!
        </p>
        <button
          onClick={onClose}
          className="w-full bg-zed-black text-white py-3.5 rounded-xl font-bold hover:bg-gray-800"
        >
          Got it
        </button>
      </div>
    );
  }

  // SUCCESS STATE
  if (status === "SUCCESS") {
    return (
      <div className="text-center py-8 animate-in zoom-in duration-300">
        <div className="bg-green-50 p-4 rounded-full mb-6 inline-flex">
          <CheckCircle size={48} className="text-green-500" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">Thank You!</h3>
        <p className="text-gray-500 mb-8">
          Your tip of <span className="font-bold text-gray-900">K{amount}</span>{" "}
          has been confirmed.
        </p>
        <button
          onClick={onClose}
          className="w-full bg-zed-black text-white py-3.5 rounded-xl font-bold hover:bg-gray-800"
        >
          Close
        </button>
      </div>
    );
  }

  // ERROR STATE
  if (status === "ERROR") {
    return (
      <div className="text-center py-8">
        <div className="bg-red-50 p-4 rounded-full mb-6 inline-flex">
          <AlertCircle size={48} className="text-red-500" />
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          Initiation Failed
        </h3>
        <p className="text-gray-500 mb-8 max-w-xs mx-auto">{error}</p>
        <button
          onClick={onRetry}
          className="w-full bg-zed-green text-white py-3.5 rounded-xl font-bold hover:bg-green-700 flex items-center justify-center gap-2"
        >
          <RefreshCw size={18} /> Try Again
        </button>
      </div>
    );
  }

  return null;
}
