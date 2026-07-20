import { Copy, Check, Share2 } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const Guide = ({ slug }) => {
  const [copied, setCopied] = useState(false);
  const [copiedScript, setCopiedScript] = useState(false);

  const creatorLink = `${window.location.protocol}//${window.location.host}/${slug}`;
  const exampleScript = `Hi! I'm now on TipZed. If you'd like to support my work, you can send me a donation here: ${creatorLink}`;

  const copyToClipboard = (text, setFn) => {
    navigator.clipboard.writeText(text);
    setFn(true);
    setTimeout(() => setFn(false), 2000);
  };

  return (
    <div className="max-w-2xl mx-auto py-12 px-4">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-2">Share & Earn</h1>
        <p className="text-gray-600">The simplest way to start receiving support.</p>
      </div>

      <div className="bg-white border border-gray-100 rounded-3xl p-8 shadow-sm space-y-8">
        {/* The Link */}
        <div>
          <label className="block text-xs font-bold text-gray-400 uppercase mb-2">Your Link</label>
          <div className="flex gap-2">
            <div className="flex-1 bg-gray-50 px-4 py-3 rounded-xl border border-gray-100 font-mono text-sm truncate">
              {creatorLink}
            </div>
            <button 
              onClick={() => copyToClipboard(creatorLink, setCopied)}
              className="bg-zed-green text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2"
            >
              {copied ? <Check size={18} /> : <Copy size={18} />}
              {copied ? "Copied" : "Copy"}
            </button>
          </div>
        </div>

        {/* The Example */}
        <div className="pt-6 border-t border-gray-50">
          <div className="flex items-center gap-2 mb-4 text-gray-900 font-bold">
            <Share2 size={18} className="text-zed-green" />
            <span>Example Post (WhatsApp/Socials)</span>
          </div>
          <div className="bg-zed-green/5 rounded-2xl p-5 relative">
            <p className="text-gray-700 italic mb-4">"{exampleScript}"</p>
            <button 
              onClick={() => copyToClipboard(exampleScript, setCopiedScript)}
              className="text-zed-green font-bold text-sm flex items-center gap-2 hover:underline"
            >
              {copiedScript ? <Check size={16} /> : <Copy size={16} />}
              {copiedScript ? "Copied Message" : "Copy Message"}
            </button>
          </div>
        </div>
      </div>

      <div className="mt-8 text-center">
        <Link to="/creator-dashboard" className="text-gray-400 font-bold hover:text-gray-900 transition-colors">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default Guide;

