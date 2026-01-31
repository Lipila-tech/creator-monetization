import api from "./api";

export const paymentService = {
  // Initialize a tip/donation
  sendTip: async (creatorId, amount, currency = "ZMW") => {
    try {
      const response = await api.post("/payments/tips/initiate/", {
        creator_id: creatorId,
        amount,
        currency,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};