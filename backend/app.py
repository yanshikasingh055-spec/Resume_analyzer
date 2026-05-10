import os
import traceback
from flask import Flask, request, jsonify, make_response

from pdf_parser import extract_text_from_pdf
from extractor import extract_keywords, extract_section_keywords
from scorer import (compute_weighted_score, compute_role_fit,
                    get_matched_keywords, get_missing_keywords,
                    generate_smart_feedback)

app = Flask(__name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/", methods=["GET"])
def home():
    response = make_response(jsonify({"message": "Resume Analyzer API is running!"}))
    return add_cors_headers(response)

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        response = make_response()
        return add_cors_headers(response), 200

    try:
        if "resume" not in request.files:
            response = make_response(jsonify({"error": "No resume file uploaded"}), 400)
            return add_cors_headers(response)

        job_description = request.form.get("job_description", "").strip()
        if not job_description:
            response = make_response(jsonify({"error": "Job description is required"}), 400)
            return add_cors_headers(response)

        resume_file = request.files["resume"]
        if not resume_file.filename.lower().endswith(".pdf"):
            response = make_response(jsonify({"error": "Only PDF files are supported"}), 400)
            return add_cors_headers(response)

        resume_text = extract_text_from_pdf(resume_file)
        print("=== RESUME TEXT SAMPLE ===")
        print(repr(resume_text[:500]))
        print("=== END SAMPLE ===")
        if not resume_text:
            response = make_response(jsonify({"error": "Could not extract text from PDF. Is it a scanned image?"}), 400)
            return add_cors_headers(response)

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

        response = make_response(jsonify({
            "match_score": match_score,
            "matched_keywords": sorted(list(matched)),
            "missing_keywords": missing,
            "feedback": feedback,
            "breakdown": breakdown,
            "role_fit": role_fit,
            "resume_keyword_count": len(resume_keywords),
            "jd_keyword_count": len(jd_keywords),
        }))
        return add_cors_headers(response)

    except Exception as e:
        traceback.print_exc()
        response = make_response(jsonify({"error": f"Analysis failed: {str(e)}"}), 500)
        return add_cors_headers(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)