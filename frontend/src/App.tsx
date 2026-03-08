import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { ThemeProvider } from "./contexts/ThemeContext";
import { LanguageProvider } from "./contexts/LanguageContext";
import { ToastProvider } from "./components/Toast";
import Layout from "./components/layout/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Analytics from "./pages/Analytics";
import Results from "./pages/Results";
import Profile from "./pages/Profile";
import Methodology from "./pages/Methodology";
import TestPage from "./pages/TestPage";
import SimpleTest from "./pages/SimpleTest";
import WigMarketplace from "./pages/WigMarketplace";
import Donation from "./pages/Donation";
import Wellness from "./pages/Wellness";
import YogaSession from "./pages/YogaSession";
import OTPRequest from "./pages/OTPRequest";
import OTPVerify from "./pages/OTPVerify";
import OTPSuccess from "./pages/OTPSuccess";
import StagingAssessment from "./pages/StagingAssessment";
import MedicineReminders from "./pages/MedicineReminders";

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <ThemeProvider>
          <ToastProvider>
            <Layout>
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* OTP Routes */}
                <Route path="/otp-request" element={<OTPRequest />} />
                <Route path="/otp-verify" element={<OTPVerify />} />
                <Route path="/otp-success" element={<OTPSuccess />} />

                {/* Protected Routes */}
                <Route path="/upload" element={<ProtectedRoute><Upload /></ProtectedRoute>} />
                <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
                <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
                <Route path="/results/:id" element={<ProtectedRoute><Results /></ProtectedRoute>} />
                <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
                <Route path="/methodology" element={<ProtectedRoute><Methodology /></ProtectedRoute>} />
                <Route path="/staging" element={<ProtectedRoute><StagingAssessment /></ProtectedRoute>} />
                <Route path="/medicines" element={<ProtectedRoute><MedicineReminders /></ProtectedRoute>} />

                {/* Public Community Routes */}
                <Route path="/wigs" element={<WigMarketplace />} />
                <Route path="/donate" element={<Donation />} />
                <Route path="/wellness" element={<Wellness />} />
                <Route path="/wellness/session/:id" element={<YogaSession />} />

                {/* Test Routes */}
                <Route path="/test" element={<TestPage />} />
                <Route path="/simple" element={<SimpleTest />} />
              </Routes>
            </Layout>
          </ToastProvider>
        </ThemeProvider>
      </AuthProvider>
    </LanguageProvider>
  );
}
