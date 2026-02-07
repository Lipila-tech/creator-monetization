import { useState, useEffect } from "react";
import { AlertCircle, Loader } from "lucide-react";
import { useParams, useNavigate } from "react-router-dom";
import { creatorService } from "../services/creatorService";
import SupportModal from "../components/Payment/SupportModal";

const getName = (creator) =>
  `${creator.user?.firstName || ""} ${creator.user?.lastName || ""}`.trim() ||
  creator.user?.username ||
  "Creator";

const formatDate = (date) =>
  new Date(date).toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
  });

const CreatorProfile = () => {
  const [isSupportOpen, setIsSupportOpen] = useState(false);
  const { slug } = useParams();
  const navigate = useNavigate();

  const [creator, setCreator] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCreator = async () => {
      try {
        const response = await creatorService.getCreatorBySlug(slug);
        if (response.status === "success") {
          setCreator(response.data);
        }
      } catch (err) {
        console.error(err);
        setError("Creator not found or unavailable.");
      } finally {
        setLoading(false);
      }
    };

    if (slug) fetchCreator();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <Loader className="animate-spin text-zed-green" size={32} />
      </div>
    );
  }

  if (error || !creator) {
    return (
      <div className="h-screen bg-white flex flex-col items-center justify-center text-center px-4">
        <AlertCircle size={48} className="text-gray-400 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">Creator Not Found</h2>
        <button
          onClick={() => navigate("/creator-catalog")}
          className="mt-4 text-zed-green font-semibold"
        >
          Back to Creators
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Cover Image (Top of page) */}
      <div className="h-48 w-full bg-gray-200 relative overflow-hidden">
        {creator.coverImage ? (
          <img
            src={creator.coverImage}
            alt="Cover"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-r from-zed-green via-yellow-500 to-zed-orange flex items-center justify-center opacity-90">
            <span className="text-9xl font-black text-white opacity-10 select-none transform rotate-12 scale-150">
              {creator.user.username || "?"}
            </span>
          </div>
        )}
      </div>

      <main className="max-w-5xl mx-auto px-6 py-8 relative z-10 -mt-20">
        {/* Creator Info Card (Profile Pic, Name, Stats) */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 mb-6">
          <div className="flex flex-col md:flex-row gap-6 items-start">
            {/* Profile Image */}
            <div className="flex-shrink-0">
              {creator.profileImage ? (
                <img
                  src={creator.profileImage}
                  alt={creator.user.username}
                  className="w-32 h-32 rounded-2xl object-cover shadow-md border-4 border-white bg-white"
                />
              ) : (
                <div className="w-32 h-32 rounded-2xl shadow-md border-4 border-white bg-zed-green flex items-center justify-center">
                  <span className="text-4xl font-bold text-white">
                    {getName(creator).charAt(0).toUpperCase()}
                  </span>
                </div>
              )}
            </div>

            {/* Name & Details */}
            <div className="flex-1 w-full">
              <div className="flex justify-between items-start">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">
                    {getName(creator)}
                  </h1>
                  <p className="text-gray-500 font-medium mb-3">
                    @{creator.user.username}
                  </p>

                  {/* Badges */}
                  <div className="flex flex-wrap items-center gap-2 mb-4">
                    {creator.verified && (
                      <span className="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded-full">
                        ✔ Verified
                      </span>
                    )}
                    <span className="bg-gray-100 text-gray-700 text-xs font-semibold px-2.5 py-1 rounded-full capitalize">
                      {creator.user.userType}
                    </span>
                  </div>
                </div>
              </div>

              {/* Stats Grid (Moved inside the card) */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 border-t border-gray-100 pt-4">
                <div className="text-center sm:text-left">
                  <p className="text-lg font-bold text-gray-900">
                    {creator.followersCount || 0}
                  </p>
                  <p className="text-xs text-gray-500">Followers</p>
                </div>
                <div className="text-center sm:text-left">
                  <p className="text-lg font-bold text-gray-900">
                    {creator.rating || "N/A"}
                  </p>
                  <p className="text-xs text-gray-500">Rating</p>
                </div>
                <div className="text-center sm:text-left">
                  <p className="text-lg font-bold text-gray-900">
                    {formatDate(creator.user.dateJoined)}
                  </p>
                  <p className="text-xs text-gray-500">Joined</p>
                </div>
                <div className="text-center sm:text-left">
                  {/* Status Badge Logic */}
                  <span
                    className={`inline-block px-2 py-1 rounded text-xs font-bold capitalize ${
                      creator.status === "active"
                        ? "bg-green-100 text-green-700"
                        : "bg-red-100 text-red-600"
                    }`}
                  >
                    {creator.status}
                  </span>
                  <p className="text-xs text-gray-500 mt-1">Status</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: About & Posts */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">About</h2>
              <p className="text-gray-600 leading-relaxed whitespace-pre-wrap">
                {creator.bio || "No bio available."}
              </p>
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                Recent Posts
              </h2>
              <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                <p>Content API integration pending...</p>
                <p className="text-sm">
                  Posts will appear here (Public vs Locked)
                </p>
              </div>
            </div>
          </div>

          {/* Right Column: Sticky Support & Links */}
          <div className="lg:col-span-1">
            <div className="sticky top-6 space-y-6">
              <div className="bg-gradient-to-r from-zed-green via-yellow-500 to-zed-orange rounded-2xl shadow-lg p-8 text-center">
                <h2 className="text-2xl font-bold text-white mb-3">
                  Support {getName(creator)?.split(" ")[0]}
                </h2>
                <p className="text-white/95 text-sm mb-6">
                  Become a supporter to unlock exclusive content.
                </p>
                <button
                  onClick={() => setIsSupportOpen(true)}
                  className="w-full bg-white text-zed-green px-8 py-3 rounded-lg hover:bg-gray-50 transition-all font-bold shadow-md"
                >
                  Send a Tip
                </button>
              </div>

              {creator.website && (
                <div className="text-center">
                  <a
                    href={creator.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-zed-green font-semibold hover:underline"
                  >
                    Visit Website →
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
      <SupportModal
        isOpen={isSupportOpen}
        onClose={() => setIsSupportOpen(false)}
        creator={creator}
      />
    </div>
  );
};

export default CreatorProfile;
