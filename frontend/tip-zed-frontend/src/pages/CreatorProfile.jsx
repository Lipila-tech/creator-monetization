import { useState, useEffect } from "react";
import {
  AlertCircle,
  CheckCircle2,
  Globe,
  Calendar,
  Users,
  Star,
  Share2,
} from "lucide-react";
import { useParams, useNavigate } from "react-router-dom";
import { creatorService } from "../services/creatorService";
import SupportModal from "../components/Payment/SupportModal";

const getName = (creator) =>
  `${creator?.user?.firstName || ""} ${creator?.user?.lastName || ""}`.trim() ||
  creator?.user?.username ||
  "Creator";

const CreatorProfile = () => {
  const [isSupportOpen, setIsSupportOpen] = useState(false);
  const { slug } = useParams();
  const navigate = useNavigate();

  const [creator, setCreator] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState({ show: false, message: "" });

  useEffect(() => {
    const fetchCreator = async () => {
      try {
        const response = await creatorService.getCreatorBySlug(slug);
        if (response.status === "success") {
          setCreator(response.data);
        }
      } catch (err) {
        console.error(err);
        setError("Creator not found.");
      } finally {
        setLoading(false);
      }
    };
    if (slug) fetchCreator();
  }, [slug]);

  if (loading)
    return (
      <div className="min-h-screen bg-white">
        {/* Cover Image Skeleton */}
        <div className="h-64 md:h-80 w-full bg-gray-100 relative overflow-hidden">
          <div className="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 animate-pulse"></div>
        </div>

        <main className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10 -mt-24 pb-20">
          {/* Top Profile Info Area Skeleton */}
          <div className="flex flex-col md:flex-row items-end gap-6 mb-8 px-2">
            {/* Profile Image Skeleton */}
            <div className="relative">
              <div className="w-40 h-40 md:w-48 md:h-48 rounded-[2.5rem] border-[6px] border-white bg-gray-100 animate-pulse shadow-xl"></div>
            </div>

            <div className="flex-1 pb-2 space-y-4">
              <div className="space-y-3">
                <div className="h-10 w-64 bg-gray-100 rounded-xl animate-pulse"></div>
                <div className="h-6 w-48 bg-gray-100 rounded-lg animate-pulse"></div>
              </div>

              {/* Stats Row Skeleton */}
              <div className="flex flex-wrap gap-6">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <div className="w-5 h-5 bg-gray-100 rounded-full animate-pulse"></div>
                    <div className="h-6 w-24 bg-gray-100 rounded-lg animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Share Button Skeleton */}
            <div className="w-12 h-12 rounded-full bg-gray-100 animate-pulse"></div>
          </div>

          {/* Content Grid Skeleton */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
            {/* Left Side: About & Feed Skeleton */}
            <div className="lg:col-span-8 space-y-12">
              <section>
                <div className="flex items-center gap-2 mb-6">
                  <div className="w-8 h-[2px] bg-gray-100 animate-pulse"></div>
                  <div className="h-6 w-32 bg-gray-100 rounded-lg animate-pulse"></div>
                </div>
                <div className="space-y-3">
                  <div className="h-4 w-full bg-gray-100 rounded animate-pulse"></div>
                  <div className="h-4 w-5/6 bg-gray-100 rounded animate-pulse"></div>
                  <div className="h-4 w-4/5 bg-gray-100 rounded animate-pulse"></div>
                  <div className="h-4 w-3/4 bg-gray-100 rounded animate-pulse"></div>
                </div>
              </section>

              <section>
                <div className="flex justify-between items-center mb-6">
                  <div className="h-6 w-48 bg-gray-100 rounded-lg animate-pulse"></div>
                </div>
                <div className="aspect-video w-full rounded-[2rem] bg-gray-50 border-2 border-gray-100 animate-pulse"></div>
              </section>
            </div>

            {/* Right Side: Support Card Skeleton */}
            <div className="lg:col-span-4">
              <div className="sticky top-28 space-y-6">
                <div className="bg-white rounded-[2.5rem] border-2 border-gray-100 p-8 shadow-xl relative overflow-hidden">
                  <div className="space-y-6">
                    <div className="h-8 w-3/4 mx-auto bg-gray-100 rounded-lg animate-pulse"></div>
                    <div className="space-y-2">
                      <div className="h-4 w-full bg-gray-100 rounded animate-pulse"></div>
                      <div className="h-4 w-5/6 mx-auto bg-gray-100 rounded animate-pulse"></div>
                    </div>
                    <div className="h-14 w-full bg-gray-100 rounded-2xl animate-pulse"></div>
                    <div className="h-5 w-40 mx-auto bg-gray-100 rounded animate-pulse"></div>
                  </div>
                </div>

                {/* Secondary info card skeleton */}
                <div className="px-8">
                  <div className="h-10 w-full bg-gray-100 rounded-lg animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    );

  if (error || !creator)
    return (
      <div className="h-screen bg-white flex flex-col items-center justify-center text-center px-4">
        <AlertCircle size={64} className="text-gray-200 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">
          Oops! Creator not found.
        </h2>
        <button
          onClick={() => navigate("/creator-catalog")}
          className="mt-6 px-6 py-2 bg-zed-green text-white rounded-full font-bold shadow-lg shadow-green-100 transition-all active:scale-95"
        >
          Explore Creators
        </button>
      </div>
    );

  const handleShare = async () => {
    const shareData = {
      title: `Support ${getName(creator)} on TipZed`,
      text: `Check out ${getName(creator)}'s profile on TipZed!`,
      url: window.location.href, // get the current profile URL
    };

    try {
      // Check if the browser supports native sharing (mostly mobile)
      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        // Fallback: Copy to clipboard for desktop users
        await navigator.clipboard.writeText(window.location.href);
        showToast("Link copied to clipboard!");
      }
    } catch (err) {
      if (err.name !== "AbortError") {
        showToast("Could not share profile.");
      }
    }
  };

  const showToast = (message) => {
    setToast({ show: true, message });
    setTimeout(() => setToast({ show: false, message: "" }), 3000); // Hide after 3 seconds
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Cover Image Section */}
      <div className="h-64 md:h-80 w-full bg-gray-100 relative overflow-hidden">
        {creator.coverImage ? (
          <img
            src={creator.coverImage}
            alt="Cover"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-zed-green/20 via-white to-zed-orange/20" />
        )}
      </div>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10 -mt-24 pb-20">
        {/* Top Profile Info Area */}
        <div className="flex flex-col md:flex-row items-end gap-6 mb-8 px-2">
          {/* Large Profile Image */}
          <div className="relative group">
            {creator.profileImage ? (
              <img
                src={creator.profileImage}
                alt={creator.user.username}
                className="w-40 h-40 md:w-48 md:h-48 rounded-[2.5rem] object-cover border-[6px] border-white shadow-xl bg-white"
              />
            ) : (
              <div className="w-40 h-40 md:w-48 md:h-48 rounded-[2.5rem] border-[6px] border-white bg-zed-green flex items-center justify-center text-white text-6xl font-black shadow-xl">
                {getName(creator).charAt(0)}
              </div>
            )}
            {creator.status === "active" && (
              <div
                className="absolute bottom-4 right-4 w-6 h-6 bg-green-500 border-4 border-white rounded-full shadow-sm"
                title="Active"
              />
            )}
          </div>

          <div className="flex-1 pb-2">
            <div className="flex flex-wrap items-center gap-3 mb-1">
              <h1 className="text-4xl font-black text-gray-900 tracking-tight">
                {getName(creator)}
              </h1>
              {creator.verified && (
                <CheckCircle2
                  size={24}
                  className="text-blue-500 fill-blue-50"
                />
              )}
            </div>
            <p className="text-lg text-gray-500 font-medium mb-4">
              @{creator.user.username}
            </p>

            {/* Cleaner Stats Row */}
            <div className="flex flex-wrap gap-6 text-sm">
              <div className="flex items-center gap-1.5 text-gray-700">
                <Users size={18} className="text-zed-green" />
                <span className="font-bold">{creator.followersCount || 0}</span>
                <span className="text-gray-400">Supporters</span>
              </div>
              <div className="flex items-center gap-1.5 text-gray-700">
                <Star size={18} className="text-zed-orange" />
                <span className="font-bold">{creator.rating || "5.0"}</span>
                <span className="text-gray-400">Rating</span>
              </div>
              <div className="flex items-center gap-1.5 text-gray-700">
                <Calendar size={18} className="text-gray-400" />
                <span className="text-gray-400">
                  Joined {new Date(creator.user.dateJoined).getFullYear()}
                </span>
              </div>
            </div>
          </div>

          {/* Share Button */}
          <button
            onClick={handleShare}
            className="p-3 rounded-full bg-gray-50 text-gray-400 hover:bg-zed-green/10 hover:text-zed-green transition-all active:scale-90 group relative"
            title="Share Profile"
          >
            <Share2 size={20} />

            {/* Tooltip that appears on hover for desktop */}
            <span className="absolute -top-10 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
              Share Profile
            </span>
          </button>
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Left Side: About & Feed */}
          <div className="lg:col-span-8 space-y-12">
            <section>
              <h2 className="text-xl font-black text-gray-900 mb-4 flex items-center gap-2 uppercase tracking-widest text-xs">
                <span className="w-8 h-[2px] bg-zed-green" />
                About Creator
              </h2>
              <p className="text-gray-600 text-lg leading-relaxed whitespace-pre-wrap max-w-3xl">
                {creator.bio || `${getName(creator)} hasn't added a bio yet.`}
              </p>
            </section>

            <section>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-black text-gray-900 uppercase tracking-widest text-xs">
                  Latest Activity
                </h2>
              </div>
              <div className="aspect-video w-full rounded-[2rem] bg-gray-50 border-2 border-dashed border-gray-100 flex flex-col items-center justify-center text-gray-400">
                <p className="font-bold">Exclusive feed coming soon</p>
                <p className="text-xs">Follow to stay updated</p>
              </div>
            </section>
          </div>

          {/* Right Side: Support Card */}
          <div className="lg:col-span-4">
            <div className="sticky top-28 space-y-6">
              <div className="bg-white rounded-[2.5rem] border-2 border-zed-green p-8 shadow-2xl shadow-green-100/50 text-center relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-zed-green/5 rounded-full -mr-12 -mt-12" />

                <h3 className="text-2xl font-black text-gray-900 mb-2">
                  Support {getName(creator).split(" ")[0]}
                </h3>
                <p className="text-gray-500 text-sm mb-8">
                  Direct support helps me keep creating the content you love.
                </p>

                <button
                  onClick={() => setIsSupportOpen(true)}
                  className="w-full bg-zed-green text-white py-4 rounded-2xl font-black text-lg shadow-lg shadow-green-200 hover:bg-green-600 hover:-translate-y-1 transition-all active:scale-95"
                >
                  Send a Tip
                </button>

                {creator.website && (
                  <a
                    href={creator.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-gray-400 hover:text-zed-green transition-colors"
                  >
                    <Globe size={14} />
                    Official Website
                  </a>
                )}
              </div>

              {/* Secondary info card */}
              <div className="px-8 text-center">
                <p className="text-xs text-gray-400 font-medium">
                  100% of your support goes directly to the creator (minus
                  processing fees).
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <div
        className={`fixed bottom-8 left-1/2 -translate-x-1/2 z-[100] transition-all duration-500 ${
          toast.show
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-4 pointer-events-none"
        }`}
      >
        <div className="bg-gray-900 text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-3 border border-white/10 backdrop-blur-md">
          <div className="bg-zed-green rounded-full p-1">
            <CheckCircle2 size={14} className="text-white" />
          </div>
          <span className="text-sm font-bold tracking-tight">
            {toast.message}
          </span>
        </div>
      </div>

      <SupportModal
        isOpen={isSupportOpen}
        onClose={() => setIsSupportOpen(false)}
        creator={creator}
      />
    </div>
  );
};

export default CreatorProfile;
