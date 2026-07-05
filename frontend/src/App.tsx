import { Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Analytics } from "./pages/Analytics";
import { CandidateDetails } from "./pages/CandidateDetails";
import { Candidates } from "./pages/Candidates";
import { Dashboard } from "./pages/Dashboard";
import { Ranking } from "./pages/Ranking";
import { Settings } from "./pages/Settings";
import { UploadJob } from "./pages/UploadJob";
import { UploadResumes } from "./pages/UploadResumes";
import "./index.css";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload-job" element={<UploadJob />} />
        <Route path="/upload-resumes" element={<UploadResumes />} />
        <Route path="/candidates" element={<Candidates />} />
        <Route path="/candidate/:id" element={<CandidateDetails />} />
        <Route path="/ranking" element={<Ranking />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;
