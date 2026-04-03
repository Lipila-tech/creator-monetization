import { useState, useEffect } from "react";
import {
  Camera,
  Save,
  Loader2,
  User,
  Image as ImageIcon,
  AlertCircle,
  Globe,
  Facebook,
  Instagram,
  Twitter,
  Music,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { validateMobileNumber } from "@/utils/mobileMoney";

const EditProfile = () => {
  const navigate = useNavigate();
  const { user, update, refreshUser } = useAuth();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    bio: user?.bio || "",
    phoneNumber: user?.phoneNumber || "",
    tiktok: user?.tiktok || "",
    facebook: user?.facebook || "",
    website: user?.website || "",
    instagram: user?.instagram || "",
    twitter: user?.twitter || "",
  });

  const [pendingFiles, setPendingFiles] = useState({
    profile: null,
    cover: null,
  });

  // Preview State - to show new images before upload
  const [previews, setPreviews] = useState({
    profile: user?.profileImage || null,
    cover: user?.coverImage || null,
  });

  // Initialize form data once user is loaded
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    if (user && !isInitialized) {
      setFormData({
        bio: user.bio || "",
        phoneNumber: user.phoneNumber || "",
        tiktok: user.tiktok || "",
        facebook: user.facebook || "",
        website: user.website || "",
        instagram: user.instagram || "",
        twitter: user.twitter || "",
      });
      setPreviews({
        profile: user.profileImage || null,
        cover: user.coverImage || null,
      });
      setIsInitialized(true);
    }
  }, [user, isInitialized]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (error) setError("");
  };

  const handleImageChange = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      // Clean up old preview URL to prevent memory leaks
      if (previews[type]?.startsWith("blob:")) {
        URL.revokeObjectURL(previews[type]);
      }

      // Store the file for FormData
      // Store the file for FormData
      setPendingFiles((prev) => ({ ...prev, [type]: file }));

      // Generate Local Preview URL
      const previewUrl = URL.createObjectURL(file);
      setPreviews((prev) => ({ ...prev, [type]: previewUrl }));

      if (error) setError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      // Create FormData object -what DRF MultiPartParser expects
      const formDataToSend = new FormData();

      // Always send bio, even if empty, to allow clearing it
      formDataToSend.append("bio", formData.bio || "");

      if (formData.phoneNumber?.trim()) {
        const phoneValidation = validateMobileNumber(formData.phoneNumber);
        
        if (!phoneValidation.isValid)
          throw new Error("Please enter a valid phone number");

        formDataToSend.append("phoneNumber", phoneValidation.formatted);
      }

      // Social Links
      formDataToSend.append("tiktok", formData.tiktok || "");
      formDataToSend.append("facebook", formData.facebook || "");
      formDataToSend.append("website", formData.website || "");
      formDataToSend.append("instagram", formData.instagram || "");
      formDataToSend.append("twitter", formData.twitter || "");

      // IMPORTANT: Append files directly - NO Base64 conversion!
      if (pendingFiles.profile) {
        formDataToSend.append("profileImage", pendingFiles.profile);
      }

      if (pendingFiles.cover) {
        formDataToSend.append("coverImage", pendingFiles.cover);
      }

      // Send FormData - DO NOT set Content-Type header, let browser set it with boundary
      const result = await update(formDataToSend);

      if (result.success) {
        setSuccess(true);
        // Clear pending files
        setPendingFiles({ profile: null, cover: null });

        // Update user data with new image URLs from response
        const normalized = result.data?.creator || result.data?.user || result.data?.data || result.data;
        
        if (normalized?.profileImage || normalized?.profile_image) {
          setPreviews((prev) => ({
            ...prev,
            profile: normalized.profileImage || normalized.profile_image,
          }));
        }
        if (normalized?.coverImage || normalized?.cover_image) {
          setPreviews((prev) => ({ 
            ...prev, 
            cover: normalized.coverImage || normalized.cover_image 
          }));
        }

        // Background refetch to ensure everything is in sync
        refreshUser();
        
        // Hide success message after 3 seconds
        setTimeout(() => {
          setSuccess(false);
        }, 3000);
      } else {
        setError(result.error || "Failed to update profile");
      }
    } catch (error) {
      setError(error.message || "An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  const isEmpty = {
    bio: !formData.bio?.trim(),
    profileImage: !previews.profile && !user?.profileImage,
    coverImage: !previews.cover && !user?.coverImage,
  };

  const hasMissingFields = Object.values(isEmpty).some(Boolean);

  return (
    <>
      <div className="min-h-screen bg-gray-50 pb-20">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto mt-6 px-4">
          {/* Read-only Info Section */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
                  Email
                </label>
                <p className="text-gray-900 font-medium truncate" title={user?.email}>
                  {user?.email}
                </p>
              </div>
              <div>
                <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
                  Username
                </label>
                <p className="text-gray-900 font-medium truncate" title={user?.name}>
                  {user?.name}
                </p>
              </div>
              <div>
                <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
                  Slug
                </label>
                <p className="text-gray-900 font-medium truncate" title={user?.slug}>
                  @{user?.slug}
                </p>
              </div>
            </div>
          </div>

          {/* Success Message */}
          {success && (
            <div className="mb-6 bg-green-50 text-green-700 px-4 py-3 rounded-xl border border-green-200 flex items-center gap-2 animate-in slide-in-from-top-2">
              <User size={18} /> Profile updated successfully!
            </div>
          )}
          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-50 text-red-700 px-4 py-3 rounded-xl border border-red-200 flex items-center gap-2">
              <AlertCircle size={18} /> {error}
            </div>
          )}
          {/* IMAGES SECTION */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden mb-6">
            {/* Cover Image Input */}
            <div
              className={`h-48 w-full bg-gray-100 relative group
              ${isEmpty.coverImage && !success ? "ring-2 ring-amber-400" : ""}
            `}
            >
              {isEmpty.coverImage && !success && (
                <span className="absolute top-3 right-3 w-3 h-3 bg-amber-400 rounded-full animate-pulse" />
              )}
              {previews.cover ? (
                <img
                  src={previews.cover}
                  alt="Cover"
                  className="w-full h-full object-cover opacity-90 group-hover:opacity-75 transition-opacity"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400 bg-gray-100">
                  <ImageIcon size={48} opacity={0.2} />
                </div>
              )}

              {/* Edit Button Overlay */}
              <label className="absolute inset-0 flex items-center justify-center cursor-pointer bg-black/0 group-hover:bg-black/20 transition-all">
                <div className="bg-white/90 backdrop-blur-sm text-gray-700 px-4 py-2 rounded-full font-medium shadow-lg flex items-center gap-2 hover:bg-white hover:text-zed-green transition-colors">
                  <Camera size={18} />
                  <span>{previews.cover ? "Change Cover" : "Add Cover"}</span>
                </div>
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => handleImageChange(e, "cover")}
                  disabled={loading || success}
                />
              </label>
            </div>

            <div className="px-8 pb-8">
              {/* Profile Image Input (Overlapping) */}
              <div className="relative -mt-16 mb-6 inline-block">
                <div className="relative group">
                  {previews.profile ? (
                    <img
                      src={previews.profile}
                      alt="Profile"
                      className="w-32 h-32 rounded-2xl border-4 border-white shadow-md object-cover bg-white"
                    />
                  ) : (
                    <div
                      className={`relative group rounded-2xl
                    ${isEmpty.profileImage && !success ? "ring-2 ring-amber-400" : ""}
                  `}
                    >
                      <div className="w-32 h-32 rounded-2xl border-4 border-white shadow-md bg-zed-green flex items-center justify-center text-white text-4xl font-bold">
                        {user?.name?.charAt(0) || "U"}
                      </div>
                      {isEmpty.profileImage && !success && (
                        <span className="absolute -top-1 -right-1 w-3 h-3 bg-amber-400 rounded-full" />
                      )}
                    </div>
                  )}

                  {/* Edit Button for Avatar */}
                  <label className="absolute bottom-[-10px] right-[-10px] bg-white p-2.5 rounded-full shadow-md border border-gray-100 cursor-pointer hover:bg-gray-50 text-gray-600 hover:text-zed-green transition-colors">
                    <Camera size={20} />
                    <input
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={(e) => handleImageChange(e, "profile")}
                      disabled={loading || success}
                    />
                  </label>
                </div>
                {pendingFiles.profile && (
                  <span className="absolute -bottom-6 left-0 text-xs text-blue-600 font-medium">
                    New photo ready
                  </span>
                )}
              </div>

              {/* TEXT FIELDS */}
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Bio / About
                  </label>
                  <textarea
                    name="bio"
                    rows={4}
                    value={formData.bio}
                    onChange={handleChange}
                    disabled={loading || success}
                    className={`w-full px-4 py-3 rounded-xl resize-none transition-all text-black
                  ${
                    isEmpty.bio && !success
                      ? "bg-amber-50 border-amber-400 ring-2 ring-amber-400"
                      : "bg-gray-50 border-gray-200 focus:ring-zed-green"
                  }
                  ${loading || success ? "opacity-50 cursor-not-allowed" : ""}
                `}
                    placeholder="Tell your supporters about what you create..."
                    maxLength={500}
                  />
                  <p className="text-right text-xs text-gray-400 mt-2">
                    {formData.bio.length}/500
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    name="phoneNumber"
                    value={formData.phoneNumber}
                    onChange={handleChange}
                    className="w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-zed-green text-black"
                    placeholder="0 97 123 4567"
                  />
                </div>

                {/* SOCIAL LINKS */}
                <div className="pt-4 border-t border-gray-100">
                  <h3 className="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2">
                    Social Links
                  </h3>
                  
                  <div className="space-y-4">
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                        <Music size={18} />
                      </div>
                      <input
                        type="url"
                        name="tiktok"
                        value={formData.tiktok}
                        onChange={handleChange}
                        className="w-full pl-11 pr-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-zed-green text-black"
                        placeholder="TikTok URL"
                      />
                    </div>

                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                        <Facebook size={18} />
                      </div>
                      <input
                        type="url"
                        name="facebook"
                        value={formData.facebook}
                        onChange={handleChange}
                        className="w-full pl-11 pr-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-zed-green text-black"
                        placeholder="Facebook URL"
                      />
                    </div>

                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                        <Instagram size={18} />
                      </div>
                      <input
                        type="url"
                        name="instagram"
                        value={formData.instagram}
                        onChange={handleChange}
                        className="w-full pl-11 pr-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-zed-green text-black"
                        placeholder="Instagram URL"
                      />
                    </div>

                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                        <Twitter size={18} />
                      </div>
                      <input
                        type="url"
                        name="twitter"
                        value={formData.twitter}
                        onChange={handleChange}
                        className="w-full pl-11 pr-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-zed-green text-black"
                        placeholder="Twitter URL"
                      />
                    </div>

                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                        <Globe size={18} />
                      </div>
                      <input
                        type="url"
                        name="website"
                        value={formData.website}
                        onChange={handleChange}
                        className="w-full pl-11 pr-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-zed-green text-black"
                        placeholder="Website URL"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* ACTIONS */}
          <div className="flex items-center justify-end gap-4 mb-10">
            <button
              type="button"
              onClick={() => navigate("/creator-dashboard")}
              disabled={loading}
              className="px-6 py-3 rounded-xl font-bold text-gray-500 hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading || success}
              className={`px-8 py-3 rounded-xl font-bold flex items-center gap-2 transition-all
              ${
                hasMissingFields && !success
                  ? "bg-amber-500 hover:bg-amber-600"
                  : "bg-zed-black hover:bg-gray-800"
              }
              ${loading || success ? "opacity-50 cursor-not-allowed" : ""}
              text-white
            `}
            >
              {loading ? (
                <>
                  <Loader2 size={20} className="animate-spin" /> Saving...
                </>
              ) : success ? (
                <>
                  <User size={20} /> Saved!
                </>
              ) : (
                <>
                  <Save size={20} /> Save Changes
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default EditProfile;

