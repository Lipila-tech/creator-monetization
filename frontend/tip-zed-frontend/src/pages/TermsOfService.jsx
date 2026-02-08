import { Link } from "react-router-dom";
import {
  ChevronRight,
  Mail,
  FileText,
} from "lucide-react";

const TermsOfService = () => {
  const sections = [
    { id: "overview", title: "1. Platform Overview" },
    { id: "eligibility", title: "2. Eligibility" },
    { id: "fees", title: "3. Platform Fees" },
    { id: "payouts", title: "4. Payouts" },
    { id: "early", title: "5. Early Payouts" },
    { id: "prohibited", title: "6. Prohibited Use" },
    { id: "termination", title: "7. Suspension & Termination" },
    { id: "liability", title: "8. Limitation of Liability" },
    { id: "changes", title: "9. Changes to Terms" },
    { id: "law", title: "10. Governing Law" },
    { id: "contact", title: "11. Contact Information" },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-100 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <nav className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-gray-400 mb-6">
            <Link to="/" className="hover:text-zed-green transition-colors">
              Home
            </Link>
            <ChevronRight size={12} />
            <span className="text-gray-900">Terms of Service</span>
          </nav>

          <h1 className="text-5xl font-black text-gray-900 tracking-tight mb-4">
            Terms of Service
          </h1>
          <p className="text-gray-500 font-medium">
            Last updated:{" "}
            <span className="text-zed-green">January 2026</span>
          </p>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-6 py-16">
        <div className="flex flex-col lg:flex-row gap-16">
          {/* Sidebar */}
          <aside className="hidden lg:block w-64">
            <div className="sticky top-28 space-y-4">
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 mb-6">
                Contents
              </p>

              {sections.map((s) => (
                <a
                  key={s.id}
                  href={`#${s.id}`}
                  className="block text-sm font-bold text-gray-500 hover:text-zed-green transition-colors"
                >
                  {s.title}
                </a>
              ))}

              <div className="mt-10 p-6 bg-zed-green/5 rounded-3xl border border-zed-green/10">
                <FileText className="text-zed-green mb-3" size={24} />
                <p className="text-xs font-bold text-gray-900 leading-relaxed">
                  These terms govern your use of the Tipzed platform.
                </p>
              </div>
            </div>
          </aside>

          {/* Content */}
          <article className="flex-1 max-w-3xl space-y-16">
            <p className="text-lg text-gray-600 leading-relaxed">
              By using the Tipzed platform, you agree to these Terms of Service.
              Please read them carefully before using the service.
            </p>

            {/* 1 */}
            <section id="overview">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                1. Platform Overview
              </h2>
              <p className="text-gray-600">
                Tipzed is a platform that allows creators to receive tips and
                support payments from their audience using mobile money and
                other supported payment methods.
              </p>
            </section>

            {/* 2 */}
            <section id="eligibility">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                2. Eligibility
              </h2>

              <ul className="space-y-4">
                {[
                  "You must be at least 18 years old",
                  "Have legal capacity to receive payments",
                  "Ensure your content complies with applicable laws",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {item}
                  </li>
                ))}
              </ul>
            </section>

            {/* 3 */}
            <section id="fees">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                3. Platform Fees
              </h2>

              <p className="text-gray-600 mb-4">
                Tipzed charges a <strong>10% platform fee</strong> on each
                transaction. This fee covers:
              </p>

              <ul className="space-y-4">
                {[
                  "Payment processing costs",
                  "Weekly payouts",
                  "Platform hosting and maintenance",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {item}
                  </li>
                ))}
              </ul>

              <p className="text-gray-600 mt-4 text-sm">
                Additional fees may apply for early payouts.
              </p>
            </section>

            {/* 4 */}
            <section id="payouts">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                4. Payouts
              </h2>

              <ul className="space-y-4">
                {[
                  "Payouts are processed weekly on Wednesdays",
                  "Creators must provide valid payout details",
                  "Failed payouts remain in the creator balance",
                  "Tipzed is not responsible for third-party delays",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {item}
                  </li>
                ))}
              </ul>
            </section>

            {/* 5 */}
            <section id="early">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                5. Early Payouts
              </h2>
              <p className="text-gray-600">
                Creators may request early payouts. An additional processing
                fee applies and will be shown before confirmation.
              </p>
            </section>

            {/* 6 */}
            <section id="prohibited">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                6. Prohibited Use
              </h2>

              <ul className="space-y-4">
                {[
                  "Fraud or money laundering",
                  "Illegal activities",
                  "Misrepresentation of identity",
                  "Abuse or exploitation of others",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {item}
                  </li>
                ))}
              </ul>

              <p className="text-gray-600 mt-4 text-sm">
                Violations may result in suspension or termination.
              </p>
            </section>

            {/* 7 */}
            <section id="termination">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                7. Account Suspension & Termination
              </h2>

              <ul className="space-y-4">
                {[
                  "Suspend accounts for suspicious activity",
                  "Withhold payouts during investigations",
                  "Terminate accounts that violate these terms",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {item}
                  </li>
                ))}
              </ul>
            </section>

            {/* 8 */}
            <section id="liability">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                8. Limitation of Liability
              </h2>

              <ul className="space-y-4">
                {[
                  "Third-party payment failures",
                  "Creator-fan disputes",
                  "Network outages or service interruptions",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {item}
                  </li>
                ))}
              </ul>

              <p className="text-gray-600 mt-4 text-sm">
                Use of the platform is at your own risk.
              </p>
            </section>

            {/* 9 */}
            <section id="changes">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                9. Changes to Terms
              </h2>
              <p className="text-gray-600">
                Continued use of the platform means acceptance of updated
                terms.
              </p>
            </section>

            {/* 10 */}
            <section id="law">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                10. Governing Law
              </h2>
              <p className="text-gray-600">
                These Terms are governed by the laws of the Republic of Zambia.
              </p>
            </section>

            {/* 11 */}
            <section id="contact">
              <div className="bg-zed-green rounded-[3rem] p-10 text-white flex flex-col md:flex-row items-center justify-between gap-8">
                <div>
                  <h2 className="text-3xl font-black mb-2">
                    Need clarification?
                  </h2>
                  <p className="text-white/80 font-medium">
                    Contact our support team.
                  </p>
                </div>

                <a
                  href="mailto:support@tipzed.com"
                  className="flex items-center gap-3 bg-white text-zed-green px-8 py-4 rounded-2xl font-black hover:scale-105 transition-transform"
                >
                  <Mail size={20} />
                  Contact Support
                </a>
              </div>
            </section>
          </article>
        </div>
      </main>
    </div>
  );
};

export default TermsOfService;
