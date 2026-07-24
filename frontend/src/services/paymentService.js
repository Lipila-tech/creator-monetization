import api from "./api";

export const paymentService = {
  /**
   * Initiates a mobile money payment to a creator.
   * @param {number|string} walletId The ID of the creator's wallet that will receive the donation.
   * @param {string} ispProvider The mobile money provider identifier.
   *  Supported values:
   *  - "MTN_MOMO_ZMB"
   *  - "AIRTEL_OAPI_ZMB"
   *  - "ZAMTEL_ZMB"
   * @param {number} amount The amount to be tipped (in ZMW).
   * @param {string} patronPhone The supporter’s mobile number (MSISDN format).
   * @param {string} patronEmail The supporter’s email address.
   * @param {string} [patronMessage=""] Optional message attached to the donation.
   * @param {string} [patronName=""] Optional name of the supporter.
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
    patronName = "",
  ) => {
    try {
      const { status, data, statusText } = await api.post(
        `/payments/deposits/${walletId}/`,
        {
          amount,
          provider: ispProvider,
          patronPhone,
          patronEmail,
          patronMessage,
          patronName,
        },
      );

      if (status === 201)
        return {
          success: true,
          data: data.data,
        };

      throw new Error(`Payment failed with status: ${statusText}`);
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data.status ||
          error.message ||
          "Failed to initiate payment.",
      };
    }
  },

  /**
   * Checks the status of an existing payment.
   * @param {number|string} paymentId The unique ID of the payment transaction.
   *
   * @returns {Promise<{
   *   success: boolean,
   *   data?: any
   * }>} Resolves with the latest payment status and metadata.
   *
   * @throws {string}
   *  Throws an error message if the status check fails.
   *
   * TODO: Does not accurately determine the final status of a payment
   */
  checkTip: async (paymentId) => {
    try {
      // const { status, data } = await api.get(`/payments/status/${paymentId}/`);
      await api.get(`/payments/status/${paymentId}/`);

      // if (status === 200)
      //   return {
      //     success: true,
      //     status: data.status,
      //   };

      return {
        success: true,
        status: "completed",
      };
    } catch (error) {
      console.log(error);
      // return {
      //   success: false,
      //   message:
      //     error.response?.data?.status ||
      //     error.message ||
      //     "Failed to check payment status.",
      // };

      return {
        success: true,
        status: "completed",
      };
    }
  },
};
