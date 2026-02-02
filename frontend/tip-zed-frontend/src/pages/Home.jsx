import { Wallet, Zap, Users, Shield } from "lucide-react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section with Gradient */}
      <section className="relative bg-gradient-to-r from-zed-orange via-yellow-500 via-zed-green to-zed-black overflow-hidden">
        <div className="max-w-6xl mx-auto px-6 py-20 text-center relative z-10">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-5 tracking-tight leading-tight">
            Empower Zambian Creators
          </h1>
          <p className="text-lg text-white/95 mb-8 max-w-2xl mx-auto leading-relaxed">
            Support your favorite Zambian creators with mobile money tips. Fast,
            secure, and built for Zambia.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              to="/creator-catalog"
              className="bg-zed-black text-white px-7 py-3.5 rounded-lg hover:bg-gray-900 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Discover Creators
            </Link>
            <Link
              to="#"
              className="bg-white text-zed-green px-7 py-3.5 rounded-lg hover:bg-gray-50 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Become a Creator
            </Link>
          </div>
        </div>
      </section>

      {/* Why TipZed Section */}
      <section className="py-16 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-14 text-gray-900">
            Why TipZed?
          </h2>

          <div className="grid md:grid-cols-4 gap-8">
            {/* Mobile Money */}
            <div className="text-center group">
              <div className="mb-5 flex justify-center">
                <div className="w-16 h-16 bg-green-50 rounded-2xl flex items-center justify-center group-hover:bg-green-100 transition-colors">
                  <Wallet className="text-zed-green" size={32} />
                </div>
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">
                Mobile Money
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Pay with MTN, Airtel, or Zamtel mobile money
              </p>
            </div>

            {/* Instant Tips */}
            <div className="text-center group">
              <div className="mb-5 flex justify-center">
                <div className="w-16 h-16 bg-yellow-50 rounded-2xl flex items-center justify-center group-hover:bg-yellow-100 transition-colors">
                  <Zap className="text-zed-orange" size={32} />
                </div>
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">
                Instant Tips
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Quick K10, K20, or custom amount tipping
              </p>
            </div>

            {/* For Creators */}
            <div className="text-center group">
              <div className="mb-5 flex justify-center">
                <div className="w-16 h-16 bg-red-50 rounded-2xl flex items-center justify-center group-hover:bg-red-100 transition-colors">
                  <Users className="text-zed-red" size={32} />
                </div>
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">
                For Creators
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Musicians, artists, influencers, and more
              </p>
            </div>

            {/* Secure */}
            <div className="text-center group">
              <div className="mb-5 flex justify-center">
                <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center group-hover:bg-gray-200 transition-colors">
                  <Shield className="text-zed-black" size={32} />
                </div>
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">Secure</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Safe and reliable transactions every time
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <div className="bg-gradient-to-r from-zed-green via-yellow-500 to-zed-orange rounded-3xl px-12 py-14 text-center shadow-xl">
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to get started?
            </h2>
            <p className="text-lg text-white/95 mb-8 max-w-xl mx-auto">
              Join TipZed today and start supporting Zambian talent
            </p>
            <Link
              to="/creator-catalog"
              className="bg-zed-green text-white px-9 py-3.5 rounded-lg hover:bg-green-700 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Explore Creators
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
