import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Loader2, CheckCircle, XCircle } from "lucide-react";
// import { useAuth } from "@/hooks/useAuth";

const AuthCallback = () => {
  // state machine: 'PROCESSING' | 'SUCCESS' | 'ERROR'
  const [statusState, setStatusState] = useState("PROCESSING");
  const [message, setMessage] = useState("Verifying your account...");
  // const { googleAuth } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const processAuth = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get("code");
      const state = params.get("state") || "login";

      if (!code) {
        setStatusState("ERROR");
        setMessage("No authorization code received. Please try again.");
        setTimeout(() => navigate(`/${state}`), 3000);
        return;
      }

      try {
        // TODO: Replace with actual API call when backend is ready
        localStorage.setItem("google_auth_code", code);
        localStorage.setItem("google_auth_mode", state);

        //  Simulate network delay for the upcoming Thursday integration
        await new Promise((resolve) => setTimeout(resolve, 1500));

        // Dummy API Result
        const dummyResult = { success: true };

        // REAL IMPLEMENTATION (For Thursday):
        // const result = await googleAuth(code);

        if (dummyResult.success) {
          setStatusState("SUCCESS");
          setMessage("Authentication successful! Redirecting...");

          // Redirect to the logged-in experience
          setTimeout(() => navigate("/creator-dashboard"), 2000);
        } else {
          // Simulating a 400/401 Error Response
          setStatusState("ERROR");
          setMessage("Invalid authorization code. Please try again.");

          // Send back to where they came from
          setTimeout(() => navigate(`/${state}`), 3000);
        }
      } catch (error) {
        console.log(error);
        setStatusState("ERROR");
        setMessage("An unexpected error occurred. Please try again.");
        setTimeout(() => navigate(`/${state}`), 3000);
      }
    };

    processAuth();
  }, [location, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-md w-full text-center animate-in fade-in zoom-in duration-300">
        {/* Dynamic Icon */}
        <div className="flex justify-center mb-6">
          {statusState === "PROCESSING" && (
            <div className="p-4 bg-blue-50 rounded-full text-blue-500">
              <Loader2 size={40} className="animate-spin" />
            </div>
          )}
          {statusState === "SUCCESS" && (
            <div className="p-4 bg-green-50 rounded-full text-zed-green">
              <CheckCircle size={40} />
            </div>
          )}
          {statusState === "ERROR" && (
            <div className="p-4 bg-red-50 rounded-full text-red-500">
              <XCircle size={40} />
            </div>
          )}
        </div>

        <h2 className="text-xl font-bold text-gray-900 mb-2">
          Google Authentication
        </h2>

        {/* Dynamic Message */}
        <p
          className={`mb-6 font-medium ${
            statusState === "SUCCESS"
              ? "text-zed-green"
              : statusState === "ERROR"
                ? "text-red-500"
                : "text-gray-600"
          }`}
        >
          {message}
        </p>

        {/* Temporary Code Display (TODO: remove before production) */}
        {statusState === "PROCESSING" && (
          <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 mt-4">
            <p className="text-xs text-gray-500 font-mono break-all">
              Code: {localStorage.getItem("google_auth_code")?.substring(0, 30)}
              ...
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthCallback;
