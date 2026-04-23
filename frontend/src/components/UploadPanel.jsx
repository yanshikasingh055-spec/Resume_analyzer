import { useState, useRef } from "react";

export default function UploadPanel({ onAnalyze, loading, error }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type === "application/pdf") {
      setResumeFile(file);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) setResumeFile(file);
  };

  const handleSubmit = () => {
    if (!resumeFile || !jobDescription.trim()) return;
    onAnalyze(resumeFile, jobDescription);
  };

  const isReady = resumeFile && jobDescription.trim().length > 50;

  return (
    <div className="upload-panel">
      <div className="panel-intro">
        <h1>Analyze your resume match</h1>
        <p>
          Upload your resume and paste a job description. We'll score your
          match, highlight gaps, and tell you exactly what to improve.
        </p>
      </div>

      <div className="upload-grid">
        {/* Resume Upload */}
        <div className="upload-section">
          <label className="section-label">Your resume</label>
          <div
            className={`drop-zone ${dragOver ? "drag-over" : ""} ${resumeFile ? "has-file" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            <input
              type="file"
              accept=".pdf"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            {resumeFile ? (
              <div className="file-selected">
                <span className="file-icon">✓</span>
                <span className="file-name">{resumeFile.name}</span>
                <span className="file-size">
                  {(resumeFile.size / 1024).toFixed(0)} KB
                </span>
              </div>
            ) : (
              <div className="drop-prompt">
                <span className="drop-icon">📎</span>
                <span className="drop-text">Drop your PDF here</span>
                <span className="drop-sub">or click to browse</span>
              </div>
            )}
          </div>
        </div>

        {/* Job Description */}
        <div className="upload-section">
          <label className="section-label">
            Job description
            <span className="char-count">
              {jobDescription.length} characters
            </span>
          </label>
          <textarea
            className="jd-textarea"
            placeholder="Paste the full job description here. Include the responsibilities, requirements, and preferred qualifications sections for best results..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={10}
          />
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <span>⚠️</span> {error}
        </div>
      )}

      <div className="submit-row">
        <button
          className={`analyze-btn ${isReady && !loading ? "ready" : "disabled"}`}
          onClick={handleSubmit}
          disabled={!isReady || loading}
        >
          {loading ? (
            <span className="btn-loading">
              <span className="spinner" /> Analyzing your resume...
            </span>
          ) : (
            "Analyze match →"
          )}
        </button>
        {!isReady && !loading && (
          <p className="hint">
            {!resumeFile
              ? "Upload a PDF resume to get started"
              : "Add a longer job description (at least 50 characters)"}
          </p>
        )}
      </div>
    </div>
  );
}
