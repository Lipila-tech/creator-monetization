import { 
  ArrowRight, 
  XCircle, 
  CheckCircle, 
  Heart, 
  Repeat, 
  Lock 
} from "lucide-react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    // Added pb-24 to account for the sticky mobile CTA
    <div className="min-h-screen bg-gray-50 pb-24 md:pb-0 font-sans">
      
      {/*  HERO SECTION */}
      <section className="relative bg-zed-black overflow-hidden pt-20 pb-16 px-6 text-center">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-br from-zed-green/20 via-transparent to-zed-orange/20 blur-3xl opacity-50 z-0 pointer-events-none"></div>
        
        <div className="max-w-3xl mx-auto relative z-10">
          <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-6 tracking-tight leading-[1.1]">
            Get paid by your fans. <span className="text-zed-green">Locally.</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-10 leading-relaxed max-w-xl mx-auto">
            Subscriptions and tips using mobile money — built for African creators.
          </p>

          {/* CTAs */}
          <div className="flex flex-col md:flex-row items-center justify-center gap-5">
            <Link
              to="#"
              className="w-full md:w-auto bg-zed-green text-white px-8 py-4 rounded-xl hover:bg-green-600 transition-all font-bold text-lg shadow-[0_4px_14px_0_rgba(0,255,100,0.39)] active:scale-95"
            >
              Start as a Creator
            </Link>
            <Link
              to="/creator-catalog"
              className="w-full md:w-auto text-white flex items-center justify-center px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/10 transition-all active:scale-95"
            >
              Support a creator <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* TRUST SECTION */}
      <section className="py-8 px-6 bg-white border-b border-gray-100">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">
            Works with local payments
          </p>
          <div className="flex flex-wrap justify-center items-center gap-x-8 gap-y-4 text-gray-600 font-semibold md:text-lg">
            <span>Airtel</span>
            <span className="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
            <span>MTN</span>
            <span className="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
            <span>Zamtel</span>
            <span className="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
            <span>Mobile Money</span>
          </div>
        </div>
      </section>

      {/* THE PROBLEM */}
      <section className="py-20 px-6 bg-gray-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-12 leading-tight">
            Creating is hard.<br />
            <span className="text-gray-400">Getting paid shouldn’t be.</span>
          </h2>

          <div className="space-y-6 mb-12">
            <div className="flex items-center gap-4 bg-white p-5 rounded-2xl shadow-sm">
              <XCircle className="text-red-500 flex-shrink-0" size={28} />
              <span className="font-semibold text-xl text-gray-800">PayPal doesn’t work</span>
            </div>
            <div className="flex items-center gap-4 bg-white p-5 rounded-2xl shadow-sm">
              <XCircle className="text-red-500 flex-shrink-0" size={28} />
              <span className="font-semibold text-xl text-gray-800">Cards fail</span>
            </div>
            <div className="flex items-center gap-4 bg-green-50 p-5 rounded-2xl shadow-sm border border-green-100">
              <CheckCircle className="text-zed-green flex-shrink-0" size={28} />
              <span className="font-semibold text-xl text-gray-900">Fans use mobile money</span>
            </div>
          </div>

          <p className="text-xl md:text-2xl font-medium text-gray-700 leading-relaxed bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
            You have supporters — but <span className="text-zed-orange">no easy way</span> to accept support.
          </p>
        </div>
      </section>

      {/* THE SOLUTION */}
      <section className="py-20 px-6 bg-zed-black text-white">
        <div className="max-w-4xl mx-auto">
          <p className="text-zed-green font-bold tracking-widest uppercase mb-3 text-sm">Meet TipZed</p>
          <h2 className="text-3xl md:text-4xl font-bold mb-10 leading-tight">
            TipZed lets fans support you using local payments.
          </h2>
          
          <p className="text-xl mb-6 font-medium text-gray-300">You get:</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            <div className="bg-white/10 p-6 rounded-2xl text-center backdrop-blur-sm">
              <p className="font-bold text-lg">Tips</p>
            </div>
            <div className="bg-white/10 p-6 rounded-2xl text-center backdrop-blur-sm">
              <p className="font-bold text-lg">Subscriptions</p>
            </div>
            <div className="bg-white/10 p-6 rounded-2xl text-center backdrop-blur-sm">
              <p className="font-bold text-lg">A wallet</p>
            </div>
            <div className="bg-white/10 p-6 rounded-2xl text-center backdrop-blur-sm">
              <p className="font-bold text-lg">Local payouts</p>
            </div>
          </div>

          <div className="bg-gradient-to-r from-zed-orange/20 to-transparent p-6 rounded-2xl border-l-4 border-zed-orange">
            <p className="text-xl font-semibold">No bank accounts. No complicated setup.</p>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16 text-gray-900">How It Works</h2>
          
          <div className="space-y-8 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-1 before:bg-gray-100">
            {[
              { step: "1", title: "Create your page" },
              { step: "2", title: "Share your link" },
              { step: "3", title: "Fans tip or subscribe" },
              { step: "4", title: "Withdraw locally" },
            ].map((item, index) => (
              <div key={index} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                {/* Icon Marker */}
                <div className="flex items-center justify-center w-12 h-12 rounded-full border-4 border-white bg-zed-green text-white font-bold text-xl shadow-md shrink-0 md:absolute md:left-1/2 md:-translate-x-1/2 z-10">
                  {item.step}
                </div>
                {/* Content Card */}
                <div className="bg-gray-50 p-6 rounded-2xl shadow-sm w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] font-semibold text-xl text-gray-800">
                  {item.title}
                </div>
              </div>
            ))}
          </div>
          
          <p className="text-center font-extrabold text-3xl mt-16 text-gray-900">That’s it.</p>
        </div>
      </section>

      {/* HOW YOU EARN */}
      <section className="py-20 px-6 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-900">How You Earn</h2>
          <div className="grid md:grid-cols-3 gap-6">
            
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 text-center">
              <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <Heart size={32} />
              </div>
              <h3 className="text-2xl font-bold mb-3">Tipping</h3>
              <p className="text-gray-600 font-medium">One-time “thank you” payments</p>
            </div>

            <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 text-center">
              <div className="w-16 h-16 bg-green-50 text-zed-green rounded-full flex items-center justify-center mx-auto mb-6">
                <Repeat size={32} />
              </div>
              <h3 className="text-2xl font-bold mb-3">Subscriptions</h3>
              <p className="text-gray-600 font-medium">Monthly or yearly support</p>
            </div>

            <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 text-center">
              <div className="w-16 h-16 bg-purple-50 text-purple-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <Lock size={32} />
              </div>
              <h3 className="text-2xl font-bold mb-3">Exclusive Access</h3>
              <p className="text-gray-600 font-medium">Private content or close community</p>
            </div>

          </div>
        </div>
      </section>

      {/* WHY CREATORS CHOOSE TIPZED */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-12 text-gray-900">Why Creators Choose TipZed</h2>
          <div className="flex flex-wrap justify-center gap-4">
            {[
              "Built for Africa",
              "Mobile money friendly",
              "No monthly fees",
              "Transparent wallet",
              "Fast payouts",
              "Real support"
            ].map((benefit, i) => (
              <span key={i} className="bg-gray-100 text-gray-800 px-6 py-3 rounded-full text-lg font-semibold">
                {benefit}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* PRICING */}
      <section className="py-20 px-6 bg-yellow-50 text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-5xl font-black text-gray-900 mb-6 tracking-tight">No monthly fees.</h2>
          <p className="text-2xl text-gray-700 font-medium mb-10">Small fee per payment.</p>
          <div className="bg-white inline-block px-8 py-5 rounded-full shadow-sm border border-yellow-200">
            <p className="text-xl font-bold text-zed-orange">
              Early creators get <span className="text-2xl">0%</span> fees for 30 days.
            </p>
          </div>
        </div>
      </section>

      {/* FOR FANS */}
      <section className="py-16 px-6 bg-gray-900 text-center">
        <div className="max-w-xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-4">For Fans</h2>
          <p className="text-lg text-gray-300 mb-6 font-medium">
            Support creators easily. Tip or subscribe using local payments.
          </p>
          <div className="inline-flex items-center gap-2 bg-red-500/10 text-red-400 px-6 py-3 rounded-full font-bold">
            <XCircle size={20} />
            <span>No cards. No PayPal.</span>
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="py-24 px-6 bg-gradient-to-br from-zed-green to-teal-700 text-center text-white">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-10 leading-tight">
            Start earning from your audience
          </h2>
          <Link
            to="#"
            className="block w-full md:inline-block md:w-auto bg-white text-zed-green px-10 py-5 rounded-2xl hover:bg-gray-50 transition-all font-bold text-xl shadow-xl active:scale-95"
          >
            Create your creator page
          </Link>
        </div>
      </section>

      {/* STICKY MOBILE CTA (Always Visible on smaller screens) */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-white/90 backdrop-blur-md border-t border-gray-200 z-50 md:hidden shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
        <Link
          to="#"
          className="flex w-full bg-zed-green text-white items-center justify-center py-4 rounded-xl font-bold text-lg shadow-lg active:scale-95 transition-transform"
        >
          Start as a Creator
        </Link>
      </div>

    </div>
  );
};

export default Home;