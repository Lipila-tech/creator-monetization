

const PrivacyPolicy = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <main className="flex-grow container mx-auto px-4 py-8 max-w-4xl">
        <div className="bg-white rounded-xl shadow-sm p-8 md:p-12 prose prose-green max-w-none">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Privacy Policy</h1>
          <p className="text-gray-500 mb-8">Last updated: January 2026</p>

          <p className="mb-6">Tipzed Technologies (“Tipzed”, “we”, “our”, “us”) respects your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, store, and protect your data when you use our platform.</p>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">1. Information We Collect</h2>
            <h3 className="font-semibold text-gray-900 mt-4 mb-2">a) Personal Information</h3>
            <ul className="list-disc pl-5 text-gray-700 space-y-1 mb-4">
              <li>Full name or display name</li>
              <li>Email address</li>
              <li>Phone number</li>
              <li>Mobile money or bank account details (for payouts)</li>
            </ul>

            <h3 className="font-semibold text-gray-900 mt-4 mb-2">b) Usage Information</h3>
            <ul className="list-disc pl-5 text-gray-700 space-y-1 mb-4">
              <li>Pages visited</li>
              <li>Transactions made (tips, payouts)</li>
              <li>IP address and device information</li>
            </ul>

            <h3 className="font-semibold text-gray-900 mt-4 mb-2">c) Payment Information</h3>
            <p className="text-gray-700">Payments are processed through licensed third-party providers. We do not store full mobile money PINs or bank login credentials.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">2. How We Use Your Information</h2>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Create and manage your account</li>
              <li>Process tips and payouts</li>
              <li>Prevent fraud and abuse</li>
              <li>Communicate platform updates</li>
              <li>Improve platform performance</li>
            </ul>
            <p className="text-gray-700 mt-2 font-medium">We do not sell your data.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">3. Sharing of Information</h2>
            <p className="text-gray-700 mb-2">We may share limited information with:</p>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Payment processors (to complete transactions)</li>
              <li>Legal authorities if required by law</li>
            </ul>
            <p className="text-gray-700 mt-2">All partners are required to protect your data.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">4. Data Storage & Security</h2>
            <p className="text-gray-700 mb-2">We take reasonable measures to protect your information using:</p>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Secure servers</li>
              <li>Access controls</li>
              <li>Encrypted connections</li>
            </ul>
            <p className="text-gray-700 mt-2">However, no system is 100% secure.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">5. Your Rights</h2>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Access your data</li>
              <li>Correct inaccurate information</li>
              <li>Request account deletion</li>
            </ul>
            <p className="text-gray-700 mt-2">You may contact us to exercise these rights.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">6. Data Retention</h2>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Legal compliance</li>
              <li>Transaction records</li>
              <li>Platform operations</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">7. Changes to This Policy</h2>
            <p className="text-gray-700">We may update this policy occasionally. Significant changes will be communicated on the platform.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">8. Contact Us</h2>
            <p className="text-gray-700">For privacy-related questions, contact support@tipzed.com.</p>
          </section>
        </div>
      </main>

    </div>
  );
};

export default PrivacyPolicy;