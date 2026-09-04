import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { sendPasswordResetEmail } from "firebase/auth";
import { auth } from "@/firebase";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const RESEND_COOLDOWN_MS = 60000; // 60 seconds between resends

const ForgotPasswordForm = () => {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [resendCooldown, setResendCooldown] = useState(0);
  const [lastResendTime, setLastResendTime] = useState(null);
  const [validationError, setValidationError] = useState("");

  // Countdown timer for resend button
  useEffect(() => {
    if (resendCooldown <= 0) return;

    const timer = setTimeout(() => {
      setResendCooldown((prev) => prev - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [resendCooldown]);

  const validateEmail = (value) => {
    if (!value.trim()) {
      setValidationError("Email address is required.");
      return false;
    }

    if (!EMAIL_REGEX.test(value.trim())) {
      setValidationError("Please enter a valid email address.");
      return false;
    }

    setValidationError("");
    return true;
  };

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);

    // Clear success message when user modifies email
    if (success) {
      setSuccess(false);
      setError("");
    }

    if (value.trim()) {
      validateEmail(value);
    } else {
      setValidationError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!validateEmail(email)) {
      return;
    }

    // Check resend cooldown
    if (lastResendTime) {
      const timeSinceLastResend = Date.now() - lastResendTime;
      if (timeSinceLastResend < RESEND_COOLDOWN_MS) {
        const secondsLeft = Math.ceil((RESEND_COOLDOWN_MS - timeSinceLastResend) / 1000);
        setError(`Please wait ${secondsLeft} second${secondsLeft !== 1 ? 's' : ''} before requesting another reset email.`);
        return;
      }
    }

    setIsLoading(true);

    try {
      await sendPasswordResetEmail(auth, email.trim());
      setSuccess(true);
      setLastResendTime(Date.now());
      setResendCooldown(RESEND_COOLDOWN_MS / 1000);
      setEmail("");
      setValidationError("");
    } catch (err) {
      console.error("Password reset error:", err);
      
      // Handle specific Firebase errors
      if (err.code === "auth/user-not-found") {
        // Security: Don't reveal if email exists or not
        setError("If an account exists with this email, you'll receive a password reset link.");
        setSuccess(true);
      } else if (err.code === "auth/invalid-email") {
        setError("Please enter a valid email address.");
      } else if (err.code === "auth/too-many-requests") {
        setError("Too many reset attempts. Please try again in a few minutes.");
        setResendCooldown(300); // 5 minute cooldown
        setLastResendTime(Date.now());
      } else {
        setError(err.message || "Failed to send reset email. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6" noValidate={false}>
      {error && (
        <div
          role="alert"
          aria-live="polite"
          className={`text-sm p-4 rounded-lg border transition-all ${
            success && error.includes("account exists")
              ? "bg-green-50 text-green-600 border-green-100"
              : "bg-red-50 text-red-600 border-red-100"
          }`}
        >
          {error}
        </div>
      )}

      {success && !error && (
        <div
          role="alert"
          aria-live="polite"
          className="bg-green-50 text-green-600 text-sm p-4 rounded-lg border border-green-100 transition-all"
        >
          ✓ Password reset email sent! Check your inbox for instructions. It may take a few minutes to arrive.
        </div>
      )}

      {/* Email Input */}
      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Email Address
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          autoComplete="email"
          value={email}
          onChange={handleEmailChange}
          disabled={isLoading || success}
          aria-invalid={validationError ? "true" : "false"}
          aria-describedby={validationError ? "email-error" : undefined}
          className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:border-transparent outline-none transition-all ${
            validationError
              ? "border-red-300 focus:ring-red-500"
              : "border-gray-300 focus:ring-zed-green"
          }`}
          placeholder="you@example.com"
        />
        {validationError && (
          <p id="email-error" className="text-red-600 text-xs mt-1">
            {validationError}
          </p>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || success || (resendCooldown > 0 && !success)}
        className="w-full py-2.5 rounded-lg font-semibold text-white bg-zed-orange hover:bg-orange-600 transition shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg
              className="animate-spin h-5 w-5 text-white"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            Sending...
          </span>
        ) : success ? (
          <>
            ✓ Email Sent{resendCooldown > 0 && ` (Resend in ${resendCooldown}s)`}
          </>
        ) : (
          "Send Reset Link"
        )}
      </button>

      {/* Help text */}
      <div className="bg-blue-50 text-blue-700 text-xs p-3 rounded-lg border border-blue-100">
        💡 <strong>Tip:</strong> Check your spam folder if you don't see the email within a few minutes. The reset link expires in 1 hour.
      </div>

      {/* Link back to login */}
      <div className="text-center text-sm text-gray-500">
        Remember your password?{" "}
        <Link
          to="/login"
          className="text-zed-orange font-medium hover:underline focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zed-orange rounded"
        >
          Back to Login
        </Link>
      </div>
    </form>
  );
};

export default ForgotPasswordForm;
