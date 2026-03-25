import { useMemo } from "react";

export const useCreatorOnboarding = (user, walletStats) => {
  const onboardingState = useMemo(() => {
    if (!user) return { showOnboarding: false, missingSteps: [] };

    const missingSteps = [];

    // Check Profile Completeness
    if (!user.profileImage) {
      missingSteps.push({
        id: "avatar",
        label: "Upload profile picture",
        link: "/creator-dashboard/edit-profile",
      });
    }
    if (!user.coverImage) {
      missingSteps.push({
        id: "cover",
        label: "Add cover photo",
        link: "/creator-dashboard/edit-profile",
      });
    }
    if (!user.bio) {
      missingSteps.push({
        id: "bio",
        label: "Write your bio",
        link: "/creator-dashboard/edit-profile",
      });
    }

    // Check Earnings (New Creator State)
    // If balance is 0 AND no transactions, they are "New"
    const hasEarnings =
      walletStats?.totalEarnings > 0 ||
      walletStats?.transactionCount > 0 ||
      user?.hasEarnings;

    if (!hasEarnings) {
      missingSteps.push({
        id: "first-tip",
        label: "Receive your first tip",
        link: "/creator-dashboard/guide#share",
      });
    }

    // Determine if Onboarding Mode is active
    // We show onboarding if ANY profile field is missing OR if they have 0 earnings
    const showOnboarding = missingSteps.length > 0;

    const firstTipOnly =
      missingSteps.length === 1 && missingSteps[0].id === "first-tip";

    return {
      showOnboarding,
      missingSteps,
      firstTipOnly,
      completionPercentage: Math.round(((4 - missingSteps.length) / 4) * 100),
    };
  }, [user, walletStats]);

  return onboardingState;
};
