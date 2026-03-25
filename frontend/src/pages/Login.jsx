import LoginForm from "@/components/Auth/LoginForm";
import MetaTags from "@/components/Common/MetaTags";
import GoogleLoginButton from "../components/Auth/GoogleLoginButton";

const Login = () => {
  return (
    <>
      <MetaTags
        title="Access Your Creator Account | TipZed"
        description="Log in to your TipZed account to manage your profile, track earnings, and connect with your supporters. Secure access for Zambian creators."
        keywords="login, sign in, creator account, access dashboard, TipZed login, creator login"
      />
      <div className="bg-gradient-to-br from-green-50 via-white to-orange-50 min-h-screen py-8 md:py-12 px-4 flex flex-col justify-center">
        <div className="w-full max-w-md mx-auto backdrop-blur-xl bg-white/80 shadow-2xl rounded-2xl p-6 md:p-8 border border-white/40">
          {/* Header Section */}
          <div className="text-center mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900">
              Welcome Back
            </h2>
            <p className="text-gray-500 text-sm mt-2">
              Access your TipZed account
            </p>
          </div>

          {/* Form Component */}
          <LoginForm />

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-gray-500 font-medium">
                OR
              </span>
            </div>
          </div>

          <GoogleLoginButton buttonText="Continue with Google" mode="login" />
        </div>
      </div>
    </>
  );
};

export default Login;
