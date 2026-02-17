import { useEffect, useState } from "react";
import { useLocation, Link, useNavigate } from "react-router-dom"; // Added useNavigate
import DashboardLayout from "@/layouts/DashboardLayout";
import { useAuth } from "@/hooks/useAuth";
import { walletService } from "@/services/walletService";
import {
  ArrowUpRight,
  ShieldCheck,
  AlertCircle,
  HelpCircle,
  BookOpen,
  X,
  UserPen,
} from "lucide-react";
import { useCreatorOnboarding } from "@/hooks/useCreatorOnboarding";
import OnboardingChecklist from "@/components/Creator/OnboardingChecklist";
import Overview from "@/components/Creator/Overview";
import Transactions from "@/components/Creator/Transactions";
import EditProfile from "@/components/Creator/EditProfile";
import Guide from "@/components/Creator/Guide";

const CreatorDashboard = () => {
  const { user } = useAuth();
  const { pathname } = useLocation();
  const navigate = useNavigate();

  //VIEW LOGIC
  const isOverview = pathname === "/creator-dashboard";
  const isTransactionsView = pathname === "/creator-dashboard/transactions";
  const isEditProfileView = pathname === "/creator-dashboard/edit-profile";
  const isGuideView = pathname === "/creator-dashboard/guide";

  // Identify if the current view requires data fetching
  const isDataView = isOverview || isTransactionsView;

  const [walletData, setWalletData] = useState(null);
  const [hasWalletData, setHasWalletData] = useState(false);
  const [txnData, setTxnData] = useState(null);
  const [loading, setLoading] = useState(isDataView); // Only start as loading if we need data
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    // GUARD-- If we are on Edit Profile or Guide, do not fetch anything.
    if (!isDataView) {
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Determine correct page for the API
        // If Overview, force page 1. If Transactions, use current state page.
        const apiPage = isTransactionsView ? page : 1;

        const promises = [];

        // OPTIMIZATION: Logic for Wallet Data (Overview Data)
        // We always need it for Overview.
        // For Transactions, we only need it for the Header. If we already have it, don't re-fetch.
        const shouldFetchWalletData = isOverview || (isTransactionsView && hasWalletData);

        if (shouldFetchWalletData) {
           promises.push(walletService.getWalletData()); // Assuming stats don't need pagination
        } else {
           promises.push(Promise.resolve(null)); // Placeholder to keep array index consistent
        }

        // Logic for Transaction Data
        // Always fetch this for both views (Overview gets p1, Transactions gets pN)
        promises.push(walletService.getWalletTxnData(apiPage));

        const [walletRes, txnRes] = await Promise.all(promises);

        // Only update walletData if we actually fetched a new one
        if (walletRes) {
          setWalletData(walletRes);
          setHasWalletData(true);
        }
        setTxnData(txnRes);

      } catch (err) {
        console.error(err);
        setError(
          err?.responseWallet?.data?.message ||
            err?.responseTxn?.data?.message ||
            "Failed to load data."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Dependencies:
    // We re-run if the view mode changes or the page changes.
  }, [page, isOverview, isTransactionsView, isDataView, hasWalletData]);

  const { missingSteps, showOnboarding, completionPercentage } =
    useCreatorOnboarding(user, walletData);


  // --- RENDER HELPERS ---

  // Helper to prevent content jumping: Skeleton Loader
  if (loading && !walletData && isDataView) {
    return (
      <DashboardLayout title={user?.username}>
        <div className="animate-pulse space-y-8">
          <div className="h-8 bg-gray-200 w-1/4 rounded-lg"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="h-32 bg-gray-100 rounded-2xl"></div>
            <div className="h-32 bg-gray-100 rounded-2xl"></div>
            <div className="h-32 bg-gray-100 rounded-2xl"></div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  // Error State (Only for Data Views)
  if (error && isDataView) {
    return (
      <DashboardLayout title={user?.username ?? "Dashboard"}>
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="bg-red-50 border border-red-100 text-red-600 rounded-2xl p-8 max-w-md">
            <AlertCircle size={40} className="mx-auto mb-4" />
            <h2 className="font-black text-lg mb-2">Something went wrong</h2>
            <p className="text-sm font-medium mb-6">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="bg-red-600 text-white px-5 py-2 rounded-xl text-sm font-bold hover:opacity-90"
            >
              Retry
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title={user?.username ?? "Dashboard"}>
      
      {/* HEADER SECTION (Shared by Overview & Transactions) */}
      {isDataView && (
        <div className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">
              {isTransactionsView ? "Transaction History" : "Overview"}
            </h1>
            {/* Guard against null walletData if API partially failed */}
            {walletData && (
              <div className="flex items-center gap-2 mt-1">
                <span className="bg-gray-100 text-gray-500 px-2 py-0.5 rounded text-[10px] font-bold uppercase">
                  {walletData.kycLevel}
                </span>
                {walletData.kycVerified && (
                  <ShieldCheck size={14} className="text-zed-green" />
                )}
              </div>
            )}
          </div>

          <button className="bg-zed-green text-white px-6 py-3 rounded-xl font-bold shadow-lg flex items-center gap-2 hover:scale-105 transition-all text-sm">
            Withdraw Funds <ArrowUpRight size={18} />
          </button>
        </div>
      )}

      {/* EDIT PROFILE HEADER */}
      {isEditProfileView && (
        <div className="bg-white border-b border-gray-200 px-6 py-4 mb-10 top-0 z-30 flex justify-between items-center shadow-sm">
          <h1 className="text-xl font-bold text-gray-900">Edit Profile</h1>
          <button
            onClick={() => navigate("/creator-dashboard")}
            className="text-gray-500 hover:text-gray-900"
          >
            <X size={24} />
          </button>
        </div>
      )}

      {/* ONBOARDING (Show on Dashboard views) */}
      {showOnboarding && !isGuideView && !isEditProfileView && (
        <OnboardingChecklist
          missingSteps={missingSteps}
          completionPercentage={completionPercentage}
        />
      )}

      {/* ERROR MESSAGE (Inline) */}
      {error && (
        <div className="mb-6 rounded-xl border border-red-100 bg-red-50 px-6 py-4 text-sm font-bold text-red-600 flex items-center gap-3">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

      {/* --- CONTENT VIEWS --- */}

      {/* VIEW A: OVERVIEW */}
      {isOverview && <Overview walletData={walletData} />}

      {/* VIEW B: TRANSACTIONS */}
      {/* Note: Transactions view handles its own list display, we just pass data */}
      {(isTransactionsView || isOverview) && (
        <Transactions
          error={error}
          // If we are on Overview, we force "View Mode" behavior (usually simplified list)
          // If on Transactions, it is the full view
          isTransactionsView={isTransactionsView} 
          txnData={txnData}
          setPage={setPage}
          loading={loading}
          walletData={walletData}
          page={page}
        />
      )}

      {/* VIEW C: EDIT PROFILE */}
      {isEditProfileView && <EditProfile user={user} />}

      {/* VIEW D: GUIDE */}
      {isGuideView && <Guide slug={user?.slug} />}


      {/* FLOATING HELP BUTTON */}
      {showOnboarding && (
        <div className="fixed bottom-6 right-6 z-40">
          <button
            onClick={() => setShowHelp(!showHelp)}
            className="bg-zed-green text-white p-4 rounded-full shadow-lg hover:scale-110 transition-transform"
          >
            <HelpCircle size={24} />
          </button>

          {showHelp && (
            <div className="absolute bottom-full right-0 mb-4 w-80 bg-white rounded-2xl shadow-2xl p-6">
              <h3 className="font-bold text-gray-900 mb-4">
                Need help getting started?
              </h3>
              <div className="space-y-3">
                <Link
                  to="/creator-dashboard/guide"
                  className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-xl"
                >
                  <BookOpen size={18} className="text-zed-green" />
                  <span className="font-medium">View Complete Guide</span>
                </Link>
                <Link
                  to="/creator-dashboard/edit-profile"
                  className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-xl"
                >
                  <UserPen size={18} className="text-zed-green" />
                  <span className="font-medium">Complete Your Profile</span>
                </Link>
              </div>
            </div>
          )}
        </div>
      )}
    </DashboardLayout>
  );
};
export default CreatorDashboard;