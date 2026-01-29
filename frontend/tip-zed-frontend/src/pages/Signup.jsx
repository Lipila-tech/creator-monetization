import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Signup() {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    full_name: "",
    role: "fan",
  });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 8 && formData.confirmPassword.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }


    setIsSubmitting(true);

    const result = await register({
      email: formData.email,
      password: formData.password,
      full_name: formData.full_name,
      role: formData.role,
    });

    if (result.success) alert("Account created!");
    else setError(result.error);

    setIsSubmitting(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-50 via-white to-green-50 p-4">
      <div className="w-full max-w-md backdrop-blur-xl bg-white/80 shadow-2xl rounded-2xl p-8 border border-white/40">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold text-gray-900">
            Join <span className="text-zed-orange">Tip Zed</span> 🚀
          </h2>
          <p className="text-gray-500 text-sm">
            Create your account in seconds
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 text-sm p-3 rounded-lg text-center mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-600">
              Full Name
            </label>
            <input
              name="full_name"
              required
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.full_name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="text-sm font-medium text-gray-600">Email</label>
            <input
              name="email"
              type="email"
              required
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="text-sm font-medium text-gray-600">
              I am a...
            </label>
            <select
              name="role"
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.role}
              onChange={handleChange}
            >
              <option value="fan">Supporter / Fan</option>
              <option value="creator">Creator</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium text-gray-600">
                Password
              </label>
              <input
                name="password"
                type={showPassword ? "text" : "password"}
                required
                className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">
                Confirm
              </label>
              <input
                name="confirmPassword"
                type={showPassword ? "text" : "password"}
                required
                className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
            </div>
          </div>

          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="text-sm text-gray-600 hover:text-white"
          >
            {showPassword ? "Hide Passwords" : "Show Passwords"}
          </button>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3 rounded-lg font-semibold text-white bg-zed-orange hover:bg-orange-600 transition shadow-md disabled:opacity-50"
          >
            {isSubmitting ? "Creating Account..." : "Sign Up"}
          </button>

          <p className="text-center text-sm text-gray-600 mt-4">
            Already have an account?{" "}
            <Link
              to="/login"
              className="text-zed-green font-medium hover:underline"
            >
              Sign in
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
