import { Link } from "react-router-dom";
import LoginForm from "@/components/Auth/LoginForm";
import MetaTags from "@/components/Common/MetaTags";

const Login = () => {
  return (
    <>
      <MetaTags
        title="Access Your Creator Account | TipZed"
        description="Log in to your TipZed account to manage your profile, track earnings, and connect with your supporters. Secure access for Zambian creators."
        keywords="login, sign in, creator account, access dashboard, TipZed login, creator login"
      />
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-white to-orange-50 px-4">
        <div className="w-full max-w-md backdrop-blur-xl bg-white/80 shadow-2xl rounded-2xl p-8 border border-white/40">
          {/* Header Section */}
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">
              Welcome Back 👋
            </h2>
            <p className="text-gray-500 text-sm mt-1">
              Login to your{" "}
              <span className="text-zed-green font-semibold">TipZed</span>{" "}
              account
            </p>
          </div>

          {/* Form Component */}
          <LoginForm />

          {/* Footer Link */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              Don't have an account?{" "}
              <Link
                to="/register"
                className="font-semibold text-zed-green hover:text-green-700"
              >
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
