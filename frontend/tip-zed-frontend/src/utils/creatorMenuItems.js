import {
  ArrowRightLeft,
  Banknote,
  LayoutDashboard,
  PiggyBank,
  UserCog,
  UserPen,
} from "lucide-react";

export const menuItems = [
  {
    icon: LayoutDashboard,
    label: "Overview",
    path: "/creator-dashboard",
  },
  {
    icon: ArrowRightLeft,
    label: "Transactions",
    path: "/creator-dashboard/transactions",
  },
  {
    icon: Banknote,
    label: "Funds & Payouts",
    path: "/creator-dashboard/funds-and-payouts",
  },
  {
    icon: PiggyBank,
    label: "Payout Account",
    path: "/creator-dashboard/payout-account",
  },
  {
    icon: UserPen,
    label: "Edit Profile",
    path: "/creator-dashboard/edit-profile",
  },
  {
    icon: UserCog,
    label: "Guide",
    path: "/creator-dashboard/guide",
  },
];
