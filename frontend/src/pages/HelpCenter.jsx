import { useState } from "react";
import { Search, HelpCircle, CreditCard, Users, MessageSquare } from "lucide-react";
import { motion as Motion } from "motion/react";
import { Link } from "react-router-dom";

const HelpCenter = () => {
  const [searchQuery, setSearchQuery] = useState("");

  const categories = [
    {
      title: "Getting Started",
      icon: <HelpCircle className="text-zed-green" size={24} />,
      articles: [
        { id: "what-is-tipzed", title: "What is TipZed?", content: "TipZed is a Zambian-centric platform designed for creators to receive financial support from their fans. Fans can tip creators directly using Mobile Money (Airtel, MTN, Zamtel)." },
        { id: "share-page", title: "How do I let my fans know about my page?", content: "After creating your page, go to your dashboard and copy your support link. You can then share this link with your fans on social media, in your bio, or via direct messages." },
        { id: "one-time-support", title: "How does one-time support work?", content: "One-time support (clinking a glass) is a direct donation from a fan to a creator. The fan selects an amount, pays via Mobile Money, and the funds are added to the creator's balance instantly." },
      ]
    },
    {
      title: "For Creators",
      icon: <Users className="text-zed-orange" size={24} />,
      articles: [
        { id: "withdrawals", title: "How do I withdraw my earnings?", content: "You can withdraw your earnings directly to your Mobile Money account. Go to your dashboard, click 'Withdraw', and follow the prompts. Fees are kept minimal to ensure you keep more of what you earn." },
        { id: "memberships", title: "Setting up memberships", content: "Memberships allow you to receive recurring monthly support from your most loyal fans in exchange for exclusive content or perks." },
      ]
    },
    {
      title: "Payments & Security",
      icon: <CreditCard className="text-zed-black" size={24} />,
      articles: [
        { id: "is-it-secure", title: "Is TipZed secure?", content: "Yes. We use industry-standard encryption and partner with regulated Zambian payment processors to ensure your transactions are safe." },
        { id: "transaction-fees", title: "What are the transaction fees?", content: "We charge a small percentage on each transaction to cover payment processing and platform maintenance. There are no hidden monthly fees for creators." },
      ]
    }
  ];

  const filteredCategories = categories.map(cat => ({
    ...cat,
    articles: cat.articles.filter(art => 
      art.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      art.content.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter(cat => cat.articles.length > 0);

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Hero Section */}
      <section className="bg-zed-black text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <Motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-black mb-6"
          >
            How can we help?
          </Motion.h1>
          <div className="relative max-w-xl mx-auto">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search articles..."
              className="w-full bg-white text-gray-900 pl-12 pr-4 py-4 rounded-2xl focus:ring-2 focus:ring-zed-green outline-none"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-4xl mx-auto px-4 mt-12 space-y-12">
        {filteredCategories.length > 0 ? (
          filteredCategories.map((category, idx) => (
            <div key={idx}>
              <div className="flex items-center gap-3 mb-6">
                {category.icon}
                <h2 className="text-2xl font-black text-gray-900">{category.title}</h2>
              </div>
              <div className="grid gap-4">
                {category.articles.map((article) => (
                  <Motion.div
                    key={article.id}
                    whileHover={{ scale: 1.01 }}
                    className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm transition-all"
                  >
                    <h3 className="text-lg font-bold text-gray-900 mb-2">{article.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{article.content}</p>
                  </Motion.div>
                ))}
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">No articles found for "{searchQuery}"</p>
          </div>
        )}

        {/* Contact CTA */}
        <div className="bg-zed-green/5 rounded-[2.5rem] p-8 md:p-12 text-center border-2 border-zed-green/10">
          <MessageSquare className="mx-auto text-zed-green mb-4" size={40} />
          <h2 className="text-2xl font-black text-gray-900 mb-4">Still have questions?</h2>
          <p className="text-gray-600 mb-8 max-w-lg mx-auto">
            Our team is here to support you in your creative journey. Reach out to us directly.
          </p>
          <Link
            to="/contact"
            className="inline-flex items-center gap-2 bg-zed-green text-white px-8 py-4 rounded-2xl font-black shadow-lg shadow-green-100 hover:bg-green-700 transition-all"
          >
            Contact Support
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HelpCenter;

