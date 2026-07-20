import { useState, useEffect } from "react";
import { 
  Users, 
  MessageSquare, 
  Calendar, 
  TrendingUp, 
  Share2, 
  Copy, 
  Check,
  User
} from "lucide-react";
import { walletService } from "@/services/walletService";

const Supporters = () => {
  const [supporters, setSupporters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const fetchSupporters = async () => {
      try {
        setLoading(true);
        const data = await walletService.getSupporters();
        
        // The backend already returns completed payments with patron info
        const donations = (data.data || []).map(txn => ({
          id: txn.id,
          name: txn.patronName || "Anonymous",
          message: txn.patronMessage || "",
          amount: txn.amount,
          date: new Date(txn.createdAt).toLocaleDateString(),
          time: new Date(txn.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }));

        setSupporters(donations);
      } catch (err) {
        console.error("Error fetching supporters:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSupporters();
  }, []);

  const shoutoutText = supporters.length > 0 
    ? `Big shout out to my latest supporters on TipZed: ${supporters.slice(0, 3).map(s => s.name).join(", ")}${supporters.length > 3 ? " and others" : ""}! 💛 Your support keeps me going. Send me a donation here: ${window.location.origin}/${localStorage.getItem("user_slug") || ""}`
    : `Huge thanks to everyone supporting my creative journey on TipZed! 💛 You can support me here: ${window.location.origin}/${localStorage.getItem("user_slug") || ""}`;

  const copyShoutout = () => {
    navigator.clipboard.writeText(shoutoutText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-10 bg-gray-200 w-1/3 rounded-lg"></div>
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-24 bg-gray-100 rounded-2xl"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-zed-green/10 rounded-xl text-zed-green">
              <Users size={20} />
            </div>
            <span className="text-sm font-bold text-gray-500 uppercase tracking-wider">Total Supporters</span>
          </div>
          <div className="text-3xl font-black text-gray-900">{supporters.length}</div>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-50 rounded-xl text-blue-600">
              <MessageSquare size={20} />
            </div>
            <span className="text-sm font-bold text-gray-500 uppercase tracking-wider">Messages</span>
          </div>
          <div className="text-3xl font-black text-gray-900">
            {supporters.filter(s => s.message).length}
          </div>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-purple-50 rounded-xl text-purple-600">
              <TrendingUp size={20} />
            </div>
            <span className="text-sm font-bold text-gray-500 uppercase tracking-wider">Engagement</span>
          </div>
          <div className="text-3xl font-black text-gray-900">High</div>
        </div>
      </div>

      {/* Shout-out Section */}
      <div className="bg-gradient-to-r from-zed-green to-emerald-600 rounded-[2.5rem] p-8 text-white shadow-xl shadow-zed-green/20">
        <div className="flex items-center gap-3 mb-4">
          <Share2 size={24} />
          <h3 className="text-xl font-black">Give a Shout-out</h3>
        </div>
        <p className="opacity-90 mb-6 text-sm leading-relaxed">
          Show appreciation to your supporters by sharing a shout-out on your WhatsApp Status, Instagram, or Facebook.
        </p>
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 relative group">
          <p className="text-sm italic leading-relaxed pr-10">
            "{shoutoutText}"
          </p>
          <button 
            onClick={copyShoutout}
            className="absolute top-4 right-4 p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
            title="Copy shout-out text"
          >
            {copied ? <Check size={18} /> : <Copy size={18} />}
          </button>
        </div>
        {copied && (
          <p className="text-xs font-bold mt-3 animate-pulse">Copied to clipboard! Ready to post.</p>
        )}
      </div>

      {/* Supporters List */}
      <div className="space-y-4">
        <h3 className="text-xl font-black text-gray-900 flex items-center gap-2">
          Recent Supporters
        </h3>

        {supporters.length === 0 ? (
          <div className="bg-white border border-dashed border-gray-200 rounded-3xl py-16 text-center">
            <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="text-gray-300" size={32} />
            </div>
            <h4 className="font-bold text-gray-900 mb-1">No supporters yet</h4>
            <p className="text-sm text-gray-500">Share your link to start receiving donations!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {supporters.map((supporter) => (
              <div 
                key={supporter.id} 
                className="bg-white border border-gray-100 rounded-3xl p-6 hover:shadow-md transition-shadow flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center shrink-0">
                    <User className="text-gray-400" size={24} />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-black text-gray-900">{supporter.name}</h4>
                      <span className="text-xs font-bold text-zed-green bg-zed-green/10 px-2 py-0.5 rounded-full">
                        K{supporter.amount}
                      </span>
                    </div>
                    {supporter.message ? (
                      <p className="text-gray-600 text-sm italic">"{supporter.message}"</p>
                    ) : (
                      <p className="text-gray-400 text-xs italic">No message left</p>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-4 text-xs font-bold text-gray-400 shrink-0">
                  <div className="flex items-center gap-1">
                    <Calendar size={14} />
                    {supporter.date}
                  </div>
                  <div>{supporter.time}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Supporters;

