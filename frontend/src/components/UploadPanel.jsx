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
    if (file && file.type === "application/pdf") setResumeFile(file);
  };

  const isReady = resumeFile && jobDescription.trim().length > 50;

  return (
    <div className="upload-panel">
      <div className="hero">
        <h1 className="hero-title">Know your match before you apply</h1>
        <p className="hero-sub">
          Upload your resume and paste a job description. We'll score your match,
          find missing keywords, and tell you exactly what to improve.
        </p>
        <div className="steps">
          {["Upload resume", "Paste job description", "Get your score", "Fix the gaps"].map((s, i) => (
            <div className="step" key={i}>
              <span className="step-num">{i + 1}</span>
              <span className="step-text">{s}</span>
              {i < 3 && <span className="step-sep">→</span>}
            </div>
          ))}
        </div>
      </div>

      <div className="upload-grid">
        <div className="upload-card">
          <div className="card-label">
            <span className="label-icon">📤</span> Your resume
          </div>
          <div
            className={`drop-zone ${dragOver ? "drag-over" : ""} ${resumeFile ? "has-file" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            <input type="file" accept=".pdf" ref={fileInputRef}
              onChange={(e) => { if (e.target.files[0]) setResumeFile(e.target.files[0]); }}
              style={{ display: "none" }} />
            {resumeFile ? (
              <div className="file-ready">
                <div className="file-ready-icon">✓</div>
                <div>
                  <div className="file-ready-name">{resumeFile.name}</div>
                  <div className="file-ready-size">{(resumeFile.size / 1024).toFixed(0)} KB · PDF ready</div>
                </div>
                <button className="file-change" onClick={(e) => { e.stopPropagation(); setResumeFile(null); }}>
                  Change
                </button>
              </div>
            ) : (
              <div className="drop-prompt">
                <div className="drop-icon-wrap">📎</div>
                <div className="drop-title">Drop your PDF here</div>
                <div className="drop-sub">or click to browse</div>
                <div className="drop-btn">Browse file</div>
              </div>
            )}
          </div>
          <div className="card-tip">Supports PDF format only</div>
        </div>

        <div className="upload-card">
          <div className="card-label">
            <span className="label-icon">💼</span> Job description
            <span className="char-pill">{jobDescription.length} chars</span>
          </div>
          <textarea
            className="jd-textarea"
            placeholder="Paste the full job description here — include responsibilities, requirements, and preferred qualifications for best results..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={10}
          />
          <div className="card-tip">
            {jobDescription.length < 50 && jobDescription.length > 0
              ? "Add more text for accurate results (min 50 characters)"
              : jobDescription.length >= 50
              ? "✓ Good length for analysis"
              : "Tip: more detail = better keyword matching"}
          </div>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <span>⚠️</span> {error}
        </div>
      )}

      <div className="submit-row">
        <button
          className={`analyze-btn ${isReady && !loading ? "ready" : "muted"}`}
          onClick={() => { if (isReady && !loading) onAnalyze(resumeFile, jobDescription); }}
          disabled={!isReady || loading}
        >
          {loading ? (
            <span className="btn-inner"><span className="spinner" /> Analyzing your resume...</span>
          ) : (
            <span className="btn-inner">🔍 Analyze match</span>
          )}
        </button>
        {!isReady && !loading && (
          <p className="submit-hint">
            {!resumeFile ? "Upload a PDF resume to get started"
              : "Paste a job description (at least 50 characters)"}
          </p>
        )}
      </div>
    </div>
  );
}