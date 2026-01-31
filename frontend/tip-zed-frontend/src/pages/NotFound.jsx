import { Home, Search } from 'lucide-react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-6 py-16">
        <div className="max-w-2xl w-full text-center">
          {/* 404 Illustration */}
          <div className="mb-8">
            <div className="inline-block relative">
              <div className="text-9xl font-bold bg-gradient-to-r from-zed-green via-zed-orange to-zed-red bg-clip-text text-transparent">
                404
              </div>
              <div className="absolute -top-4 -right-4 w-16 h-16 bg-zed-orange/20 rounded-full animate-pulse"></div>
              <div className="absolute -bottom-4 -left-4 w-12 h-12 bg-zed-green/20 rounded-full animate-pulse delay-75"></div>
            </div>
          </div>

          {/* Message */}
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Creator Not Found
          </h1>
          <p className="text-lg text-gray-600 mb-10 max-w-md mx-auto leading-relaxed">
            Oops! The creator you're looking for doesn't exist or may have been removed. Let's get you back on track.
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/" className="inline-flex items-center justify-center gap-2 bg-zed-black text-white px-8 py-4 rounded-xl hover:bg-gray-800 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105">
              <Home size={20} />
              Go to Homepage
            </Link>
            <Link to="/creator-catalog" className="inline-flex items-center justify-center gap-2 bg-white text-zed-green border-2 border-zed-green px-8 py-4 rounded-xl hover:bg-zed-green hover:text-white transition-all font-semibold shadow-lg hover:shadow-xl transform hover:scale-105">
              <Search size={20} />
              Browse Creators
            </Link>
          </div>

          {/* Decorative Elements */}
          <div className="mt-16 grid grid-cols-3 gap-4 max-w-md mx-auto">
            <div className="h-2 bg-gradient-to-r from-zed-green to-transparent rounded-full"></div>
            <div className="h-2 bg-gradient-to-r from-zed-orange to-transparent rounded-full"></div>
            <div className="h-2 bg-gradient-to-r from-zed-red to-transparent rounded-full"></div>
          </div>
        </div>
      </main>

      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.5;
            transform: scale(1.1);
          }
        }
        
        .animate-pulse {
          animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        .delay-75 {
          animation-delay: 0.75s;
        }
      `}</style>
    </div>
  );
}

export default NotFound;