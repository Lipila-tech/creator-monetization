import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const SignupForm = () => {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    password2: "",
    username: "",
    userType: "creator",
    firstName: "",
    lastName: "",
  });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // VALIDATE PASSWORDS
    if (formData.password !== formData.password2) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 8) {
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

    if (result.success) navigate("/login");
    else setError(result.error);

    setIsSubmitting(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 text-sm p-3 rounded-lg text-center mb-4">
          {error}
        </div>
      )}

      {/* <div>
        <label className="text-sm font-medium text-gray-600">First Name</label>
        <input
          name="firstName"
          required
          className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
          value={formData.firstName}
          onChange={handleChange}
        />
      </div> */}

      {/* <div>
        <label className="text-sm font-medium text-gray-600">Last Name</label>
        <input
          name="lastName"
          required
          className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
          value={formData.lastName}
          onChange={handleChange}
        />
      </div> */}

      <div>
        <label className="text-sm font-medium text-gray-600">Username</label>
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

      {/* <div>
        <label className="text-sm font-medium text-gray-600">I am a...</label>
        <select
          name="userType"
          className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
          value={formData.userType}
          onChange={handleChange}
        >
          <option value="creator">Creator</option>
          <option value="fan">Supporter / Fan</option>
        </select>
      </div> */}

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-sm font-medium text-gray-600">Password</label>
          <input
            name="password"
            type={showPassword ? "text" : "password"}
            required
            className="mt-1 w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-zed-orange focus:border-zed-orange outline-none"
            value={formData.password1}
            onChange={handleChange}
          />
        </div>
        <div>
          <label className="text-sm font-medium text-gray-600">Confirm</label>
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
        className="text-sm text-gray-600 hover:text-gray-900"
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
    </form>
  );
};

export default SignupForm;
