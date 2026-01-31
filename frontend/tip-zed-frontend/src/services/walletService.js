// import api from './api';

export const getWalletData = async (page = 1) => {
  // Simulate Network Delay (1 second) to test your Skeleton Loader
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Return Dummy Data (Matches your API Contract inner 'data' object)
  return {
    currency: "ZMW",
    balance: 1250.00,
    total_earnings: 4500.00,
    total_transactions: 56,
    
    // Toggle these transactions to test different statuses
    transactions: [
      {
        id: "txn_1",
        date: "2024-01-30T10:00:00Z",
        amount: 50.00,
        type: "tip",
        status: "completed",
        supporter: { name: "Mutale Mwanza" }
      },
      {
        id: "txn_2",
        date: "2024-01-29T14:30:00Z",
        amount: 100.00,
        type: "tip",
        status: "pending",
        supporter: null // Anonymous
      },
      {
        id: "txn_3",
        date: "2024-01-28T09:15:00Z",
        amount: 20.00,
        type: "tip",
        status: "failed",
        supporter: { name: "Chanda Bwalya" }
      },
      {
        id: "txn_4",
        date: "2024-01-27T16:45:00Z",
        amount: 250.00,
        type: "tip",
        status: "completed",
        supporter: { name: "John Doe" }
      },
      {
        id: "txn_5",
        date: "2024-01-26T11:20:00Z",
        amount: 50.00,
        type: "tip",
        status: "completed",
        supporter: { name: "Jane Phiri" }
      }
    ],

    // Dynamic pagination to test your "Next/Prev" buttons
    pagination: {
      total: 56,
      limit: 5,
      page: parseInt(page), // Returns whatever page you asked for
      pages: 12
    }
  };

  /* // --- REAL API CALL ( for when Backend is ready) ---
  try {
    const response = await api.get(`/wallets/me?page=${page}`);
    // Note: If backend returns { status: "success", data: { ... } }
    return response.data.data; 
  } catch (error) {
    throw error.response?.data || { message: "Failed to fetch wallet data" };
  }
  */
};