import { useState, useEffect, useMemo } from "react";
import {
  Search,
  Music,
  Video,
  Palette,
  Mic,
  UserX,
  ArrowRight,
} from "lucide-react";
import { Link } from "react-router-dom";
import { creatorService } from "@/services/creatorService";

const getCreatorName = (creator) => {
  const name =
    `${creator?.user?.firstName || ""} ${creator?.user?.lastName || ""}`.trim();
  return name || creator?.user?.username || "Anonymous Creator";
};

const CreatorCatalog = () => {
  const [creators, setCreators] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  useEffect(() => {
    const fetchCreators = async () => {
      try {
        const response = await creatorService.getAllCreators();
        if (response.status === "success") {
          setCreators(response.data);
        } else {
          throw new Error("Failed to fetch");
        }
      } catch (err) {
        console.error(err);
        setError("Unable to reach the gallery. Please try again later.");
      } finally {
        setLoading(false);
      }
    };
    fetchCreators();
  }, []);

  const filteredCreators = useMemo(() => {
    return creators.filter((c) => {
      // match the search term
      const matchSearch = getCreatorName(c)
        .toLowerCase()
        .includes(searchTerm.toLowerCase());

      // match the categories of the creator
      const matchCategory =
        selectedCategory === "All" ||
        c.categories.find((cat) =>
          cat.toLowerCase().includes(selectedCategory.toLowerCase()),
        );

      [].fin;
      return matchSearch && matchCategory;
    });
  }, [creators, searchTerm, selectedCategory]);

  // Skeleton loader component
  const SkeletonLoader = () => (
    <div className="min-h-screen bg-white">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-10">
        {/* Header Area Skeleton */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-6">
          <div className="space-y-4">
            <div className="h-12 w-64 bg-gray-100 rounded-2xl animate-pulse"></div>
            <div className="h-5 w-96 bg-gray-100 rounded-xl animate-pulse"></div>
          </div>

          {/* Search Bar Skeleton */}
          <div className="relative w-full md:w-96">
            <div className="h-14 bg-gray-100 rounded-2xl animate-pulse"></div>
          </div>
        </div>

        {/* Category Filter Skeleton */}
        <div className="flex overflow-x-auto pb-4 gap-3 no-scrollbar mb-12">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className="h-11 w-32 bg-gray-100 rounded-full animate-pulse"
            ></div>
          ))}
        </div>

        {/* Catalog Grid Skeleton */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-12">
          {[...Array(8)].map((_, index) => (
            <div key={index} className="flex flex-col h-full">
              {/* Image Container Skeleton */}
              <div className="aspect-[4/5] overflow-hidden rounded-[2rem] bg-gray-100 relative animate-pulse">
                <div className="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200"></div>

                {/* Floating Badge Skeleton */}
                <div className="absolute top-4 left-4">
                  <div className="h-7 w-20 bg-gray-200 rounded-full"></div>
                </div>
              </div>

              {/* Content Section Skeleton */}
              <div className="pt-6 px-2 space-y-3">
                <div className="h-6 w-3/4 bg-gray-100 rounded-lg animate-pulse"></div>
                <div className="space-y-2">
                  <div className="h-4 w-full bg-gray-100 rounded animate-pulse"></div>
                  <div className="h-4 w-5/6 bg-gray-100 rounded animate-pulse"></div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="h-6 w-28 bg-gray-100 rounded animate-pulse"></div>
                  <div className="h-5 w-5 bg-gray-100 rounded animate-pulse"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );

  if (loading) {
    return <SkeletonLoader />;
  }

  return (
    <div className="min-h-screen bg-white">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-10">
        {/* Header Area */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-6">
          <div className="space-y-2">
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
              Gallery
            </h1>
            <p className="text-gray-500 font-medium italic">
              Support creators directly.
            </p>
          </div>

          {/* REFINED SEARCH BAR */}
          <div className="relative w-full md:w-96 group">
            <Search
              className="absolute left-4 top-1/2 -translate-y-1/2 text-zed-green transition-colors"
              size={20}
            />
            <input
              type="text"
              placeholder="Search creators..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full text-black pl-12 pr-4 py-3.5 bg-zed-green/[0.02] border border-gray-100 rounded-2xl focus:ring-4 focus:ring-zed-green/10 focus:border-zed-green focus:bg-white outline-none transition-all shadow-sm placeholder-gray-400"
            />
          </div>
        </div>

        <div className="flex overflow-x-auto pb-4 gap-3 no-scrollbar mb-12">
          {["All", "Music", "Video", "Art", "Podcast"].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-full transition-all font-bold text-sm whitespace-nowrap shadow-sm border ${
                selectedCategory === cat
                  ? "bg-zed-green text-white border-zed-green"
                  : "bg-white text-gray-600 border-gray-100 hover:border-zed-green/30"
              }`}
            >
              {cat === "Music" && <Music size={16} />}
              {cat === "Video" && <Video size={16} />}
              {cat === "Art" && <Palette size={16} />}
              {cat === "Podcast" && <Mic size={16} />}
              {cat}
            </button>
          ))}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-100 text-red-600 p-4 rounded-xl mb-6">
            {error}
          </div>
        )}

        {/* Catalog Grid */}
        {filteredCreators.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-12">
            {filteredCreators.map((creator) => {
              const name = getCreatorName(creator);
              return (
                <Link
                  to={`/creator-profile/${creator.user?.slug}`}
                  key={creator.user?.id || creator._id}
                  className="group"
                >
                  <div className="flex flex-col h-full">
                    {/* Image Container with high-end shadow */}
                    <div className="aspect-[4/5] overflow-hidden rounded-[2rem] bg-gray-100 relative shadow-[0_15px_35px_-10px_rgba(0,0,0,0.1)] transition-transform duration-500 group-hover:-translate-y-2">
                      {creator.profileImage ? (
                        <img
                          src={creator.profileImage}
                          alt={name}
                          loading="lazy"
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                        />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-gray-50 to-gray-200 flex items-center justify-center">
                          <span className="text-4xl font-black text-gray-300 uppercase">
                            {name.charAt(0)}
                          </span>
                        </div>
                      )}

                      {/* Floating Badge */}
                      <div className="absolute top-4 left-4">
                        <span className="bg-white/80 backdrop-blur-md text-gray-900 text-[10px] font-black px-3 py-1.5 rounded-full uppercase tracking-tighter shadow-sm">
                          {creator.user?.userType || "Creator"}
                        </span>
                      </div>
                    </div>

                    {/* Content Section */}
                    <div className="pt-6 px-2">
                      <h3 className="font-bold text-xl text-gray-900 mb-1 group-hover:text-zed-green transition-colors">
                        {name}
                      </h3>
                      <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                        {creator.bio || "No bio available."}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-[11px] font-black uppercase tracking-widest text-zed-green bg-zed-green/10 px-2 py-1 rounded">
                          {creator.followersCount || 0} Supporters
                        </span>
                        <ArrowRight
                          size={18}
                          className="text-gray-300 group-hover:text-zed-green group-hover:translate-x-1 transition-all"
                        />
                      </div>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-24 border-2 border-dashed border-gray-100 rounded-[3rem]">
            <UserX
              className="mx-auto text-gray-200 mb-4"
              size={64}
              strokeWidth={1}
            />
            <h3 className="text-xl font-bold text-gray-900">
              No creators found
            </h3>
            <p className="text-gray-500 mt-1">Try a different search term.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default CreatorCatalog;
