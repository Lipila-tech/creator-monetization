import api from "./api";

export const paymentService = {
  /**
   * Simulates sending a tip to a creator.
   * @param {number} walletId - The ID of the creator receiving the tip
   * @param {number} ispProvider - The selected provider ("MTN_MOMO_ZMB" "AIRTEL_OAPI_ZMB" "ZAMTEL_ZMB")
   * @param {number} amount - The amount in ZMW
   * @param {string} currency - The currency code (e.g., "ZMW")
   * @param {string} patronPhone - The user's mobile number
   * @param {string} patronEmail -
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
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
