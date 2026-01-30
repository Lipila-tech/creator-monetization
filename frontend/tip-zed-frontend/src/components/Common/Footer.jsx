import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          
          {/* Copyright */}
          <div className="text-gray-500 text-sm">
            © {currentYear} TipZed Technologies. Made with ❤️ in Zambia.
          </div>

          {/* Legal Links */}
          <div className="flex space-x-6">
            <Link 
              to="/terms-of-service" 
              className="text-gray-500 hover:text-zed-green text-sm transition-colors"
            >
              Terms of Service
            </Link>
            <Link 
              to="/privacy-policy" 
              className="text-gray-500 hover:text-zed-green text-sm transition-colors"
            >
              Privacy Policy
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;