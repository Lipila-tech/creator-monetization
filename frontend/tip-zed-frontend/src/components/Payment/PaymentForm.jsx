import { useState } from "react";
import { ChevronLeft, Lock, Edit2 } from "lucide-react";
import { detectProvider, PROVIDERS } from "../../utils/mobileMoney";

const PROVIDERS_ARRAY = Object.values(PROVIDERS);

const PaymentForm = ({ amount, onSubmit, onBack }) => {
  // Initialize state from localStorage if available
  const [phone, setPhone] = useState(
    () => localStorage.getItem("saved_phone") || "",
  );
  const [provider, setProvider] = useState(() => {
    const savedProviderId = localStorage.getItem("saved_provider_id");
    return PROVIDERS_ARRAY.find((p) => p.id === savedProviderId) || null;
  });
  const [isManual, setIsManual] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);

  // Auto-detect only if NOT in manual mode and phone changes
  const handlePhoneChange = (e) => {
    const val = e.target.value.replace(/\D/g, ""); // Only numbers
    setPhone(val);

    if (!isManual) {
      const detected = detectProvider(val);
      setProvider(detected);
    }
  };

  const handlePayment = () => {
    if (rememberMe) {
      localStorage.setItem("saved_phone", phone);
      localStorage.setItem("saved_provider_id", provider?.id);
    } else {
      localStorage.removeItem("saved_phone");
      localStorage.removeItem("saved_provider_id");
    }
    onSubmit(phone, provider?.id);
  };

  return (
    <div className="animate-in slide-in-from-right-4 duration-300">
      <button
        onClick={onBack}
        className="flex items-center text-gray-400 hover:text-gray-600 mb-6 text-sm"
      >
        <ChevronLeft size={16} /> Back
      </button>

      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">K{amount}</h2>
        <p className="text-gray-500 text-sm">Confirm payment details</p>
      </div>

      <div className="space-y-4 mb-6">
        {/* Phone Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mobile Number
          </label>
          <div className="relative">
            <input
              type="tel"
              value={phone}
              onChange={handlePhoneChange}
              placeholder="097xxxxxxx"
              className="w-full pl-4 pr-12 py-3.5 text-black bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-zed-green transition-all text-lg tracking-wide"
              maxLength={10}
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2">
              {provider?.logo ? (
                <img
                  src={provider.logo}
                  alt=""
                  className="w-8 h-8 rounded-full object-contain"
                />
              ) : (
                <div className="w-8 h-8 rounded-full bg-gray-100" />
              )}
            </div>
          </div>
        </div>

        {/* Provider Selection */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium text-gray-700">
              Network Provider
            </label>
            <button
              onClick={() => setIsManual(!isManual)}
              className="text-xs text-zed-green font-semibold flex items-center gap-1 hover:underline"
            >
              <Edit2 size={12} /> {isManual ? "Detect Network" : "Select Network"}
            </button>
          </div>

          {isManual ? (
            <div className="grid grid-cols-3 gap-2">
              {PROVIDERS_ARRAY.map((p) => {
                return <>{p.id}</>;
              })}
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-3">
              {PROVIDERS_ARRAY.map((p) => {
                const isSelected = provider?.id === p.id;

                // Mapping brand colors for the active state
                const brandColors = {
                  MTN_MOMO_ZMB: "bg-[#FFCC00] border-[#FFCC00]", // MTN Yellow
                  AIRTEL_OAPI_ZMB: "bg-[#FF0000] border-[#FF0000]", // Airtel Red
                  ZAMTEL_ZMB: "bg-[#009639] border-[#009639]", // Zamtel Green
                };

                return (
                  <button
                    key={p.id}
                    onClick={() => setProvider(p)}
                    className={`p-4 border-2 rounded-2xl flex flex-col items-center gap-2 transition-all duration-200 ${
                      isSelected
                        ? `${brandColors[p.id] || "bg-zed-green border-zed-green"} shadow-md scale-105`
                        : "border-gray-100 bg-white hover:border-gray-200"
                    }`}
                  >
                    <div
                      className={`p-1 rounded-full ${isSelected ? "bg-white" : "bg-transparent"}`}
                    >
                      <img
                        src={p.logo}
                        alt={p.name}
                        className="w-12 h-12 object-contain"
                      />
                    </div>
                    <span
                      className={`text-[10px] font-black uppercase tracking-wider ${
                        isSelected ? "text-white" : "text-gray-500"
                      }`}
                    >
                      {p.name}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Remember Me Toggle */}
        <label className="flex items-center gap-2 cursor-pointer group">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-zed-green focus:ring-zed-green"
          />
          <span className="text-sm text-gray-500 group-hover:text-gray-700 transition-colors">
            Save details for future tips
          </span>
        </label>
      </div>

      <button
        onClick={handlePayment}
        disabled={!phone || !provider || phone.length < 10}
        className="w-full bg-zed-green text-white py-4 rounded-xl font-bold text-lg hover:bg-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-green-100"
      >
        Tip K{amount}
      </button>

      <div className="mt-4 flex items-center justify-center gap-2 text-gray-400 text-xs">
        <Lock size={12} />
        <span>Secure Payment via pawaPay</span>
      </div>
    </div>
  );
}

export default PaymentForm;
