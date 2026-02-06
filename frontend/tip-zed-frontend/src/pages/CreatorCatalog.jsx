import React, { useState, useEffect } from "react";
import {
  Search,
  Music,
  Video,
  Palette,
  Mic,
  Loader,
  UserX,
} from "lucide-react";
import { Link } from "react-router-dom";
import { creatorService } from "../services/creatorService";

const getName = (creator) =>
  `${creator.user?.firstName || ""} ${creator.user?.lastName || ""}`.trim() ||
  creator.user?.username ||
  "Creator";

const CreatorCatalog = () => {
  const [creators, setCreators] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  // Later Add category state
  // const [selectedCategory, setSelectedCategory] = useState("All");

  useEffect(() => {
    const fetchCreators = async () => {
      try {
        const response = await creatorService.getAllCreators();
        if (response.status === "success") {
          setCreators(response.data);
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load creators. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchCreators();
  }, []);

  // Filter Logic
  const filteredCreators = creators.filter((c) =>
    getName(c).toLowerCase().includes(searchTerm.toLowerCase()),
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <Loader className="animate-spin text-zed-green" size={32} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative">
            <Search
              className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
              size={20}
            />
            <input
              type="text"
              placeholder="Search creators..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3.5 bg-white text-gray-900 placeholder-gray-400 caret-zed-green border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-zed-green"
            />
          </div>
        </div>

        {/* Category Buttons (Visual Only for now) */}
        <div className="flex flex-wrap gap-3 mb-8">
          {["Music", "Video", "Art", "Podcast"].map((cat) => (
            <button
              key={cat}
              onClick={() => console.log("Category filter not implemented yet")}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:border-zed-green hover:bg-zed-green/5 transition-colors text-gray-700 font-medium text-sm"
            >
              {cat === "Music" && <Music size={18} />}
              {cat === "Video" && <Video size={18} />}
              {cat === "Art" && <Palette size={18} />}
              {cat === "Podcast" && <Mic size={18} />}
              {cat}
            </button>
          ))}
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Featured Creators
        </h2>

        {error && <div className="text-red-500 mb-4">{error}</div>}

        {/* Grid or Empty State */}
        {filteredCreators.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {filteredCreators.map((creator) => (
              <Link
                to={`/creator-profile/${creator.user.slug}`}
                key={creator.user.id}
                className="block"
              >
                <div className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all cursor-pointer group border border-gray-100 h-full">
                  <div className="aspect-square overflow-hidden bg-gray-100 relative">
                    {creator.profileImage ? (
                      <img
                        src={creator.profileImage}
                        alt={getName(creator)}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full bg-gray-200 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
                        <span className="text-5xl font-bold text-gray-400">
                          {getName(creator)?.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="p-5">
                    <h3 className="font-bold text-lg text-gray-900 mb-2">
                      {getName(creator)}
                    </h3>
                    <span className="inline-block bg-zed-green text-white text-xs font-semibold px-3 py-1 rounded-full mb-3">
                      {creator.user.userType}
                    </span>
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                      {creator.bio || "No bio available."}
                    </p>
                    <p className="text-gray-500 text-sm">
                      {creator.followersCount} supporters
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <div className="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <UserX className="text-gray-400" size={32} />
            </div>
            <h3 className="text-lg font-medium text-gray-900">
              No creators found
            </h3>
            <p className="text-gray-500">Try searching for a different name.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default CreatorCatalog;
