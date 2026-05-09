import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultsDashboard from "./components/ResultsDashboard";
import "./App.css";

export default function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async (resumeFile, jobDescription) => {
    setLoading(true);
    setError("");
    setResults(null);
    try {
      const formData = new FormData();
      formData.append("resume", resumeFile);
      formData.append("job_description", jobDescription);
      const response = await fetch("/analyze", { method: "POST", body: formData });
      let data;
      try { data = await response.json(); }
      catch { throw new Error("Server returned an invalid response."); }
      if (!response.ok) throw new Error(data.error || `Server error (${response.status})`);
      setResults(data);
    } catch (err) {
      setError(err.message === "Failed to fetch"
        ? "Cannot connect to backend. Make sure Flask is running."
        : err.message);
    } finally { setLoading(false); }
  };

  return (
    <div className="app">
      {!results ? (
        <>
          <nav className="nav">
            <div className="nav-logo">
              <div className="nav-logo-icon">📄</div>
              <span className="nav-logo-text">ResumeMatch</span>
            </div>
            <span className="nav-pill">ATS Resume Analyzer</span>
          </nav>
          <main className="main">
            <UploadPanel onAnalyze={handleAnalyze} loading={loading} error={error} />
          </main>
          <footer className="footer">
            <p>Built with Python · Flask · spaCy · React</p>
          </footer>
        </>
      ) : (
        <ResultsDashboard results={results} onReset={() => { setResults(null); setError(""); }} />
      )}
    </div>
  );
}