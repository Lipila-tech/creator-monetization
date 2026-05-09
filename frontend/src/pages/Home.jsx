import {HashLink as Hlink} from 'react-router-hash-link';
import {
  ArrowDown,
  XCircle,
  Heart,
  Repeat,
  Lock,
} from "lucide-react";
import { Link } from "react-router-dom";
import MetaTags from "@/components/Common/MetaTags";
import bannerImage from "@/assets/images/banner.webp";

const Home = () => {
  return (
    <>
      <MetaTags
        title="TipZed | Local Support for Zambian Creators"
        description="Get tipped and subscribed directly via Mobile Money. The simplest way for Zambian creators to earn from their audience."
        keywords="Zambian creators, mobile money tips, support creators, Zambia, TipZed"
        image={bannerImage}
      />

      <div className="min-h-screen bg-white font-sans text-gray-900">
        {/* HERO */}
        <section 
          className="relative bg-black pt-24 pb-20 px-6 text-center overflow-hidden"
          style={{
            backgroundImage: `url(${bannerImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        >
          <div className="absolute inset-0 bg-black/70 z-0"></div>
          
          <div className="max-w-3xl mx-auto relative z-10">
            <h1 className="text-3xl md:text-4xl font-black text-white mb-4 tracking-tight leading-tight">
              Fund your creative vision <br />
              <span className="text-zed-green text-2xl md:text-3xl">Monetize your passion effortlessly.</span>
            </h1>
            <p className="text-base md:text-lg text-gray-300 mb-8 max-w-xl mx-auto font-medium">
              Gather support, build your membership, and launch your shop. It's more accessible than you'd imagine.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to="/register"
                className="w-full sm:w-auto bg-zed-green text-white px-8 py-3.5 rounded-xl hover:bg-green-600 transition-all font-bold text-base shadow-lg active:scale-95"
              >
                Start my page
              </Link>
              <Link
                to="/creator-catalog"
                className="w-full sm:w-auto bg-white/10 text-white border border-white/20 px-8 py-3.5 rounded-xl hover:bg-white/20 transition-all font-bold text-base active:scale-95"
              >
                Explore Creators
              </Link>
            </div>
          </div>
        </section>

        {/* THE PITCH */}
        <section className="py-16 px-6 max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-2xl font-black mb-4 uppercase tracking-widest text-xs text-zed-orange">
                The Reality
              </h2>
              <p className="text-lg text-gray-700 leading-relaxed font-medium">
                You're creating amazing content on TikTok, Facebook, and YouTube, and your fans love it. But while they're ready to support you, global platforms make it nearly impossible to get paid locally here in Zambia.
              </p>
            </div>
            <div className="bg-gray-50 p-8 rounded-[2rem] border-2 border-gray-100">
              <h2 className="text-2xl font-black mb-4 uppercase tracking-widest text-xs text-zed-green">
                The Fix
              </h2>
              <p className="text-lg text-gray-700 leading-relaxed font-medium">
                TipZed is your direct connection. We bridge the gap by letting your loyal fans support you instantly using Mobile Money—the way Zambians actually pay. No cards, no complications.
              </p>
            </div>
          </div>
        </section>

        {/* HOW IT WORKS (COMPACT) */}
        <section className="py-16 px-6 bg-gray-50">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-xl font-black text-center mb-12 uppercase tracking-[0.2em] text-gray-400 text-xs">
              How it works
            </h2>
            <div className="grid sm:grid-cols-3 gap-8">
              {[
                { icon: <div className="w-10 h-10 rounded-full bg-zed-green/10 flex items-center justify-center text-zed-green font-bold">1</div>, title: "Create your page", desc: "Set up your profile in less than a minute." },
                { icon: <div className="w-10 h-10 rounded-full bg-zed-green/10 flex items-center justify-center text-zed-green font-bold">2</div>, title: "Share your link", desc: "Post your payment link on your TikTok, FB, or YouTube." },
                { icon: <div className="w-10 h-10 rounded-full bg-zed-green/10 flex items-center justify-center text-zed-green font-bold">3</div>, title: "Get tipped", desc: "Fans support you instantly via Mobile Money." }
              ].map((item, i) => (
                <div key={i} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="mb-4">{item.icon}</div>
                  <h3 className="text-lg font-bold mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-500 font-medium leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* PRICING (MINIMAL) */}
        <section className="py-16 px-6 text-center">
          <div className="max-w-xl mx-auto">
            <h2 className="text-2xl font-black mb-4">No monthly fees. Period.</h2>
            <p className="text-gray-500 mb-8 font-medium">
              We only win when you do. We take a small flat fee per transaction to keep the lights on.
            </p>
            <div className="inline-block bg-zed-green/10 text-zed-green px-6 py-2 rounded-full text-sm font-bold">
              Early creators: 0% fees for your first 30 days
            </div>
          </div>
        </section>

        {/* FINAL CALL */}
        <section className="py-20 px-6 bg-zed-black text-center">
          <div className="max-w-2xl mx-auto">
            <h2 className="text-3xl font-black text-white mb-8 leading-tight">
              Ready to turn your audience <br />
              into a community?
            </h2>
            <Link
              to="/register"
              className="inline-block bg-zed-green text-white px-10 py-4 rounded-2xl hover:bg-green-600 transition-all font-black text-lg shadow-xl active:scale-95"
            >
              Start Earning Now
            </Link>
            <p className="mt-6 text-gray-500 text-sm font-medium">
              Takes less than a minute to set up.
            </p>
          </div>
        </section>
      </div>
    </>
  );
};

export default Home;

