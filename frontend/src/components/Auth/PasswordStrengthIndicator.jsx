import { useMemo } from "react";

const PasswordStrengthIndicator = ({ password = "" }) => {
  const strengthMetrics = useMemo(() => {
    if (!password) {
      return { score: 0, label: "No password", color: "bg-gray-300", checklist: [] };
    }

    let score = 0;
    const checks = {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      numbers: /\d/.test(password),
      special: /[!@#$%^&*()_+=;':"\\|,.<>/?{}-]/.test(password),
    };

    Object.values(checks).forEach((check) => {
      if (check) score++;
    });

    const strengthLevels = {
      1: { label: "Weak", color: "bg-red-500" },
      2: { label: "Fair", color: "bg-orange-500" },
      3: { label: "Good", color: "bg-yellow-500" },
      4: { label: "Strong", color: "bg-green-500" },
      5: { label: "Very Strong", color: "bg-green-600" },
    };

    return {
      score,
      label: strengthLevels[score]?.label || "Weak",
      color: strengthLevels[score]?.color || "bg-gray-300",
      checks,
    };
  }, [password]);

  if (!password) return null;

  return (
    <div className="space-y-3 mt-2">
      {/* Strength Bar */}
      <div className="space-y-1">
        <div className="flex justify-between items-center">
          <span className="text-xs font-medium text-gray-600">Password Strength</span>
          <span className={`text-xs font-semibold ${
            strengthMetrics.score <= 2 ? "text-red-600" :
            strengthMetrics.score === 3 ? "text-orange-600" :
            "text-green-600"
          }`}>
            {strengthMetrics.label}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${strengthMetrics.color}`}
            style={{ width: `${(strengthMetrics.score / 5) * 100}%` }}
          />
        </div>
      </div>

      {/* Requirements Checklist */}
      <div className="bg-gray-50 rounded-lg p-3 space-y-2">
        <p className="text-xs font-medium text-gray-700">Requirements:</p>
        <ul className="space-y-1 text-xs">
          <li className="flex items-center gap-2">
            <span className={`w-4 h-4 rounded-full flex items-center justify-center text-white text-xs ${
              strengthMetrics.checks.length ? "bg-green-500" : "bg-gray-300"
            }`}>
              {strengthMetrics.checks.length ? "✓" : ""}
            </span>
            <span className={strengthMetrics.checks.length ? "text-gray-700" : "text-gray-500"}>
              At least 8 characters
            </span>
          </li>
          <li className="flex items-center gap-2">
            <span className={`w-4 h-4 rounded-full flex items-center justify-center text-white text-xs ${
              strengthMetrics.checks.uppercase ? "bg-green-500" : "bg-gray-300"
            }`}>
              {strengthMetrics.checks.uppercase ? "✓" : ""}
            </span>
            <span className={strengthMetrics.checks.uppercase ? "text-gray-700" : "text-gray-500"}>
              One uppercase letter (A-Z)
            </span>
          </li>
          <li className="flex items-center gap-2">
            <span className={`w-4 h-4 rounded-full flex items-center justify-center text-white text-xs ${
              strengthMetrics.checks.lowercase ? "bg-green-500" : "bg-gray-300"
            }`}>
              {strengthMetrics.checks.lowercase ? "✓" : ""}
            </span>
            <span className={strengthMetrics.checks.lowercase ? "text-gray-700" : "text-gray-500"}>
              One lowercase letter (a-z)
            </span>
          </li>
          <li className="flex items-center gap-2">
            <span className={`w-4 h-4 rounded-full flex items-center justify-center text-white text-xs ${
              strengthMetrics.checks.numbers ? "bg-green-500" : "bg-gray-300"
            }`}>
              {strengthMetrics.checks.numbers ? "✓" : ""}
            </span>
            <span className={strengthMetrics.checks.numbers ? "text-gray-700" : "text-gray-500"}>
              One number (0-9)
            </span>
          </li>
          <li className="flex items-center gap-2">
            <span className={`w-4 h-4 rounded-full flex items-center justify-center text-white text-xs ${
              strengthMetrics.checks.special ? "bg-green-500" : "bg-gray-300"
            }`}>
              {strengthMetrics.checks.special ? "✓" : ""}
            </span>
            <span className={strengthMetrics.checks.special ? "text-gray-700" : "text-gray-500"}>
              One special character (!@#$%^&*...)
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default PasswordStrengthIndicator;
