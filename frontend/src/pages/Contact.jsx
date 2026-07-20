import { Mail, MessageSquare, Send } from "lucide-react";
import { motion as Motion } from "motion/react";

const Contact = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <Motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100"
        >
          <div className="bg-zed-black p-8 text-white text-center">
            <h1 className="text-3xl font-black mb-2">Contact Us</h1>
            <p className="text-gray-400">We'd love to hear from you!</p>
          </div>
          
          <div className="p-8 md:p-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <Mail className="text-zed-green" size={24} />
                  Email Us
                </h2>
                <p className="text-gray-600 mb-4">
                  For support, inquiries, or partnerships, reach out to us at:
                </p>
                <a 
                  href="mailto:tipzed2@gmail.com" 
                  className="text-2xl font-black text-zed-black hover:text-zed-green transition-colors break-all"
                >
                  tipzed2@gmail.com
                </a>
              </div>

              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <MessageSquare className="text-zed-green" size={24} />
                  Feedback
                </h2>
                <p className="text-gray-600 mb-6">
                  Are you a creator or a supporter? We value your suggestions to make TipZed better.
                </p>
                <div className="bg-gray-50 rounded-2xl p-6 border border-gray-100">
                  <p className="text-sm text-gray-500 italic">
                    "Your feedback helps us build the best platform for Zambian creators."
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-12 pt-12 border-t border-gray-100 text-center">
              <p className="text-gray-500 text-sm">
                TipZed is built for the community. Every message is read and appreciated.
              </p>
            </div>
          </div>
        </Motion.div>
      </div>
    </div>
  );
};

export default Contact;

