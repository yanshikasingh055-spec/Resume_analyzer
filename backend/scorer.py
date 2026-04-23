from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from extractor import SEMANTIC_SYNONYMS

_CANONICAL_TO_SYNONYMS: dict = {}
for phrase, canonical in SEMANTIC_SYNONYMS.items():
    _CANONICAL_TO_SYNONYMS.setdefault(canonical, []).append(phrase)

# ── Role profiles for Role Fit detection ─────────────────────────────────────
ROLE_PROFILES = {
    "Machine Learning Engineer": {
        "keywords": {"machine learning", "deep learning", "python", "tensorflow", "pytorch",
                     "scikit-learn", "computer vision", "natural language processing",
                     "neural network", "model deployment", "feature engineering"},
        "weight": 1.0,
    },
    "Data Scientist": {
        "keywords": {"data science", "data analysis", "python", "machine learning", "pandas",
                     "numpy", "matplotlib", "scikit-learn", "regression", "classification",
                     "data visualization", "sql"},
        "weight": 1.0,
    },
    "Full Stack Developer": {
        "keywords": {"react", "node", "javascript", "html", "css", "rest api", "flask",
                     "django", "database", "git", "python"},
        "weight": 1.0,
    },
    "Backend Developer": {
        "keywords": {"python", "flask", "django", "fastapi", "rest api", "database",
                     "mysql", "postgresql", "mongodb", "git", "docker", "aws"},
        "weight": 1.0,
    },
    "Frontend Developer": {
        "keywords": {"react", "javascript", "typescript", "html", "css", "tailwind",
                     "responsive design", "accessibility", "angular", "vue"},
        "weight": 1.0,
    },
    "DevOps Engineer": {
        "keywords": {"docker", "kubernetes", "ci/cd", "aws", "azure", "gcp", "linux",
                     "git", "jenkins", "terraform", "monitoring", "bash"},
        "weight": 1.0,
    },
    "Data Engineer": {
        "keywords": {"python", "sql", "etl", "data pipeline", "big data", "spark",
                     "airflow", "aws", "postgresql", "mongodb"},
        "weight": 1.0,
    },
    "AI/Computer Vision Engineer": {
        "keywords": {"computer vision", "deep learning", "opencv", "yolo", "tensorflow",
                     "pytorch", "object detection", "cnn", "image classification", "python"},
        "weight": 1.0,
    },
}

# Skill category groups — for section scoring
SKILL_GROUPS = {
    "ml_ai": {"machine learning", "deep learning", "computer vision", "natural language processing",
               "neural network", "cnn", "rnn", "lstm", "transformer", "bert", "gpt",
               "reinforcement learning", "transfer learning", "generative ai", "llm"},
    "frameworks": {"tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "opencv",
                   "huggingface", "yolo", "detectron"},
    "languages": {"python", "javascript", "typescript", "java", "c++", "sql", "r", "scala"},
    "web": {"react", "flask", "django", "node", "express", "fastapi", "angular", "vue",
            "rest api", "graphql", "tailwind", "bootstrap"},
    "data": {"pandas", "numpy", "matplotlib", "seaborn", "data analysis", "data science",
             "data visualization", "etl", "big data"},
    "cloud_devops": {"aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "git",
                     "github", "linux", "jenkins"},
    "databases": {"mysql", "postgresql", "mongodb", "redis", "sqlite", "database",
                  "firebase", "elasticsearch"},
}

def split_jd_keywords(jd_keywords):
    return {
        "skills": jd_keywords & (
            SKILL_GROUPS["ml_ai"] |
            SKILL_GROUPS["data"] |
            SKILL_GROUPS["web"]
        ),
        "tools": jd_keywords & (
            SKILL_GROUPS["frameworks"] |
            SKILL_GROUPS["languages"] |
            SKILL_GROUPS["cloud_devops"]
        ),
        "experience": jd_keywords,   # keep full
        "projects": jd_keywords      # keep full
    }


def _semantic_match(resume_kws: set, jd_kws: set) -> set:
    resume_canonicals = set(resume_kws)
    for kw in resume_kws:
        if kw in SEMANTIC_SYNONYMS:
            resume_canonicals.add(SEMANTIC_SYNONYMS[kw])
        if kw in _CANONICAL_TO_SYNONYMS:
            resume_canonicals.update(_CANONICAL_TO_SYNONYMS[kw])

    semantically_matched = set()
    for jd_kw in jd_kws:
        if jd_kw in resume_canonicals:
            semantically_matched.add(jd_kw)
        elif jd_kw in _CANONICAL_TO_SYNONYMS:
            if any(syn in resume_kws or syn in resume_canonicals
                   for syn in _CANONICAL_TO_SYNONYMS[jd_kw]):
                semantically_matched.add(jd_kw)
        elif jd_kw in SEMANTIC_SYNONYMS:
            if SEMANTIC_SYNONYMS[jd_kw] in resume_kws:
                semantically_matched.add(jd_kw)
    return semantically_matched


def get_matched_keywords(resume_keywords, jd_keywords):
    exact = resume_keywords & jd_keywords
    semantic = _semantic_match(resume_keywords, jd_keywords)
    return exact | semantic


def get_missing_keywords(resume_keywords, jd_keywords):
    matched = get_matched_keywords(resume_keywords, jd_keywords)
    missing = jd_keywords - matched
    return sorted(list(missing), key=lambda x: (-len(x.split()), x))


def compute_weighted_score(resume_sections: dict, jd_sections: dict, resume_text: str, job_description: str):
    """
    Section-weighted scoring:
      Skills section     → 40%
      Projects section   → 30%
      Tools/frameworks   → 20%  (from all sections, filtered by SKILL_GROUPS frameworks)
      Experience section → 10%
    """
    def section_match_rate(section_kws, jd_kws):
      if not section_kws or not jd_kws:
        return 0.0

      matched = get_matched_keywords(section_kws, jd_kws)

      precision = len(matched) / len(section_kws)
      recall = len(matched) / len(jd_kws)

      if precision + recall == 0:
        return 0.0

      return (2 * precision * recall) / (precision + recall)

    skills_kws = resume_sections.get("skills", set())
    projects_kws = resume_sections.get("projects", set())
    experience_kws = resume_sections.get("experience", set())
    # 🔥 Reduce overlap between sections
    projects_kws = projects_kws - skills_kws
    experience_kws = experience_kws - skills_kws - projects_kws

    # Tools = framework/language keywords found anywhere in resume
    all_resume_kws = set()
    for kws in resume_sections.values():
        all_resume_kws |= kws

        jd_split = split_jd_keywords(set().union(*jd_sections.values()))

        jd_skills = jd_split["skills"]
        jd_projects = jd_split["projects"]
        jd_tools = jd_split["tools"]
        jd_experience = jd_split["experience"]
        tools_kws = (
    skills_kws | projects_kws | experience_kws
) & (
    SKILL_GROUPS["frameworks"] |
    SKILL_GROUPS["languages"] |
    SKILL_GROUPS["cloud_devops"]
)

    skills_score = section_match_rate(skills_kws, jd_skills)
    projects_score = section_match_rate(projects_kws, jd_projects)
    tools_score = section_match_rate(tools_kws, jd_tools)
    experience_score = section_match_rate(experience_kws, jd_experience)

    # Fallback: if sections are empty, use full resume
    if not skills_kws and not projects_kws:
        skills_score = section_match_rate(all_resume_kws, jd_skills)
        projects_score = skills_score
        tools_score = skills_score
        experience_score = skills_score

    keyword_score = (
        skills_score * 0.40 +
        projects_score * 0.30 +
        tools_score * 0.20 +
        experience_score * 0.10
    )

    # TF-IDF secondary signal (20% of final score)
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2),
                                     max_features=8000, sublinear_tf=True)
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        tfidf_score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    except Exception:
        tfidf_score = 0.0

    combined = (keyword_score * 0.80) + (tfidf_score * 0.20)
    final = round(min(combined * 100, 100.0), 1)

    breakdown = {
        "skills": round(skills_score * 100, 1),
        "projects": round(projects_score * 100, 1),
        "tools": round(tools_score * 100, 1),
        "experience": round(experience_score * 100, 1),
    }

    return final, breakdown


def compute_role_fit(resume_keywords: set) -> dict:
    """
    Compare resume keywords against role profiles.
    Returns role scores, best fit roles, and the detected role category.
    """
    scores = {}
    for role, profile in ROLE_PROFILES.items():
        profile_kws = profile["keywords"]
        matched = get_matched_keywords(resume_keywords, profile_kws)
        scores[role] = round(len(matched) / len(profile_kws) * 100, 1)

    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_roles = [r for r, s in sorted_roles if s >= 50][:3]
    if not best_roles:
        best_roles = [sorted_roles[0][0]] if sorted_roles else []

    return {
        "role_scores": scores,
        "best_fit_roles": best_roles,
        "top_score": sorted_roles[0][1] if sorted_roles else 0,
    }


def generate_smart_feedback(missing_keywords: list, match_score: float,
                            role_fit: dict, breakdown: dict) -> list:
    """
    Recruiter-style smart feedback instead of generic suggestions.
    """
    feedback = []
    missing_set = set(missing_keywords)

    # ── Overall verdict ────────────────────────────────────────────────
    if match_score >= 85:
        feedback.append({"type": "success", "text":
            "Excellent match! Your resume aligns very well with this role."})
    elif match_score >= 70:
        feedback.append({"type": "success", "text":
            "Strong match! A few targeted additions could make you a top candidate."})
    elif match_score >= 50:
        feedback.append({"type": "warning", "text":
            "Moderate match. Your core skills align but some key areas need strengthening."})
    else:
        feedback.append({"type": "error", "text":
            "Low match. Your profile and this role have significant skill gaps."})

    # ── Section-specific insight ────────────────────────────────────────
    if breakdown.get("skills", 0) < 60:
        feedback.append({"type": "error", "text":
            f"Your Skills section only covers {breakdown['skills']}% of required skills. "
            "Add the missing technologies explicitly in a Technical Skills section."})

    if breakdown.get("projects", 0) < 50:
        feedback.append({"type": "warning", "text":
            f"Projects show {breakdown['projects']}% alignment with the role. "
            "Highlight projects that directly use the required tools and technologies."})

    # ── Domain mismatch detection ───────────────────────────────────────
    devops_missing = missing_set & {"docker", "kubernetes", "ci/cd", "jenkins", "terraform"}
    cloud_missing = missing_set & {"aws", "azure", "gcp", "google cloud"}
    ml_missing = missing_set & {"machine learning", "deep learning", "tensorflow", "pytorch"}
    web_missing = missing_set & {"react", "angular", "vue", "node", "graphql"}

    if len(devops_missing) >= 3:
        feedback.append({"type": "error", "text":
            f"Missing core infrastructure skills: {', '.join(sorted(devops_missing))}. "
            "This role has a strong DevOps requirement your resume doesn't address."})
    elif devops_missing:
        feedback.append({"type": "warning", "text":
            f"Missing some DevOps tools: {', '.join(sorted(devops_missing))}. "
            "Add any containerization or deployment experience you have."})

    if cloud_missing:
        feedback.append({"type": "warning", "text":
            f"No cloud platform experience mentioned ({', '.join(sorted(cloud_missing))}). "
            "Even free-tier or personal project deployments count — add them."})

    if ml_missing:
        feedback.append({"type": "error", "text":
            f"Missing ML/AI fundamentals the JD requires: {', '.join(sorted(ml_missing))}."})

    if web_missing:
        feedback.append({"type": "warning", "text":
            f"Missing frontend/web technologies: {', '.join(sorted(web_missing))}."})

    # ── Role fit insight ────────────────────────────────────────────────
    best_roles = role_fit.get("best_fit_roles", [])
    if best_roles:
        feedback.append({"type": "info", "text":
            f"Your resume is best suited for: {', '.join(best_roles)}."})

    # ── Missing keyword summary ────────────────────────────────────────
    if missing_keywords:
        top = missing_keywords[:5]
        feedback.append({"type": "warning", "text":
            f"Top missing keywords to add: {', '.join(top)}."})

    # ── ATS tip ────────────────────────────────────────────────────────
    if match_score < 80:
        feedback.append({"type": "info", "text":
            "Mirror the job description's exact phrasing in your bullet points — "
            "ATS systems match phrases, not just concepts."})

    feedback.append({"type": "info", "text":
        "Quantify your achievements: accuracy %, latency improvements, team size, "
        "dataset sizes. Numbers dramatically boost ATS and recruiter scores."})

    return feedback


def compute_match_score(resume_text, job_description, resume_keywords, jd_keywords):
    """Legacy single-score function (used as fallback)."""
    if jd_keywords:
        matched = get_matched_keywords(resume_keywords, jd_keywords)
        keyword_score = len(matched) / len(jd_keywords)
    else:
        keyword_score = 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2),
                                     max_features=8000, sublinear_tf=True)
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        tfidf_score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    except Exception:
        tfidf_score = 0.0
    return round(min((keyword_score * 0.80 + tfidf_score * 0.20) * 100, 100.0), 1)


def generate_suggestions(missing_keywords, match_score):
    """Legacy plain-text suggestions (kept for compatibility)."""
    return [f["text"] for f in generate_smart_feedback(missing_keywords, match_score, {}, {})]
