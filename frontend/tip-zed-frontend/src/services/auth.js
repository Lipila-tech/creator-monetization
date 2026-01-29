// mimics the API contract defined in Issue #8
const MOCK_DELAY = 1000;

export const loginUser = async (email, password) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simulate Validation Logic
      if (email === "creator@example.com" && password === "password") {
        resolve({
          status: "success",
          data: {
            access_token: "mock_jwt_token_123",
          },
        });
      } else if (email === "fan@example.com" && password === "password") {
        resolve({
          status: "success",
          data: {
            access_token: "mock_jwt_token_456",
          },
        });
      } else {
        reject({
          response: {
            data: { message: "Invalid email or password" },
          },
        });
      }
    }, MOCK_DELAY);
  });
};

export const registerUser = async (userData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Basic mock validation
      if (
        !userData.email ||
        !userData.password1 ||
        !userData.password1 ||
        !userData.username ||
        !userData.user_type ||
        !userData.first_name ||
        !userData.last_name
      ) {
        reject({
          response: {
            data: { message: "Missing required fields" },
          },
        });
        return;
      }

      resolve({
        status: "success",
        data: {
          ...userData,
          user_id: "user_new_789",
          user_type: userData.user_type || "creator",
          access_token: "mock_jwt_token_789",
        },
      });
    }, MOCK_DELAY);
  });
};
