import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Signup() {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: "",
    password1: "",
    password2: "",
    username: "",
    user_type: "creator",
    first_name: "",
    last_name: "",
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

    // VALIDATE PASSWORDS
    if (formData.password1 !== formData.password2) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password1.length < 8 && formData.password2.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }

    // VALIDATE USERNAME
    if (formData.username.length < 2) {
      setError("Username must be at least 2 characters");
      return;
    }

    setIsSubmitting(true);

    const result = await register(formData);

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
              First Name
            </label>
            <input
              name="first_name"
              required
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.first_name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="text-sm font-medium text-gray-600">
              Last Name
            </label>
            <input
              name="last_name"
              required
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.last_name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="text-sm font-medium text-gray-600">
              Username
            </label>
            <input
              name="username"
              required
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.username}
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
              name="user_type"
              className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
              value={formData.user_type}
              onChange={handleChange}
            >
              <option value="creator">Creator</option>
              <option value="fan">Supporter / Fan</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium text-gray-600">
                Password
              </label>
              <input
                name="password1"
                type={showPassword ? "text" : "password"}
                required
                className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
                value={formData.password1}
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600">
                Confirm
              </label>
              <input
                name="password2"
                type={showPassword ? "text" : "password"}
                required
                className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
                value={formData.password2}
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
