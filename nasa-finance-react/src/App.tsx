import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import CitizenPortal from './pages/CitizenPortal';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/citizen-portal" replace />} />
        <Route path="/citizen-portal" element={<CitizenPortal />} />
        {/* More routes will be added here */}
      </Routes>
    </Router>
  );
}

export default App;
