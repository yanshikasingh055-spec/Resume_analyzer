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

      // Use relative URL — Vite proxy forwards to localhost:5000
      const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
      });

      let data;
      try {
        data = await response.json();
      } catch {
        throw new Error("Server returned an invalid response. Make sure the backend is running on port 5000.");
      }

      if (!response.ok) {
        throw new Error(data.error || `Server error (${response.status})`);
      }

      setResults(data);
    } catch (err) {
      if (err.message === "Failed to fetch") {
        setError("Cannot connect to backend. Make sure Flask is running: cd backend && python app.py");
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError("");
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">📄</span>
            <span className="logo-text">ResumeMatch</span>
          </div>
          <p className="tagline">Know your match before you apply</p>
        </div>
      </header>

      <main className="main">
        {!results ? (
          <UploadPanel onAnalyze={handleAnalyze} loading={loading} error={error} />
        ) : (
          <ResultsDashboard results={results} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>Built with Python · Flask · spaCy · React</p>
      </footer>
    </div>
  );
}