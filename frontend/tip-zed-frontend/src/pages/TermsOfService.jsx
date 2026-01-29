import { Link } from 'react-router-dom';

const TermsOfService = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <main className="flex-grow container mx-auto px-4 py-8 max-w-4xl">
        <div className="bg-white rounded-xl shadow-sm p-8 md:p-12 prose prose-green max-w-none">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Terms of Service</h1>
          <p className="text-gray-500 mb-8">Last updated: January 2026</p>

          <p className="mb-6">By using the Tipzed platform, you agree to these Terms of Service.</p>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">1. Platform Overview</h2>
            <p className="text-gray-700">Tipzed is a platform that allows creators to receive tips and support payments from their audience using mobile money and other supported methods.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">2. Eligibility</h2>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>You must be at least 18 years old, or</li>
              <li>Have legal capacity to receive payments</li>
              <li>Creators are responsible for ensuring their content complies with the law.</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">3. Platform Fees</h2>
            <p className="text-gray-700 mb-2">Tipzed charges a 10% platform fee on each transaction. This fee covers:</p>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Payment processing costs</li>
              <li>Weekly payouts</li>
              <li>Platform hosting and maintenance</li>
            </ul>
            <p className="text-gray-700 mt-2">Additional fees may apply for early payouts.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">4. Payouts</h2>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Payouts are processed weekly on Wednesdays</li>
              <li>Creators must provide valid mobile money or bank details</li>
              <li>Failed payouts remain in the creator balance</li>
              <li>Tipzed is not responsible for delays caused by mobile money providers or banks.</li>
            </ul>
          </section>

           <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">5. Early Payouts</h2>
            <p className="text-gray-700">Creators may request payouts before the scheduled payout day. Early payouts attract an additional processing fee, shown before confirmation.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">6. Prohibited Use</h2>
            <p className="text-gray-700 mb-2">You may not use Tipzed to:</p>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Engage in fraud or money laundering</li>
              <li>Collect payments for illegal activities</li>
              <li>Misrepresent your identity</li>
              <li>Abuse or exploit others</li>
            </ul>
            <p className="text-gray-700 mt-2">Violations may result in account suspension or termination.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">7. Account Suspension & Termination</h2>
            <p className="text-gray-700 mb-2">We reserve the right to:</p>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Suspend accounts for suspicious activity</li>
              <li>Withhold payouts during investigations</li>
              <li>Terminate accounts that violate these terms</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">8. Limitation of Liability</h2>
            <p className="text-gray-700 mb-2">Tipzed is not liable for:</p>
            <ul className="list-disc pl-5 text-gray-700 space-y-2">
              <li>Losses due to third-party payment failures</li>
              <li>Creator-fan disputes</li>
              <li>Network outages or service interruptions</li>
            </ul>
            <p className="text-gray-700 mt-2">Use the platform at your own risk.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">9. Changes to Terms</h2>
            <p className="text-gray-700">We may update these Terms from time to time. Continued use of the platform means acceptance of updated terms.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">10. Governing Law</h2>
            <p className="text-gray-700">These Terms are governed by the laws of the Republic of Zambia.</p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-3">11. Contact Information</h2>
            <p className="text-gray-700">For questions regarding these Terms, please contact support@tipzed.com.</p>
          </section>
        </div>
      </main>

    </div>
  );
};

export default TermsOfService;