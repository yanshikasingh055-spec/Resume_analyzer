# 📄 ResumeMatch – AI-Powered Resume Analyzer

> Know your match before you apply. Upload your resume and a job description — get a real-time match score, keyword gap analysis, and actionable improvement tips.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![spaCy](https://img.shields.io/badge/spaCy-NLP-09a3d5)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What it does

Most job seekers apply without knowing if their resume even passes ATS (Applicant Tracking System) filters. ResumeMatch fixes that:

- **Match Score (0–100)** – TF-IDF cosine similarity between your resume and the job description
- **Keyword Gap Analysis** – Shows which required skills/tools are missing from your resume
- **Matched Keywords** – Confirms what you already have right
- **Actionable Suggestions** – Specific, prioritized tips to improve your score

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, plain CSS |
| Backend | Python, Flask, Flask-CORS |
| NLP | spaCy (en_core_web_md), TF-IDF |
| PDF Parsing | PyPDF2 |
| Scoring | scikit-learn cosine similarity |

---

## Getting started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/resume-analyzer.git
cd resume-analyzer
```

### 2. Set up the backend
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_md
python app.py
```
The API will run at `http://localhost:5000`

### 3. Set up the frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000`

---

## Project structure

```
resume-analyzer/
├── backend/
│   ├── app.py          # Flask API routes
│   ├── parser.py       # PDF text extraction
│   ├── extractor.py    # spaCy keyword extraction
│   ├── scorer.py       # TF-IDF match scoring + suggestions
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── UploadPanel.jsx     # File upload + JD input
│   │       ├── ResultsDashboard.jsx
│   │       ├── ScoreCard.jsx       # Animated match score
│   │       ├── KeywordGap.jsx      # Missing/matched keywords
│   │       └── Suggestions.jsx     # Improvement tips
│   └── package.json
└── README.md
```

---

## API reference

### `POST /analyze`

**Request** (multipart/form-data):
| Field | Type | Description |
|---|---|---|
| `resume` | File (PDF) | Candidate's resume |
| `job_description` | String | Full job description text |

**Response**:
```json
{
  "match_score": 72.4,
  "matched_keywords": ["python", "flask", "machine learning"],
  "missing_keywords": ["docker", "kubernetes", "aws"],
  "suggestions": ["Add these missing keywords...", "Quantify achievements..."],
  "resume_keyword_count": 18,
  "jd_keyword_count": 24
}
```

---

## How the scoring works

1. **Text extraction** – PyPDF2 pulls raw text from the resume PDF
2. **Keyword extraction** – spaCy NER + a curated tech skills dictionary identify relevant terms
3. **TF-IDF vectorization** – Both texts are converted to TF-IDF vectors (bigrams, 5000 features)
4. **Cosine similarity** – The angle between vectors gives the match score (0–1, scaled to 0–100)
5. **Gap analysis** – Set difference between JD keywords and resume keywords

---

## Future improvements

- [ ] Support for DOCX resume files
- [ ] Multiple job description comparison
- [ ] Sentence-level suggestions (highlight which bullet points to rewrite)
- [ ] Export results as PDF report
- [ ] User accounts to save and track multiple analyses

---

## License

MIT — free to use, fork, and build on.

---

Built by **Yanshika Singh** · [LinkedIn](https://linkedin.com/in/yanshika-singh05)
