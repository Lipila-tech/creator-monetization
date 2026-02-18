import {
  PlayCircle,
  Share2,
  MessageCircle,
  TrendingUp,
  Copy,
  Check,
  Heart,
  MessageSquare,
  Video,
} from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faWhatsapp,
  faInstagram,
  faTiktok,
  faFacebook,
  faYoutube,
} from "@fortawesome/free-brands-svg-icons";

const Guide = ({ slug }) => {
  const [copied, setCopied] = useState(false);
  const [copiedScript, setCopiedScript] = useState(null);
  const { hash } = useLocation();
  const copyRef = useRef(null);

  const creatorLink = `${window.location.protocol}//${window.location.host}/creator-profile/${slug}`;

  const copyToClipboard = (text, type = "link") => {
    navigator.clipboard.writeText(text);

    if (type === "link") {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } else {
      setCopiedScript(type);
      setTimeout(() => setCopiedScript(null), 2000);
    }
  };

  useEffect(() => {
    if (hash === "#share") {
      copyRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [hash]);

  const scripts = [
    {
      id: "whatsapp",
      icon: <FontAwesomeIcon icon={faWhatsapp} className="text-green-500" />,
      platform: "WhatsApp Status / Story",
      script:
        "Hi family 👋 If you enjoy my content and would like to support me, I've shared a link where you can tip or subscribe using mobile money. Thank you so much 💛",
      bgColor: "bg-green-50",
      borderColor: "border-green-100",
    },
    {
      id: "instagram-tiktok",
      icon: (
        <>
          <FontAwesomeIcon icon={faTiktok} className="text-black" />{" "}
          <FontAwesomeIcon icon={faInstagram} className="text-pink-500" />
        </>
      ),
      platform: "Instagram / TikTok Video Script",
      script:
        "Quick message before the video 👋 If you enjoy my content and want to support me, I've added a link where you can tip or subscribe using mobile money. The link is in my bio — thank you 💛",
      bgColor: "bg-purple-50",
      borderColor: "border-purple-100",
    },
    {
      id: "soft-ask",
      icon: "💛",
      platform: "Soft Ask (Not Pushy)",
      script:
        "You don't have to support — watching and sharing already means a lot 💛 But if you want to support, I've shared a link where you can tip or subscribe using mobile money. Thank you always.",
      bgColor: "bg-yellow-50",
      borderColor: "border-yellow-100",
    },
  ];

  const platforms = [
    {
      name: "WhatsApp Status",
      icon: <FontAwesomeIcon icon={faWhatsapp} className="text-green-500" />,
    },
    {
      name: "Instagram Stories",
      icon: <FontAwesomeIcon icon={faInstagram} className="text-pink-500" />,
    },
    {
      name: "TikTok Bio",
      icon: <FontAwesomeIcon icon={faTiktok} className="text-black" />,
    },
    {
      name: "Facebook Posts",
      icon: <FontAwesomeIcon icon={faFacebook} className="text-blue-600" />,
    },
    {
      name: "YouTube Description",
      icon: <FontAwesomeIcon icon={faYoutube} className="text-red-500" />,
    },
    { name: "Live Videos", icon: "🔴" },
  ];

  return (
    <>
      <div className="max-w-4xl mx-auto space-y-8 px-4 py-6">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-zed-green/10 to-blue-50 rounded-3xl p-6 md:p-8">
          <h1 className="text-3xl md:text-4xl font-black text-gray-900 mb-4">
            Welcome to TipZed Creator Guide
          </h1>
          <p className="text-lg text-gray-600 mb-6">
            This guide helps you set up your creator page and start earning
            support from your audience using local payments.
          </p>
          <div className="flex items-center gap-2 text-sm font-bold text-zed-green">
            <PlayCircle size={20} />
            <span>No technical skills needed • Just share your link</span>
          </div>
        </div>

        {/* Benefits Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            {
              icon: "💸",
              title: "Receive Tips",
              desc: "One-time support from fans",
            },
            {
              icon: "📅",
              title: "Subscriptions",
              desc: "Monthly or yearly recurring",
            },
            {
              icon: "📱",
              title: "Mobile Money",
              desc: "Local payments in your country",
            },
            {
              icon: "💰",
              title: "Track Earnings",
              desc: "Real-time wallet updates",
            },
            {
              icon: "🏦",
              title: "Withdraw Locally",
              desc: "Direct to your bank/mobile",
            },
            {
              icon: "🎯",
              title: "Direct Support",
              desc: "You get paid immediately",
            },
          ].map((item, idx) => (
            <div
              key={idx}
              className="bg-white border border-gray-100 rounded-2xl p-5 hover:shadow-md transition-shadow"
            >
              <div className="text-2xl mb-3">{item.icon}</div>
              <h3 className="font-bold text-gray-900 mb-2">{item.title}</h3>
              <p className="text-sm text-gray-600">{item.desc}</p>
            </div>
          ))}
        </div>

        {/* Step-by-Step Guide */}
        <div className="space-y-6">
          <h2 className="text-2xl font-black text-gray-900">
            Your Step-by-Step Guide
          </h2>

          {/* Step 1 */}
          <div className="bg-white border border-gray-100 rounded-2xl p-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-10 h-10 bg-zed-green text-white rounded-full flex items-center justify-center font-black text-lg">
                1
              </div>
              <div>
                <h3 className="text-xl font-bold">Set Up Your Creator Page</h3>
                <p className="text-gray-600">
                  Takes 5 minutes • Complete all steps
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 ml-0 md:ml-14">
              <div className="bg-gray-50 rounded-xl p-4">
                <div className="font-bold text-gray-900 mb-2">✓ Sign up</div>
                <div className="text-xs text-gray-500">Already done!</div>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <div className="font-bold text-gray-900 mb-2">
                  Complete Profile
                </div>
                <div className="text-xs text-gray-500">Photo, cover, bio</div>
              </div>
              <div className="bg-zed-green/10 rounded-xl p-4 border border-zed-green/20">
                <div className="font-bold text-gray-900 mb-2">
                  Copy Your Link
                </div>
                <div className="text-xs text-zed-green font-bold">
                  Most important!
                </div>
              </div>
            </div>
          </div>

          {/* Step 2 - Sharing */}
          <div className="bg-white border border-gray-100 rounded-2xl p-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-10 h-10 bg-zed-green text-white rounded-full flex items-center justify-center font-black text-lg">
                2
              </div>
              <div>
                <h3 className="text-xl font-bold">
                  Share Your Link (Very Important!)
                </h3>
                <p className="text-gray-600">
                  Creators who share regularly earn 5x more
                </p>
              </div>
            </div>

            {/* Your Link Card */}
            <div className="bg-gradient-to-r from-zed-green/5 to-blue-50 rounded-xl p-5 mb-6">
              <div className="flex flex-col md:flex-row md:items-center gap-4">
                <div className="flex-1">
                  <label className="text-sm font-bold text-gray-500 mb-2 block">
                    Your Creator Link
                  </label>
                  <div className="flex items-center gap-3">
                    <div className="bg-white px-4 py-3 text-black rounded-lg border border-gray-200 font-mono text-sm flex-1 truncate">
                      {creatorLink}
                    </div>
                    <button
                      onClick={() => copyToClipboard(creatorLink, "link")}
                      className="bg-zed-green text-white px-5 py-3 rounded-lg font-bold hover:opacity-90 transition-opacity flex items-center gap-2 min-w-[100px] justify-center"
                    >
                      {copied ? <Check size={18} /> : <Copy size={18} />}
                      {copied ? "Copied!" : "Copy"}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Where to Share */}
            <div className="mb-6">
              <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Share2 size={18} />
                Where to Share (Share at least once a week)
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                {platforms.map((platform) => (
                  <div
                    key={platform.name}
                    className="bg-gray-50 rounded-xl p-4 text-center hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex justify-center text-xl mb-2">
                      {platform.icon}
                    </div>
                    <div className="text-xs font-medium text-gray-900 leading-tight">
                      {platform.name}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Scripts */}
            <div>
              <h4 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <MessageCircle size={18} />
                Ready-to-Use Promo Scripts
              </h4>
              <div className="space-y-4">
                {scripts.map((script) => (
                  <div
                    key={script.id}
                    className={`${script.bgColor} ${script.borderColor} rounded-xl p-5 border`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xl">{script.icon}</span>
                      <div className="font-bold text-gray-900">
                        {script.platform}
                      </div>
                    </div>
                    <p className="text-gray-700 mb-3 italic">
                      "{script.script}"
                    </p>
                    <button
                      onClick={() => copyToClipboard(script.script, script.id)}
                      className="text-sm text-zed-green font-bold hover:underline flex items-center gap-1"
                    >
                      {copiedScript === script.id ? (
                        <>
                          <Check size={14} />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy size={14} />
                          Copy Script
                        </>
                      )}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Steps 3 & 4 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border border-gray-100 rounded-2xl p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-10 h-10 bg-zed-green text-white rounded-full flex items-center justify-center font-black text-lg">
                  3
                </div>
                <h3 className="text-xl font-bold">Thank Your Supporters</h3>
              </div>
              <ul className="space-y-3 text-gray-600 ml-0 md:ml-14">
                <li className="flex items-center gap-2">
                  <MessageSquare size={16} className="text-zed-green" />
                  Reply privately
                </li>
                <li className="flex items-center gap-2">
                  <Video size={16} className="text-zed-green" />
                  Say thank you on your story
                </li>
                <li className="flex items-center gap-2">
                  <Heart size={16} className="text-zed-green" />
                  Mention supporters during live sessions
                </li>
              </ul>
              <p className="mt-4 text-sm text-gray-500 ml-0 md:ml-14">
                Gratitude builds trust and repeat support
              </p>
            </div>

            <div className="bg-white border border-gray-100 rounded-2xl p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-10 h-10 bg-zed-green text-white rounded-full flex items-center justify-center font-black text-lg">
                  4
                </div>
                <h3 className="text-xl font-bold">Keep Going</h3>
              </div>
              <div className="space-y-4 ml-0 md:ml-14">
                <div className="flex items-start gap-3">
                  <TrendingUp size={20} className="text-zed-green mt-1" />
                  <div>
                    <div className="font-bold text-gray-900">Share weekly</div>
                    <div className="text-sm text-gray-600">
                      Consistency is key
                    </div>
                  </div>
                </div>
                <div className="text-sm text-gray-600 space-y-1">
                  <p className="font-bold mb-1">Remember:</p>
                  <p className="flex items-start gap-1">
                    <span>•</span>
                    <span>You're not begging</span>
                  </p>
                  <p className="flex items-start gap-1">
                    <span>•</span>
                    <span>
                      You're giving fans a way to support work they value
                    </span>
                  </p>
                  <p className="flex items-start gap-1">
                    <span>•</span>
                    <span>Even small support adds up over time</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Final CTA */}
        <div className="bg-gradient-to-r from-zed-green to-emerald-600 rounded-2xl p-8 text-center text-white">
          <h3 className="text-2xl font-black mb-4">You're Ready to Start!</h3>
          <p className="mb-6 opacity-90">Create. Share. Earn.</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              ref={copyRef}
              onClick={() => copyToClipboard(creatorLink, "link")}
              className="bg-white text-zed-green px-8 py-3 rounded-xl font-bold hover:opacity-90 transition-opacity"
            >
              {copied ? "Copied!" : "Copy Your Link"}
            </button>
            <Link
              to="/creator-dashboard"
              className="border-2 border-white text-white px-8 py-3 rounded-xl font-bold hover:bg-white/10 transition-colors"
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Guide;
