import { Link } from "react-router-dom";
import SignupForm from "../components/Auth/SignupForm";

export default function Signup() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-50 via-white to-green-50 p-4">
      <div className="w-full max-w-md backdrop-blur-xl bg-white/80 shadow-2xl rounded-2xl p-8 border border-white/40">
        
        {/* Header Section */}
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold text-gray-900">
            Join <span className="text-zed-orange">Tip Zed</span> 🚀
          </h2>
          <p className="text-gray-500 text-sm">
            Create your account in seconds
          </p>
        </div>

        {/* Form Component */}
        <SignupForm />

        {/* Footer Link */}
        <p className="text-center text-sm text-gray-600 mt-4">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-zed-green font-medium hover:underline"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}