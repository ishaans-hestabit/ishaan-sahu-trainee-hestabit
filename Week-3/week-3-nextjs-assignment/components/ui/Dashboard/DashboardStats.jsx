import StatsCard from "./StatsCard";
import { Wallet,Users,UserPlus,ShoppingCart,
    } from "lucide-react";

export default function DashboardStats() {
  const stats = [
    {
      title: "Today's Money",
      value: "$53,000",
      change: "+55%",
      icon: <Wallet size={18} color="white"/>,
    },
    {
      title: "Today's Users",
      value: "2,300",
      change: "+5%",
      icon: <Users size={18} color="white"/>,
    },
    {
      title: "New Clients",
      value: "+3,052",
      change: "-14%",
      icon: <UserPlus size={18} color="white"/>
    },
    {
      title: "Total Sales",
      value: "$173,000",
      change: "+8%",
      icon: <ShoppingCart size={18} color="white"/>,
    },
  ];

  return (
    <div className="grid grid-cols-1 grid-cols-4 gap-4 p-6">
      { stats.map((stat) => (
        <StatsCard key={stat.title} {...stat} />
      ))}
    </div>
  );
}
