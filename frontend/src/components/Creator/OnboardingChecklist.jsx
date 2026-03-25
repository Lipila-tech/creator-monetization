import { ChevronRight, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";

const OnboardingChecklist = ({
  missingSteps,
  firstTipOnly,
  completionPercentage,
}) => {
  if (missingSteps.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-zed-green/20 shadow-sm overflow-hidden mb-8 w-full max-w-4xl mx-auto">
      {/* Header - Responsive */}
      <div className="bg-gradient-to-r from-zed-green/10 to-transparent p-4 md:p-6 border-b border-zed-green/10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle size={20} className="text-zed-green flex-shrink-0" />
              <h2 className="text-lg font-bold text-gray-900">
                Complete your profile setup
              </h2>
            </div>
            <p className="text-gray-600 text-sm">
              Creators with complete profiles earn 3x more tips!
            </p>
          </div>

          {/* Progress and CTA */}
          <div className="flex items-center gap-4">
            <span className="font-bold text-zed-green text-xl">
              {completionPercentage}%
            </span>
            <Link
              to={`/creator-dashboard/guide${firstTipOnly ? "#share" : ""}`}
              className="text-sm font-bold text-zed-green hover:text-zed-green-dark underline"
            >
              {firstTipOnly ? "Receive your first tip" : "View Guide"}
            </Link>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-zed-green h-2 rounded-full transition-all duration-500"
            style={{ width: `${completionPercentage}%` }}
          />
        </div>
      </div>

      {/* Action Items*/}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 p-4">
        {missingSteps.map((step) => (
          <Link
            key={step.id}
            to={step.link}
            className="flex items-center justify-between p-3 md:p-4 rounded-xl hover:bg-gray-50 transition-colors group border border-gray-100"
          >
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full border-2 border-gray-300 flex items-center justify-center">
                <span className="text-xs font-bold text-gray-400">
                  {missingSteps.indexOf(step) + 1}
                </span>
              </div>
              <span className="text-gray-700 font-medium text-sm md:text-base">
                {step.label}
              </span>
            </div>
            <ChevronRight
              size={18}
              className="text-gray-300 group-hover:text-zed-green"
            />
          </Link>
        ))}
      </div>
    </div>
  );
};

export default OnboardingChecklist;
