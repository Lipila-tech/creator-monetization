export const paymentService = {
  /**
   * Simulates sending a tip to a creator.
   * @param {number} creatorId - The ID of the creator receiving the tip
   * @param {number} amount - The amount in ZMW
   * @param {string} currency - The currency code (e.g., "ZMW")
   * @param {string} phoneNumber - The user's mobile number
   * @param {string} providerId - The selected provider (mtn, airtel, zamtel)
   */
  sendTip: async (creatorId, amount, currency, phoneNumber, providerId) => {
    console.log(`Initiating payment: K${amount} via ${providerId} (${phoneNumber})`);

    // 1. Simulate Network Delay (2 seconds)
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // 2. Simulate Validation Error
    // Rule: Reject if amount is less than 2
    if (amount < 2) {
      throw new Error("Minimum tip amount is K2.00");
    }

    // Rule: Reject specific "test" numbers to test Error State
    // If you type "0999999999", it will fail.
    if (phoneNumber === "0999999999") {
      throw new Error("Payment provider rejected the transaction. Insufficient funds.");
    }

    // 3. Return Mock Success Response
    return {
      status: "success",
      transaction_id: `TXN-${Date.now()}`,
      message: "Payment initiated successfully. Check your phone for the prompt.",
      data: {
        amount: amount,
        currency: currency,
        provider: providerId,
        timestamp: new Date().toISOString(),
      },
    };
  },
};