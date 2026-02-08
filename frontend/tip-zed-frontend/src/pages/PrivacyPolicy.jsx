import { ShieldCheck, Lock, Mail, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";

const PrivacyPolicy = () => {
  const sections = [
    { id: "collection", title: "1. Information We Collect" },
    { id: "usage", title: "2. How We Use Information" },
    { id: "sharing", title: "3. Sharing of Information" },
    { id: "security", title: "4. Data Storage & Security" },
    { id: "rights", title: "5. Your Rights" },
    { id: "retention", title: "6. Data Retention" },
    { id: "changes", title: "7. Changes to This Policy" },
    { id: "contact", title: "8. Contact Us" },
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
            <span className="text-gray-900">Privacy Policy</span>
          </nav>

          <h1 className="text-5xl font-black text-gray-900 tracking-tight mb-4">
            Privacy Policy
          </h1>
          <p className="text-gray-500 font-medium">
            Last updated: <span className="text-zed-green">January 2026</span>
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
                <ShieldCheck className="text-zed-green mb-3" size={24} />
                <p className="text-xs font-bold text-gray-900 leading-relaxed">
                  Your privacy matters. We never sell your personal data.
                </p>
              </div>
            </div>
          </aside>

          {/* Content */}
          <article className="flex-1 max-w-3xl space-y-16">
            <p className="text-lg text-gray-600 leading-relaxed">
              Tipzed Technologies respects your
              privacy and is committed to protecting your personal information.
              This Privacy Policy explains how we collect, use, store, and
              protect your data when you use our platform.
            </p>

            {/* 1 */}
            <section id="collection">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                1. Information We Collect
              </h2>

              <h3 className="text-sm font-black uppercase tracking-widest text-zed-green mb-3">
                a) Personal Information
              </h3>

              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
                {[
                  "Full name or display name",
                  "Email address",
                  "Phone number",
                  "Mobile money or bank details",
                ].map((item) => (
                  <li
                    key={item}
                    className="flex items-center gap-2 text-gray-600 text-sm font-medium bg-gray-50 p-3 rounded-xl border border-gray-100"
                  >
                    <Lock size={14} className="text-gray-300" />
                    {item}
                  </li>
                ))}
              </ul>

              <h3 className="text-sm font-black uppercase tracking-widest text-zed-green mb-3">
                b) Usage Information
              </h3>
              <p className="text-gray-600 text-sm mb-6">
                Pages visited, transactions made, IP address, and device
                information.
              </p>

              <h3 className="text-sm font-black uppercase tracking-widest text-zed-green mb-3">
                c) Payment Information
              </h3>
              <p className="text-gray-600 text-sm">
                Payments are processed through licensed third-party providers.
                We do not store mobile money PINs or bank login credentials.
              </p>
            </section>

            {/* 2 */}
            <section id="usage">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                2. How We Use Your Information
              </h2>

              <ul className="space-y-4">
                {[
                  "Create and manage your account",
                  "Process tips and payouts",
                  "Prevent fraud and abuse",
                  "Communicate platform updates",
                  "Improve platform performance",
                ].map((text) => (
                  <li
                    key={text}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {text}
                  </li>
                ))}
              </ul>

              <p className="mt-6 text-sm font-black uppercase tracking-widest text-zed-green">
                We do not sell your data
              </p>
            </section>

            {/* 3 */}
            <section id="sharing">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                3. Sharing of Information
              </h2>

              <ul className="space-y-4">
                {[
                  "Payment processors for transaction completion",
                  "Legal authorities when required by law",
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

              <p className="text-gray-600 text-sm mt-4">
                All partners are required to protect your data.
              </p>
            </section>

            {/* 4 */}
            <section id="security">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                4. Data Storage & Security
              </h2>

              <p className="text-gray-600 leading-relaxed">
                We use secure servers, access controls, and encrypted
                connections. However, no system is 100% secure.
              </p>
            </section>

            {/* 5 */}
            <section id="rights">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                5. Your Rights
              </h2>

              <ul className="space-y-4">
                {[
                  "Access your data",
                  "Correct inaccurate information",
                  "Request account deletion",
                ].map((right) => (
                  <li
                    key={right}
                    className="flex items-start gap-3 text-gray-700 font-medium"
                  >
                    <span className="mt-2 w-1.5 h-1.5 bg-zed-green rounded-full" />
                    {right}
                  </li>
                ))}
              </ul>
            </section>

            {/* 6 */}
            <section id="retention">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                6. Data Retention
              </h2>

              <p className="text-gray-600">
                Data is retained for legal compliance, transaction records, and
                platform operations.
              </p>
            </section>

            {/* 7 */}
            <section id="changes">
              <h2 className="text-2xl font-black text-gray-900 mb-6 flex items-center gap-3">
                <span className="w-1.5 h-6 bg-zed-green rounded-full" />
                7. Changes to This Policy
              </h2>

              <p className="text-gray-600">
                We may update this policy occasionally. Significant changes will
                be communicated on the platform.
              </p>
            </section>

            {/* 8 */}
            <section id="contact">
              <div className="bg-zed-green rounded-[3rem] p-10 text-white flex flex-col md:flex-row items-center justify-between gap-8">
                <div>
                  <h2 className="text-3xl font-black mb-2">Have questions?</h2>
                  <p className="text-white/80 font-medium">
                    Our privacy team is here to help.
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

export default PrivacyPolicy;
