import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';

// Note: AuthProvider is already wrapping this in main.jsx, so we don't need it here.

function App() {
  return (
    <Router>
      <Routes>
        {/* The Landing Page */}
        <Route path="/" element={<Home />} />

        {/* Auth Pages */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Signup />} />

        {/* 404 Fallback (Optional) */}
        <Route path="*" element={<div className="text-center mt-20">Page Not Found</div>} />
      </Routes>
    </Router>
  )
}

export default App