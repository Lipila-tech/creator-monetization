import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import TermsOfService from "./pages/TermsOfService";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import Footer from "./components/Common/Footer";
import Header from "./components/Common/Header";
import CreatorDashboard from "./pages/CreatorDashboard";
import ProtectedRoute from "./components/Auth/ProtectedRoute";
import CreatorCatalog from "./pages/CreatorCatalog";
import CreatorProfile from "./pages/CreatorProfile";
import NotFound from "./pages/NotFound";
import { menuItems } from "@/utils/creatorMenuItems";

function App() {
  return (
    <Router>
      {/* flex will force footer at the bottom of the page */}
      <div className="flex flex-col min-h-screen">
        {/* Header will appear at the top of all pages */}
        <Header />
        {/* flex grow will allow page content to fill available space */}
        <div className="flex-grow">
          <Routes>
            {/* The Landing Page */}
            <Route path="/" element={<Home />} />

            {/* Public Facing Pages */}
            <Route path="/:slug" element={<CreatorProfile />} />
            <Route path="/creator-catalog" element={<CreatorCatalog />} />

            {/* Auth Pages */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Signup />} />

            {/* Legal Pages */}
            <Route path="/terms-of-service" element={<TermsOfService />} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />

            {/* Creator Pages*/}
            {menuItems.map((item, key) => (
              <Route
                key={key}
                path={item.path}
                element={
                  <ProtectedRoute>
                    <CreatorDashboard />
                  </ProtectedRoute>
                }
              />
            ))}

            {/* 404 Fallback (Optional) */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
        {/* Footer will appear at the bottom of all pages */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;
