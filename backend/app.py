import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from pdf_parser import extract_text_from_pdf
from extractor import extract_keywords, extract_section_keywords
from scorer import (compute_weighted_score, compute_role_fit,
                    get_matched_keywords, get_missing_keywords,
                    generate_smart_feedback)

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume Analyzer API is running!"})

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume file uploaded"}), 400

        job_description = request.form.get("job_description", "").strip()
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400

        resume_file = request.files["resume"]
        if not resume_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Only PDF files are supported"}), 400

        resume_text = extract_text_from_pdf(resume_file)
        print("=== RESUME TEXT SAMPLE ===")
        print(repr(resume_text[:500]))
        print("=== END SAMPLE ===")
        if not resume_text:
            return jsonify({"error": "Could not extract text from PDF. Is it a scanned image?"}), 400

        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)

        try:
            resume_sections = extract_section_keywords(resume_text)
        except Exception:
            resume_sections = {"other": resume_keywords}

        try:
            match_score, breakdown = compute_weighted_score(
                resume_sections, jd_keywords, resume_text, job_description
            )
        except Exception:
            matched_fallback = get_matched_keywords(resume_keywords, jd_keywords)
            match_score = round(len(matched_fallback) / max(len(jd_keywords), 1) * 100, 1)
            breakdown = {"skills": match_score, "projects": match_score,
                         "tools": match_score, "experience": match_score}

        matched = get_matched_keywords(resume_keywords, jd_keywords)
        missing = get_missing_keywords(resume_keywords, jd_keywords)

        try:
            role_fit = compute_role_fit(resume_keywords)
        except Exception:
            role_fit = {"role_scores": {}, "best_fit_roles": [], "top_score": 0}

        try:
            feedback = generate_smart_feedback(missing, match_score, role_fit, breakdown)
        except Exception:
            feedback = [{"type": "info", "text": "Analysis complete."}]

        return jsonify({
            "match_score": match_score,
            "matched_keywords": sorted(list(matched)),
            "missing_keywords": missing,
            "feedback": feedback,
            "breakdown": breakdown,
            "role_fit": role_fit,
            "resume_keyword_count": len(resume_keywords),
            "jd_keyword_count": len(jd_keywords),
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)