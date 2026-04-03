import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useNavigate } from "react-router-dom";
import MetaTags from "@/components/Common/MetaTags";
import { User, FileText, Camera, ArrowRight, Check } from "lucide-react";

const Onboarding = () => {
  const { user, update } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  
  const [formData, setFormData] = useState({
    name: user?.name || "",
    bio: user?.bio || "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const nameParts = formData.name.trim().split(/\s+/);
      const firstName = nameParts[0] || "";
      const lastName = nameParts.slice(1).join(" ") || "";
      
      const data = new FormData();
      // Always send bio, even if empty
      data.append("bio", formData.bio || "");
      data.append("name", formData.name);
      data.append("firstName", firstName);
      data.append("lastName", lastName);
      
      const result = await update(data);
      if (result.success) {
        navigate("/creator-dashboard");
      } else {
        setError(result.error || "Failed to update profile");
      }
    } catch (err) {
      setError("An unexpected error occurred");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <MetaTags 
        title="Complete Your Profile | TipZed"
        description="Set up your creator profile to start receiving support from your fans."
      />
      
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
        {/* Progress Bar */}
        <div className="h-1.5 w-full bg-gray-100">
          <div 
            className="h-full bg-zed-green transition-all duration-500" 
            style={{ width: `${(step / 3) * 100}%` }}
          />
        </div>

        <div className="p-8">
          <div className="mb-8 text-center">
            <h1 className="text-2xl font-black text-gray-900 mb-2">
              {step === 1 && "What's your name?"}
              {step === 2 && "Tell us about yourself"}
              {step === 3 && "Almost there!"}
            </h1>
            <p className="text-gray-500 text-sm">
              {step === 1 && "This is how you'll be known on TipZed."}
              {step === 2 && "A short bio helps people know what you do."}
              {step === 3 && "Confirm your details to finish setup."}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 bg-red-50 border border-red-100 text-red-600 text-sm rounded-xl">
                {error}
              </div>
            )}

            {step === 1 && (
              <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="name"
                    placeholder="Your Name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-4 py-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-zed-green outline-none transition-all"
                  />
                </div>
                {formData.name && (
                  <div className="px-4 py-3 bg-zed-green/5 rounded-2xl border border-zed-green/10 animate-in fade-in zoom-in-95 duration-300">
                    <p className="text-[10px] uppercase tracking-wider font-bold text-gray-400 mb-1">Your profile link will be:</p>
                    <p className="text-sm font-black text-zed-green break-all">
                      tipzed.space/{formData.name.toLowerCase().replace(/[^a-z0-9]/g, "")}
                    </p>
                  </div>
                )}
                <button
                  type="button"
                  onClick={() => setStep(2)}
                  disabled={!formData.name}
                  className="w-full py-4 bg-zed-black text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-gray-800 transition-all disabled:opacity-50"
                >
                  Next Step <ArrowRight size={20} />
                </button>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="relative">
                  <FileText className="absolute left-4 top-4 text-gray-400" size={20} />
                  <textarea
                    name="bio"
                    placeholder="Write a short bio..."
                    value={formData.bio}
                    onChange={handleChange}
                    required
                    rows={4}
                    className="w-full pl-12 pr-4 py-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-zed-green outline-none transition-all resize-none"
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="flex-1 py-4 bg-gray-100 text-gray-600 rounded-2xl font-bold hover:bg-gray-200 transition-all"
                  >
                    Back
                  </button>
                  <button
                    type="button"
                    onClick={() => setStep(3)}
                    disabled={!formData.bio}
                    className="flex-[2] py-4 bg-zed-black text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-gray-800 transition-all disabled:opacity-50"
                  >
                    Next Step <ArrowRight size={20} />
                  </button>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="bg-gray-50 p-6 rounded-2xl border border-gray-100">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-16 h-16 bg-zed-green rounded-full flex items-center justify-center text-white text-2xl font-black">
                      {formData.name?.[0]?.toUpperCase() || "U"}
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900">{formData.name}</h3>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 italic">"{formData.bio}"</p>
                </div>

                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="flex-1 py-4 bg-gray-100 text-gray-600 rounded-2xl font-bold hover:bg-gray-200 transition-all"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-[2] py-4 bg-zed-green text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-green-700 transition-all disabled:opacity-50 shadow-lg shadow-zed-green/20"
                  >
                    {isLoading ? "Saving..." : (
                      <>Complete Setup <Check size={20} /></>
                    )}
                  </button>
                </div>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;

