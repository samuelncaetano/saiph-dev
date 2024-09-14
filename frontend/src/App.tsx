import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AuthScreenWithAPI from "./AuthScreenWithAPI";
import BookDashboard from "./BookDashboard";
import { Toaster } from "./components/ui/toaster";

export function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthScreenWithAPI />} />
        <Route path="/dashboard" element={<BookDashboard />} />
      </Routes>
      <Toaster />
    </Router>
  );
}
