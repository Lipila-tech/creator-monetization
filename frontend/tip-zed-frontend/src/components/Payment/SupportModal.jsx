import { useState } from "react";
import { X } from "lucide-react";
import AmountSelector from "./AmountSelector";
import PaymentForm from "./PaymentForm";
import PaymentStatus from "./PaymentStatus";
import { paymentService } from "../../services/paymentService";

const STATUS_MAPPINGS = {
  SUCCESS: ["COMPLETED", "PAID"],
  PROCESSING: [
    "ACCEPTED",
    "PENDING",
    "PROCESSING",
    "CAPTURED",
    "SUBMITTED",
    "REQUIRES_ACTION",
    "REQUIRES_CONFIRMATION",
    "PARTIALLY_CAPTURED",
    "SUBMITTED",
    "IN_RECONCILIATION",
  ],
  ERROR: [
    "REFUNDED",
    "PARTIALLY_REFUNDED",
    "FAILED",
    "REJECTED",
    "DISPUTED",
    "EXPIRED",
    "CANCELLED",
  ],
};

const SupportModal = ({ isOpen, onClose, creator }) => {
  const [step, setStep] = useState("AMOUNT"); // AMOUNT | PHONE | PROCESSING | PENDING | SUCCESS | ERROR
  const [amount, setAmount] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentPaymentId, setCurrentPaymentId] = useState(null);

  if (!isOpen) return null;

  // select the price
  const handleAmountSelect = (selectedAmount) => {
    setAmount(selectedAmount);
    setStep("PHONE");
  };

  const handlePaymentSubmit = async (phone, providerId) => {
    setStep("PROCESSING");
    setErrorMsg("");

    try {
      const { data, success, message } = await paymentService.sendTip(
        creator.walletId,
        providerId,
        amount,
        phone,
        creator.user.email,
      );

      if (success) {
        const { status, depositId } = data.metadata;
        setCurrentPaymentId(depositId);

        if (STATUS_MAPPINGS.SUCCESS.includes(status)) {
          setStep("SUCCESS");
        } else if (STATUS_MAPPINGS.PROCESSING.includes(status)) {
          setStep("PROCESSING");
        } else {
          setStep("ERROR");
          setErrorMsg("Transaction was declined or failed.");
        }
      } else {
        setStep("ERROR");
        setErrorMsg(message || "Something went wrong.");
      }
    } catch (err) {
      setErrorMsg(err.message || "Payment failed. Please try again.");
      setStep("ERROR");
    }
  };

  const handleVerifyStatus = async () => {
    if (currentPaymentId) {
      setLoading(true);
      try {
        const { status, success, message } =
          await paymentService.checkTip(currentPaymentId);

        if (success) {
          if (STATUS_MAPPINGS.SUCCESS.includes(status.toUpperCase())) {
            setStep("SUCCESS");
          } else if (
            STATUS_MAPPINGS.PROCESSING.includes(status.toUpperCase())
          ) {
            setStep("PENDING");
          } else {
            setStep("ERROR");
            setErrorMsg("Transaction was declined or failed.");
          }
        } else {
          setStep("ERROR");
          setErrorMsg(message || "Something went wrong.");
        }
      } catch (err) {
        console.error(err);
        setErrorMsg(
          "We couldn't verify the payment status. It might still be processing.",
        );
        setStep("PENDING");
      } finally {
        setLoading(false);
      }
    } else {
      setErrorMsg("No tip detected.");
    }
  };

  const handleRetry = () => {
    setStep("PHONE");
    setErrorMsg("");
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200 max-h-[90vh] flex flex-col">
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-100 flex justify-between items-center shrink-0">
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

        <div className="p-6 overflow-y-auto">
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
            step === "PENDING" ||
            step === "ERROR") && (
            <PaymentStatus
              status={step}
              amount={amount}
              error={errorMsg}
              isLoading={loading}
              onRetry={handleRetry}
              onVerify={handleVerifyStatus}
              onClose={onClose}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default SupportModal;
