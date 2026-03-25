import {
  DollarSign,
  ArrowUpRight,
} from "lucide-react";

const Overview = ({ walletData }) => {
  const statCards = [
    {
      label: "Balance",
      val: walletData?.balance,
      icon: DollarSign,
      color: "text-zed-green",
      bg: "bg-green-50",
    },
    {
      label: "Outgoing",
      val: walletData?.totalOutgoing,
      icon: ArrowUpRight,
      color: "text-orange-600",
      bg: "bg-orange-50",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols gap-12 mb-10">
      {statCards.map((stat, i) => (
        <div
          key={i}
          className="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm"
        >
          <div
            className={`${stat.bg} ${stat.color} w-10 h-10 flex items-center justify-center rounded-xl mb-4`}
          >
            <stat.icon size={20} />
          </div>
          <p className="text-xs font-bold text-gray-400 uppercase">
            {stat.label}
          </p>
          <h3 className="text-2xl font-black text-gray-900">
            {walletData?.currency} {Number(stat.val).toLocaleString()}
          </h3>
        </div>
      ))}
    </div>
  );
};

export default Overview;
