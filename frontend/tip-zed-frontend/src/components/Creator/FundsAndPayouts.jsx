import { useState, useEffect } from "react";
import {
  Wallet,
  ArrowUpRight,
  TrendingUp,
  Calendar,
  Clock,
  AlertCircle,
  ChevronRight,
  Landmark,
} from "lucide-react";
import { walletService } from "../../services/walletService";

const Shimmer = ({ className = "" }) => (
  <div
    className={`animate-pulse bg-gradient-to-r from-gray-100 via-gray-200 to-gray-100 bg-[length:400%_100%] rounded-xl ${className}`}
    style={{
      animation: "shimmer 2s ease-in-out infinite",
    }}
  />
);

const ShimmerStyles = () => (
  <style>{`
    @keyframes shimmer {
      0%   { background-position: 100% 50%; }
      100% { background-position: 0%   50%; }
    }
  `}</style>
);

const StatCardSkeleton = () => (
  <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
    <div className="flex justify-between items-start mb-4">
      <Shimmer className="w-12 h-12 rounded-2xl" />
      <Shimmer className="w-8 h-8 rounded-full" />
    </div>
    <Shimmer className="h-4 w-28 mb-3" />
    <Shimmer className="h-10 w-40" />
  </div>
);

const PayoutInfoSkeleton = () => (
  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-8 bg-gray-50/80 rounded-2xl p-6 border border-gray-100">
    {[0, 1, 2].map((i) => (
      <div key={i} className={i !== 2 ? "md:border-r md:border-gray-200/60 pr-4" : ""}>
        <div className="flex items-center gap-2 mb-3">
          <Shimmer className="h-4 w-4 rounded-full" />
          <Shimmer className="h-3.5 w-24" />
        </div>
        <Shimmer className="h-8 w-32" />
      </div>
    ))}
  </div>
);

const FundsAndPayouts = ({ walletData, loading }) => {
  const [hasPayoutData, setHasPayoutData] = useState(true);
  const [data, setData] = useState(null);
  const [innerLoading, setInnerLoading] = useState(false);
  const [payoutError, setPayoutError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setInnerLoading(true);
      try {
        const response = await walletService.getPayoutsData();
        if (response) {
          setData(response);
          setHasPayoutData(true);
        }
      } catch (err) {
        console.error(err);
        setPayoutError(err?.response?.data?.message || "Failed to load payout schedule.");
      } finally {
        setInnerLoading(false);
      }
    };

    fetchData();
  }, []);

  const isLoading = loading || innerLoading;

  return (
    <div className="min-h-screen bg-gray-50/50 p-4 md:p-8 font-sans">
      <ShimmerStyles />
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-gray-100">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-50 text-green-700 text-xs font-bold tracking-wide uppercase mb-3 border border-green-100">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              Wallet Active
            </div>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Funds & Payouts</h1>
            <p className="text-gray-500 mt-2 text-sm md:text-base max-w-lg leading-relaxed">
              Track your earnings, manage your available balance, and view your upcoming withdrawal schedule.
            </p>
          </div>
          <div className="hidden md:flex items-center gap-2 text-gray-400 bg-gray-50 px-4 py-2 rounded-xl border border-gray-100">
             <Landmark size={18} />
             <span className="text-sm font-medium">Standard Bank Settlement</span>
          </div>
        </div>

        {/* ── Stat Cards ── */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {isLoading ? (
            <>
              <StatCardSkeleton />
              <StatCardSkeleton />
              <StatCardSkeleton />
            </>
          ) : walletData ? (
            <>
              {/* Available Balance */}
              <div className="group bg-gradient-to-br from-green-500 to-green-600 p-6 md:p-8 rounded-3xl shadow-md border border-green-400 text-white relative overflow-hidden transition-transform hover:-translate-y-1 duration-300">
                <div className="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 rounded-full bg-white opacity-10 blur-2xl group-hover:opacity-20 transition-opacity"></div>
                <div className="flex justify-between items-start mb-8 relative z-10">
                  <div className="p-3 bg-white/20 backdrop-blur-sm rounded-2xl">
                    <Wallet size={26} className="text-white" />
                  </div>
                  <button className="p-2 bg-white/10 hover:bg-white/20 rounded-full backdrop-blur-sm transition-colors">
                    <ChevronRight size={20} />
                  </button>
                </div>
                <div className="relative z-10">
                  <h2 className="text-green-50 text-sm font-semibold mb-1 tracking-wide">Available Balance</h2>
                  <div className="flex items-baseline gap-1">
                    <span className="text-2xl font-bold opacity-80">{walletData.currency}</span>
                    <p className="text-4xl md:text-5xl font-black tracking-tight">
                      {walletData.balance}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Total Paid Out */}
              <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-gray-100 transition-shadow hover:shadow-md duration-300 group">
                <div className="flex justify-between items-start mb-8">
                  <div className="p-3 bg-orange-50 text-orange-500 rounded-2xl group-hover:scale-110 transition-transform duration-300">
                    <ArrowUpRight size={26} strokeWidth={2.5} />
                  </div>
                </div>
                <div>
                  <h2 className="text-gray-500 text-sm font-semibold mb-1 tracking-wide">Total Paid Out</h2>
                  <div className="flex items-baseline gap-1">
                    <span className="text-lg font-bold text-gray-400">{walletData.currency}</span>
                    <p className="text-3xl font-black text-gray-900 tracking-tight">
                      {walletData.cashOut}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Lifetime Earnings */}
              <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-gray-100 transition-shadow hover:shadow-md duration-300 group">
                <div className="flex justify-between items-start mb-8">
                  <div className="p-3 bg-blue-50 text-blue-500 rounded-2xl group-hover:scale-110 transition-transform duration-300">
                    <TrendingUp size={26} strokeWidth={2.5} />
                  </div>
                </div>
                <div>
                  <h2 className="text-gray-500 text-sm font-semibold mb-1 tracking-wide">Lifetime Earnings</h2>
                  <div className="flex items-baseline gap-1">
                    <span className="text-lg font-bold text-gray-400">{walletData.currency}</span>
                    <p className="text-3xl font-black text-gray-900 tracking-tight">
                      {walletData.cashIn}
                    </p>
                  </div>
                </div>
              </div>
            </>
          ) : (
            // Fallback if walletData is missing entirely
            <div className="col-span-1 md:col-span-3 bg-white p-12 rounded-3xl border border-gray-100 text-center flex flex-col items-center justify-center gap-4">
              <div className="p-4 bg-gray-50 rounded-full text-gray-400">
                 <Wallet size={32} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">Data Unavailable</h3>
                <p className="text-gray-500 mt-1 max-w-sm mx-auto">We couldn't load your wallet statistics at this time. Please try refreshing.</p>
              </div>
            </div>
          )}
        </div>

        {/* ── Next Payout + Withdraw ── */}
        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
          {/* Header */}
          <div className="p-6 md:p-8 border-b border-gray-100 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                <div className="p-2 bg-gray-50 rounded-lg">
                  <Calendar size={20} className="text-gray-700" />
                </div>
                Next Payout Schedule
              </h2>
            </div>
            
            {/* Withdraw Button (Moved to top for better UX) */}
            <div>
              {isLoading ? (
                <Shimmer className="w-32 h-10 rounded-xl" />
              ) : (
                <button
                  disabled
                  className="w-full md:w-auto px-6 py-2.5 bg-gray-900 hover:bg-gray-800 text-white text-sm font-bold rounded-xl opacity-50 cursor-not-allowed flex items-center justify-center gap-2 transition-all"
                >
                  <Wallet size={16} />
                  Withdraw Funds
                </button>
              )}
            </div>
          </div>

          <div className="p-6 md:p-8 bg-white">
            {isLoading ? (
              <PayoutInfoSkeleton />
            ) : payoutError ? (
              /* Error State */
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between bg-red-50/50 text-red-800 rounded-2xl p-6 border border-red-100 gap-4">
                <div className="flex items-start sm:items-center gap-3">
                  <div className="p-2 bg-red-100 rounded-lg shrink-0">
                    <AlertCircle size={20} className="text-red-600" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm">Failed to load schedule</h4>
                    <p className="text-sm text-red-600/80 mt-0.5">{payoutError}</p>
                  </div>
                </div>
                <button 
                  onClick={() => window.location.reload()} 
                  className="px-5 py-2.5 bg-white border border-red-200 text-red-600 text-sm font-bold rounded-xl hover:bg-red-50 transition-colors shadow-sm w-full sm:w-auto"
                >
                  Try Again
                </button>
              </div>
            ) : hasPayoutData && data ? (
              /* Active Schedule State */
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-0 bg-gray-50/50 rounded-2xl p-6 border border-gray-100">
                {/* Estimated Amount */}
                <div className="md:border-r md:border-gray-200/60 md:pr-6 flex flex-col justify-center">
                  <p className="text-sm text-gray-500 font-semibold mb-2 flex items-center gap-1.5 uppercase tracking-wider text-[11px]">
                     <TrendingUp size={14} className="text-green-500"/> Estimated Amount
                  </p>
                  <div className="flex items-baseline gap-1">
                    <span className="text-xl font-bold text-gray-400">{walletData?.currency || ""}</span>
                    <p className="text-3xl font-black text-green-600 tracking-tight">
                      {data.estimatedAmount}
                    </p>
                  </div>
                </div>
                
                {/* Payout Date */}
                <div className="md:border-r md:border-gray-200/60 md:px-6 flex flex-col justify-center pt-4 md:pt-0 border-t border-gray-200/60 md:border-t-0">
                  <p className="text-sm text-gray-500 font-semibold mb-2 flex items-center gap-1.5 uppercase tracking-wider text-[11px]">
                    <Calendar size={14} className="text-blue-500"/> Scheduled Date
                  </p>
                  <p className="text-xl font-bold text-gray-900">{data.date}</p>
                </div>
                
                {/* Schedule Type */}
                <div className="md:pl-6 flex flex-col justify-center pt-4 md:pt-0 border-t border-gray-200/60 md:border-t-0">
                  <p className="text-sm text-gray-500 font-semibold mb-2 flex items-center gap-1.5 uppercase tracking-wider text-[11px]">
                    <Clock size={14} className="text-orange-500"/> Frequency
                  </p>
                  <div className="flex items-center gap-2">
                     <p className="text-xl font-bold text-gray-900 capitalize">{data.schedule}</p>
                     <span className="px-2 py-0.5 bg-gray-200 text-gray-600 text-[10px] font-bold uppercase rounded-md tracking-wider">Auto</span>
                  </div>
                </div>
              </div>
            ) : (
              /* Empty State */
              <div className="flex flex-col items-center justify-center py-12 px-4 bg-gray-50/50 rounded-2xl border border-dashed border-gray-200 text-center">
                <div className="p-4 bg-white rounded-2xl shadow-sm border border-gray-100 mb-4">
                  <AlertCircle size={28} className="text-gray-400" />
                </div>
                <h3 className="text-gray-900 font-bold text-lg mb-1.5">No active payout schedule</h3>
                <p className="text-sm text-gray-500 max-w-sm leading-relaxed">
                  Your next payout date and estimated amount will appear here once automated withdrawals are enabled for your account.
                </p>
              </div>
            )}
            
            {/* Footer Note */}
            <div className="mt-6 pt-6 border-t border-gray-100 flex items-start gap-3">
               <div className="mt-0.5 text-blue-500 bg-blue-50 p-1.5 rounded-lg shrink-0">
                  <Wallet size={16} />
               </div>
               <p className="text-sm text-gray-500 leading-relaxed font-medium">
                 <span className="text-gray-700 font-bold">Coming Soon:</span> Manual withdrawals are currently disabled. You will be notified when you can manually withdraw your available balance outside of the automated schedule.
               </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default FundsAndPayouts;