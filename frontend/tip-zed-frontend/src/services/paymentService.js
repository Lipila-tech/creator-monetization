import api from "./api";

export const paymentService = {
  /**
   * Initiates a mobile money tip/payment to a creator.
   * @param {number|string} walletId The ID of the creator's wallet that will receive the tip.
   * @param {string} ispProvider The mobile money provider identifier.
   *  Supported values:
   *  - "MTN_MOMO_ZMB"
   *  - "AIRTEL_OAPI_ZMB"
   *  - "ZAMTEL_ZMB"
   * @param {number} amount The amount to be tipped (in ZMW).
   * @param {string} patronPhone The supporter’s mobile number (MSISDN format).
   * @param {string} patronEmail The supporter’s email address.
   * @param {string} [patronMessage=""] Optional message attached to the tip.
   *
   * @returns {Promise<{
   *   success: boolean,
   *   data?: any,
   *   message?: string
   * }>} Resolves with a success flag and payment data if the request is accepted,
   *  otherwise resolves with an error message.
   */
  sendTip: async (
    walletId,
    ispProvider,
    amount,
    patronPhone,
    patronEmail,
    patronMessage = "",
  ) => {
    try {
      const response = await api.post(`/payments/deposits/${walletId}/`, {
        amount,
        provider: ispProvider,
        patronPhone,
        patronEmail,
        patronMessage,
      });

      if (response.status === "accepted" || response.status === "success") {
        return {
          success: true,
          data: response.data,
        };
      }

      throw new Error(response.message);
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data ||
          error.message ||
          "Failed to initiate payment.",
      };
    }
  },

  /**
   * Checks the status of an existing tip/payment.
   * @param {number|string} paymentId The unique ID of the payment transaction.
   *
   * @returns {Promise<{
   *   success: boolean,
   *   data?: any
   * }>} Resolves with the latest payment status and metadata.
   *
   * @throws {string}
   *  Throws an error message if the status check fails.
   */
  checkTip: async (paymentId) => {
    try {
      const response = await api.get(`/payments/status/${paymentId}/`);

      return {
        success: response.status,
      };
      
    } catch (error) {
      throw (
        error.response?.data ||
        error.message ||
        "Failed to check payment status."
      );
    }
  },
};
