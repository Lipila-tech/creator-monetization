import { useState } from "react";
import { X } from "lucide-react";
import AmountSelector from "./AmountSelector";
import PaymentForm from "./PaymentForm";
import PaymentStatus from "./PaymentStatus";
import { paymentService } from "../../services/paymentService";

const SupportModal = ({ isOpen, onClose, creator }) => {
  const [step, setStep] = useState("AMOUNT"); // AMOUNT | PHONE | PROCESSING | SUCCESS | ERROR
  const [amount, setAmount] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");

  if (!isOpen) return null;

  // select the price
  const handleAmountSelect = (selectedAmount) => {
    setAmount(selectedAmount);
    setStep("PHONE");
  };

  const handlePaymentSubmit = async (phone, providerId) => {
    setStep("PROCESSING");

    console.log(creator);
    try {
      // Call the service we defined earlier
      await paymentService.sendTip(
        creator.walletId,
        providerId,
        amount,
        phone,
        creator.user.email,
      );
      setStep("SUCCESS");
    } catch (err) {
      setErrorMsg(err.message || "Payment failed. Please try again.");
      setStep("ERROR");
    }
  };

  const handleManualConfirm = () => {
    setStep('SUCCESS');
  };

  const handleRetry = () => {
    setStep("PHONE");
    setErrorMsg("");
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
        {/* Modal Header */}
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <div>
            <h3 className="font-bold text-gray-900">Support {creator.name}</h3>
            {step === "PHONE" && (
              <p className="text-xs text-zed-green font-medium">
                Sending K{amount}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-200 rounded-full transition-colors"
          >
            <X size={20} className="text-gray-500" />
          </button>
        </div>

        {/* Dynamic Body */}
        <div className="p-6">
          {step === "AMOUNT" && (
            <AmountSelector onSelect={handleAmountSelect} />
          )}

          {step === "PHONE" && (
            <PaymentForm
              amount={amount}
              onSubmit={handlePaymentSubmit}
              onBack={() => setStep("AMOUNT")}
            />
          )}

          {(step === "PROCESSING" ||
            step === "SUCCESS" ||
            step === "ERROR") && (
            <PaymentStatus
              status={step}
              amount={amount}
              error={errorMsg}
              onRetry={handleRetry}
              onManualConfirm={handleManualConfirm}
              onClose={onClose}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default SupportModal;
