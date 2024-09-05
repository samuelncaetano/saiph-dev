import { Route, BrowserRouter as Router, Routes } from "react-router-dom";

import AuthScreenWithAPI from "./AuthScreenWithAPI";
import BookDashboard from "./BookDashboard";

export function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthScreenWithAPI />} />
        <Route path="/dashboard" element={<BookDashboard />} />

      </Routes>
    </Router>
  );
}
