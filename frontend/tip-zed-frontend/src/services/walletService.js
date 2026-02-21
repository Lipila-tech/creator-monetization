import api from "./api";

export const walletService = {
  /**
   * Retrieves the authenticated user’s wallet information.
   * @param {number} [page=1] The page number for paginated wallet data.
   *
   * @returns {Promise<any>} Resolves with the user’s wallet data for the given page.
   *
   * @throws {{ message: string }} Throws an error object if the request fails.
   */
  getWalletData: async (page = 1) => {
    try {
      const response = await api.get(`/wallets/me/?page=${page}`);
      return response.data.data;
    } catch (error) {
      throw error.response?.data || { message: "Failed to fetch wallet data" };
    }
  },

  /**
   * Retrieves the authenticated user’s wallet transaction history.
   * @param {number} [page=1] The page number for paginated transaction records.
   *
   * @returns {Promise<any>} Resolves with a paginated list of wallet transactions.
   *
   * @throws {{ message: string }} Throws an error object if the request fails.
   */
  getWalletTxnData: async (page = 1) => {
    try {
      const response = await api.get(`/wallets/transactions/?page=${page}`);
      return response.data;
    } catch (error) {
      throw (
        error.response?.data || {
          message: "Failed to fetch wallet transactions data",
        }
      );
    }
  },

  getPayoutsData: async () => {
    return {
      date: "Oct 25, 2026",
      schedule: "Weekly",
      estimatedAmount: 1250,
    };
  },

  getPayoutAccount: async () => {
    try {
      const response = await api.get(`/wallets/payout-account`);
      return response.data;
    } catch (error) {
      throw (
        error.response?.data || {
          message: "Failed to fetch wallet payout account data",
        }
      );
    }
  },

  updatePayoutAccount: async (accountData) => {
    try {
      const response = await api.put(`/wallets/payout-account`, accountData);
      return response.data;
    } catch (error) {
      throw (
        error.response?.data || {
          message: "Failed to update wallet payout account data",
        }
      );
    }
  },
};
