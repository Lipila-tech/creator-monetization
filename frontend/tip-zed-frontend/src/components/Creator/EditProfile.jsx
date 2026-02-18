import { useState } from "react";
import {
  Camera,
  Save,
  Loader2,
  User,
  Image as ImageIcon,
  AlertCircle,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

const EditProfile = () => {
  const navigate = useNavigate();
  const { user, update } = useAuth();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    fullName: `${user?.firstName || ""} ${user?.lastName || ""}`.trim(),
    bio: user?.bio || "",
  });

  const [pendingFiles, setPendingFiles] = useState({
    profile: null,
    cover: null,
  });

  // Preview State - to show new images before upload
  // Preview State - to show new images before upload
  const [previews, setPreviews] = useState({
    profile: user?.profileImage || null,
    cover: user?.coverImage || null,
  });

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
      // VALIDATION
      if (!formData.fullName?.trim()) {
        throw new Error("Display name is required");
      }

      // Split full name
      const nameParts = formData.fullName.trim().split(/\s+/);

      // Create FormData object -what DRF MultiPartParser expects
      const formDataToSend = new FormData();

      // Add text fields
      formDataToSend.append("first_name", nameParts[0]);
      formDataToSend.append("last_name", nameParts.slice(1).join(" ") || "");

      if (formData.bio?.trim()) {
        formDataToSend.append("bio", formData.bio.trim());
      }

      // IMPORTANT: Append files directly - NO Base64 conversion!
      if (pendingFiles.profile) {
        formDataToSend.append("profile_image", pendingFiles.profile);
      }

      if (pendingFiles.cover) {
        formDataToSend.append("cover_image", pendingFiles.cover);
      }

      // Send FormData - DO NOT set Content-Type header, let browser set it with boundary
      const result = await update(formDataToSend);

      if (result.success) {
        setSuccess(true);
        // Clear pending files
        setPendingFiles({ profile: null, cover: null });

        // Update user data with new image URLs from response
        if (result.data?.profileImage) {
          setPreviews((prev) => ({
            ...prev,
            profile: result.data.profileImage,
          }));
        }
        if (result.data?.coverImage) {
          setPreviews((prev) => ({ ...prev, cover: result.data.coverImage }));
        }

        // Redirect after successful update
        setTimeout(() => navigate("/creator-dashboard"), 1500);
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
    fullName: !formData.fullName?.trim(),
    bio: !formData.bio?.trim(),
    profileImage: !previews.profile && !user?.profileImage,
    coverImage: !previews.cover && !user?.coverImage,
  };

  const hasMissingFields = Object.values(isEmpty).some(Boolean);

  return (
    <>
      <div className="min-h-screen bg-gray-50 pb-20">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto mt-6 px-4">
          {/* Success Message */}
          {success && (
            <div className="mb-6 bg-green-50 text-green-700 px-4 py-3 rounded-xl border border-green-200 flex items-center gap-2 animate-in slide-in-from-top-2">
              <User size={18} /> Profile updated successfully! Redirecting...
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
                        {formData.fullName?.charAt(0) || "U"}
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
                    Display Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    disabled={loading || success}
                    className={`w-full px-4 py-3 rounded-xl font-medium transition-all text-black
                  ${
                    isEmpty.fullName && !success
                      ? "bg-amber-50 border-amber-400 ring-2 ring-amber-400"
                      : "bg-gray-50 border-gray-200 focus:ring-zed-green"
                  }
                  ${loading || success ? "opacity-50 cursor-not-allowed" : ""}
                `}
                    placeholder="e.g. Chanda Mwamba"
                  />
                  {isEmpty.fullName && !success && (
                    <p className="text-xs text-amber-600 mt-1 flex items-center gap-1">
                      <AlertCircle size={12} /> Display name is required
                    </p>
                  )}
                </div>

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