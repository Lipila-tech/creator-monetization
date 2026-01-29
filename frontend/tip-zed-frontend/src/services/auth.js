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
            user_id: "user_123",
            email: email,
            role: "creator",
            access_token: "mock_jwt_token_123",
            full_name: "Test Creator"
          }
        });
      } else if (email === "fan@example.com" && password === "password") {
        resolve({
          status: "success",
          data: {
            user_id: "user_456",
            email: email,
            role: "fan",
            access_token: "mock_jwt_token_456",
            full_name: "Test Fan"
          }
        });
      } else {
        reject({
          response: {
            data: { message: "Invalid email or password" }
          }
        });
      }
    }, MOCK_DELAY);
  });
};

export const registerUser = async (userData) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Basic mock validation
      if (!userData.email || !userData.password || !userData.full_name) {
         reject({
          response: {
            data: { message: "Missing required fields" }
          }
        });
        return;
      }

      resolve({
        status: "success",
        data: {
          user_id: "user_new_789",
          email: userData.email,
          role: userData.role || "fan",
          access_token: "mock_jwt_token_789",
          full_name: userData.full_name
        }
      });
    }, MOCK_DELAY);
  });
};