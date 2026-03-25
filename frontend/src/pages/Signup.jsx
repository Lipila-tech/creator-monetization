import SignupForm from "@/components/Auth/SignupForm";
import MetaTags from "@/components/Common/MetaTags";
import GoogleLoginButton from "../components/Auth/GoogleLoginButton";

const Signup = () => {
  return (
    <>
      <MetaTags
        title="Start Supporting Zambian Creators  | TipZed"
        description="Create your TipZed account today. Join a growing community of Zambian creators and supporters. Start tipping and accessing exclusive content."
        keywords="sign up, create account, join TipZed, register, new creator, become a supporter, Zambia creators platform"
      />
      <div className="bg-gradient-to-br from-orange-50 via-white to-green-50 py-8 md:py-12 px-4">
        <div className="w-full max-w-md mx-auto backdrop-blur-xl bg-white/80 shadow-2xl rounded-2xl p-6 md:p-8 border border-white/40">
          {/* Header Section */}
          <div className="text-center mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900">
              Create Your Account
            </h2>
            <p className="text-gray-500 text-sm mt-2">Join TipZed in seconds</p>
          </div>

          {/* Form Component */}
          <SignupForm />

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

          <GoogleLoginButton
            buttonText="Continue with Google"
            mode="register"
          />
        </div>
      </div>
    </>
  );
};

export default Signup;
