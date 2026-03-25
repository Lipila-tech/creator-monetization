import { useState, useEffect } from "react";
import { walletService } from "@/services/walletService";
import { PROVIDERS } from "@/utils/mobileMoney";
import { detectProvider, validateMobileNumber } from "@/utils/mobileMoney";

const PROVIDERS_ARRAY = Object.values(PROVIDERS);

// Helper to format ISO date strings
const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(dateString));
};

const PayoutAccount = () => {
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [payoutAccount, setPayoutAccount] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    phoneNumber: "",
    accountName: "",
    provider: "",
  });

  // Fetch existing payout account
  useEffect(() => {
    fetchPayoutAccount();
  }, []);

  const fetchPayoutAccount = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await walletService.getPayoutAccount();

      if (response.data) {
        setPayoutAccount(response.data);
        // Pre-fill form with existing data when editing
        setFormData({
          phoneNumber: response.data.phoneNumber || "",
          accountName: response.data.accountName || "",
          provider: response.data.provider || "",
        });
      }
    } catch (err) {
      if (err.response?.status !== 404) {
        setError("Failed to load payout account. Please refresh the page.");
        console.error("Error fetching payout account:", err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePhoneChange = (value) => {
    const detected = detectProvider(value);

    setFormData((prev) => ({
      ...prev,
      phoneNumber: value,
      provider: detected?.id || prev.provider,
    }));
  };

  const validateForm = () => {
    if (
      !formData.phoneNumber ||
      formData.phoneNumber.replace(/\D/g, "").length < 9
    ) {
      setError("Please enter a valid Zambian phone number");
      return false;
    }

    if (!validateMobileNumber(formData.phoneNumber).isValid) {
      setError("Please enter a valid Zambian phone number");
      return false;
    }

    if (!formData.accountName?.trim()) {
      setError("Account name is required");
      return false;
    }
    if (!formData.provider) {
      setError("Please select a mobile money provider");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      const payload = {
        phoneNumber: validateMobileNumber(formData.phoneNumber).formatted,
        accountName: formData.accountName.trim(),
        provider: formData.provider,
      };

      if (payoutAccount) {
        await walletService.updatePayoutAccount(payload);
        setSuccess("Payout account updated successfully!");
      } else {
        await walletService.createPayoutAccount(payload);
        setSuccess("Payout account added successfully!");
      }

      await fetchPayoutAccount();
      setIsEditing(false);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          "Failed to save payout account. Please try again.",
      );
      console.error("Error saving payout account:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setError(null);
    setSuccess(null);
  };

  const handleCancel = () => {
    setIsEditing(false);
    if (payoutAccount) {
      setFormData({
        phoneNumber: payoutAccount.phoneNumber || "",
        accountName: payoutAccount.accountName || "",
        provider: payoutAccount.provider || "",
      });
    }
    setError(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto animate-pulse">
          <div className="mb-8">
            <div className="h-9 bg-gray-200 rounded-md w-48 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded-md w-3/4 max-w-md"></div>
          </div>
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-gray-200 border-gray-100 p-6 space-y-6">
            <div className="h-6 bg-gray-200 rounded-md w-40 mb-2"></div>
            <div>
              <div className="h-4 bg-gray-200 rounded-md w-32 mb-2"></div>
              <div className="h-11 bg-gray-200 rounded-md w-full"></div>
            </div>
            <div>
              <div className="h-4 bg-gray-200 rounded-md w-28 mb-2"></div>
              <div className="h-11 bg-gray-200 rounded-md w-full"></div>
            </div>
            <div>
              <div className="h-4 bg-gray-200 rounded-md w-36 mb-2"></div>
              <div className="h-11 bg-gray-200 rounded-md w-full"></div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <div className="h-11 bg-gray-200 rounded-md flex-1"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const providerConfig = PROVIDERS_ARRAY.find(
    (p) => p.id === payoutAccount?.provider,
  );

  const PROVIDER_STYLES = {
    MTN_MOMO_ZMB: "bg-[#FFCC00] border-[#FFCC00]",
    AIRTEL_OAPI_ZMB: "bg-[#FF0000] border-[#FF0000]",
    ZAMTEL_ZMB: "bg-[#009639] border-[#009639]",
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Alerts */}
        {error && (
          <div className="mb-6 flex items-center justify-between p-4 text-sm text-red-800 rounded-xl bg-red-50 border border-red-100 shadow-sm">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 mr-3 text-red-500"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="font-medium">{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-red-500 hover:text-red-700 transition-colors hover:scale-[1.01] active:scale-[0.98]"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>
        )}

        {success && (
          <div className="mb-6 flex items-center justify-between p-4 text-sm text-green-800 rounded-xl bg-green-50 border border-green-100 shadow-sm">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 mr-3 text-green-500"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="font-medium">{success}</span>
            </div>
            <button
              onClick={() => setSuccess(null)}
              className="text-green-500 hover:text-green-700 transition-colors hover:scale-[1.01] active:scale-[0.98]"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>
        )}

        {/* Main Content */}
        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-gray-200 border-gray-200 overflow-hidden ">
          {!payoutAccount || isEditing ? (
            // Add/Edit Form
            <form onSubmit={handleSubmit} className="p-8 space-y-6">
              <div className="border-b border-gray-100 pb-4 mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  {payoutAccount ? "Edit Payout Account" : "Add Payout Account"}
                </h2>
                <p className="mt-1 text-sm text-gray-500">
                  Ensure these details match your mobile money registration
                  exactly.
                </p>
              </div>

              <div className="space-y-5">
                {/* Phone Number */}
                <div>
                  <label
                    htmlFor="phoneNumber"
                    className="block text-sm font-medium text-gray-700 mb-1.5"
                  >
                    Mobile Money Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    id="phoneNumber"
                    name="phoneNumber"
                    value={formData.phoneNumber}
                    onChange={(e) => handlePhoneChange(e.target.value)}
                    placeholder="0977 123 456"
                    required
                    disabled={submitting}
                    className="w-full px-4 py-2.5 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 focus:border-green-500 focus:bg-white transition-colors disabled:opacity-60 focus:ring-4 focus:ring-green-500/20"
                  />
                  {formData.provider && (
                    <p className="mt-2 text-xs text-green-600 flex items-center gap-1">
                      ✓ Provider detected automatically
                    </p>
                  )}
                </div>

                {/* Account Name */}
                <div>
                  <label
                    htmlFor="accountName"
                    className="block text-sm font-medium text-gray-700 mb-1.5"
                  >
                    Account Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="accountName"
                    name="accountName"
                    value={formData.accountName}
                    onChange={handleInputChange}
                    placeholder="John Doe"
                    required
                    disabled={submitting}
                    className="w-full px-4 py-2.5 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 focus:border-green-500 focus:bg-white transition-colors disabled:opacity-60 focus:ring-4 focus:ring-green-500/20"
                  />
                </div>

                {/* Provider Selection */}
                <div className="grid grid-cols-3 gap-3">
                  {PROVIDERS_ARRAY.map((providerItem) => {
                    const isSelected = formData.provider === providerItem.id;

                    const brandColors = {
                      MTN_MOMO_ZMB: "bg-[#FFCC00] border-[#FFCC00]", // MTN Yellow
                      AIRTEL_OAPI_ZMB: "bg-[#FF0000] border-[#FF0000]", // Airtel Red
                      ZAMTEL_ZMB: "bg-[#009639] border-[#009639]", // Zamtel Green
                    };

                    return (
                      <button
                        key={providerItem.id}
                        type="button"
                        onClick={() =>
                          setFormData((prev) => ({
                            ...prev,
                            provider: providerItem.id,
                          }))
                        }
                        className={`p-4 border-2 rounded-2xl flex flex-col items-center gap-2 transition-all duration-200 ${
                          isSelected
                            ? `${brandColors[providerItem.id] || "bg-green-600 border-green-600"} shadow-md scale-105`
                            : "border-gray-100 bg-white hover:border-gray-200"
                        }`}
                      >
                        <div
                          className={`p-1 rounded-full ${isSelected ? "bg-white" : "bg-transparent"}`}
                        >
                          <img
                            src={providerItem.logo}
                            alt={providerItem.name}
                            className="w-12 h-12 object-contain"
                          />
                        </div>
                        <span
                          className={`text-[10px] font-black uppercase tracking-wider ${
                            isSelected ? "text-white" : "text-gray-500"
                          }`}
                        >
                          {providerItem.name}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Form Actions */}
              <div className="flex flex-col sm:flex-row gap-3 pt-6 mt-6 border-t border-gray-100">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 inline-flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors disabled:opacity-70 disabled:cursor-not-allowed hover:scale-[1.01] active:scale-[0.98]"
                >
                  {submitting && (
                    <svg
                      className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                  )}
                  {submitting
                    ? "Saving details..."
                    : payoutAccount
                      ? "Update Account"
                      : "Add Account"}
                </button>

                {payoutAccount && (
                  <button
                    type="button"
                    onClick={handleCancel}
                    disabled={submitting}
                    className="flex-1 sm:flex-none inline-flex justify-center items-center py-2.5 px-6 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors disabled:opacity-70 hover:scale-[1.01] active:scale-[0.98]"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          ) : (
            // View Account Details
            <div className="p-0">
              <div className="p-6 sm:p-8 border-b border-gray-100 bg-gray-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-3">
                    Active Payout Account
                    {payoutAccount.verified && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200 bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-sm">
                        <svg
                          className="w-3 h-3 mr-1"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                        Verified
                      </span>
                    )}
                  </h2>
                  <p className="mt-1 text-sm text-gray-500">
                    Added on {formatDate(payoutAccount.createdAt)}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={handleEdit}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors hover:scale-[1.01] active:scale-[0.98]"
                >
                  <svg
                    className="mr-2 -ml-1 h-4 w-4 text-gray-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                    />
                  </svg>
                  Edit Details
                </button>
              </div>

              <div className="p-6 sm:p-8">
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Network Provider
                    </dt>
                    <dd className="mt-2 text-sm text-gray-900"></dd>
                    {providerConfig && (
                      <div className="grid grid-cols-3 gap-3">
                        <div
                          className={`
        p-4 border-2 rounded-2xl flex flex-col items-center gap-2
        transition-all duration-300 ease-out
        shadow-lg scale-105
        ${PROVIDER_STYLES[providerConfig.id] ?? "bg-green-600 border-green-600"}
      `}
                        >
                          <div className="p-1 rounded-full bg-white shadow-sm">
                            <img
                              src={providerConfig.logo}
                              alt={providerConfig.name}
                              className="w-12 h-12 object-contain"
                            />
                          </div>

                          <span className="text-[10px] font-black uppercase tracking-wider text-white">
                            {providerConfig.name}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Phone Number
                    </dt>
                    <dd className="mt-2 text-sm text-gray-900 font-medium font-mono text-lg">
                      {payoutAccount.phoneNumber}
                    </dd>
                  </div>

                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Registered Name
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900 font-medium">
                      {payoutAccount.accountName}
                    </dd>
                  </div>

                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Last Updated
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {formatDate(payoutAccount.updatedAt)}
                    </dd>
                  </div>
                </dl>

                <div className="mt-8 bg-blue-50 border border-blue-100 rounded-xl p-4">
                  <div className="flex items-start">
                    <div className="flex-shrink-0 mt-0.5">
                      <svg
                        className="h-5 w-5 text-blue-500"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                    <div className="ml-3 flex-1">
                      <h3 className="text-sm font-medium text-blue-800">
                        Automatic Payouts Enabled
                      </h3>
                      <p className="mt-1 text-sm text-blue-700">
                        Earnings will be securely sent to this account every
                        Friday or whenever your balance reaches K100, whichever
                        occurs first.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Empty State (if no account and not editing) */}
        {!payoutAccount && !isEditing && (
          <div className="mt-6 bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-gray-200 border-gray-200 overflow-hidden">
            <div className="px-6 py-16 sm:p-16 text-center">
              <div className="mx-auto h-20 w-20 text-green-100 bg-green-50 rounded-full flex items-center justify-center mb-6 border border-green-100">
                <svg
                  className="w-10 h-10 text-green-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No payout account set up
              </h3>
              <p className="text-gray-500 mb-8 max-w-sm mx-auto text-sm leading-relaxed">
                Add a mobile money account to start receiving automatic, secure
                payouts for your content directly to your phone.
              </p>
              <button
                type="button"
                onClick={() => setIsEditing(true)}
                className="inline-flex justify-center items-center py-3 px-6 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors hover:scale-[1.01] active:scale-[0.98]"
              >
                <svg
                  className="mr-2 -ml-1 h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                Set Up Payout Account
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PayoutAccount;
