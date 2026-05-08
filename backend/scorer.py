print("NEW SCORER LOADED ✅")
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS_KEYWORDS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "sql", "nosql", "r", "scala", "kotlin", "swift", "machine learning",
    "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "matplotlib", "opencv", "keras",
    "flask", "django", "fastapi", "react", "angular", "vue", "node",
    "express", "spring", "aws", "azure", "gcp", "docker", "kubernetes",
    "ci/cd", "git", "linux", "rest", "graphql", "mongodb", "postgresql",
    "mysql", "redis", "spark", "hadoop", "airflow", "tableau", "power bi",
    "data analysis", "feature engineering", "version control", "statistics",
    "natural language processing", "opencv", "yolo", "cnn", "regression",
    "classification", "supervised learning", "model evaluation", "data visualization"
}

TOOLS_KEYWORDS = {
    "docker", "kubernetes", "git", "github", "gitlab", "jenkins", "jira",
    "confluence", "vscode", "pycharm", "jupyter", "postman", "figma",
    "tableau", "power bi", "excel", "aws", "azure", "gcp", "heroku",
    "vercel", "netlify", "terraform", "ansible", "ci/cd", "linux",
    "bash", "airflow", "mlflow", "weights & biases", "wandb", "redis",
    "elasticsearch", "kafka", "rabbitmq", "nginx", "yolo", "opencv",
    "tensorflow", "pytorch", "scikit-learn", "mysql", "mongodb"
}

# Words that appear in JDs but never in resumes — exclude from matching
JD_NOISE_WORDS = {
    # Job posting boilerplate
    "description", "eligibility", "familiarity", "exposure", "developer",
    "developers", "developing", "engineer", "engineers", "entry-level",
    "fresher", "freshers", "field", "growing", "passionate", "ideal",
    "candidate", "candidates", "responsible", "responsibilities",
    "requirement", "requirements", "qualifications", "preferred",
    "required", "bonus", "good", "have", "has", "join", "team", "role",
    "company", "collaborate", "applications", "building", "deploy",
    "deployment", "optimize", "scalability", "bangalore", "remote",
    "india", "location", "cloud", "database", "databases", "control",
    "looking", "seeking", "profile", "portfolio", "track", "record",
    "contribute", "contribution", "day", "one", "real", "world", "year",
    "years", "hands", "growing", "ai", "why", "fit", "great", "plus",
    "understanding", "familiarity", "awareness", "exposure", "grasp",
    "proficiency", "proficient", "expert", "expertise", "senior", "junior",
    "lead", "manage", "coordinate", "implement", "implement", "maintain",
    # Generic English
    "and", "or", "the", "a", "an", "in", "of", "for", "to", "with",
    "is", "are", "be", "on", "at", "by", "as", "we", "you", "your",
    "our", "will", "using", "use", "such", "including", "ability",
    "skills", "skill", "this", "that", "from", "not", "but", "also",
    "work", "build", "design", "create", "write", "new", "key", "main",
    "used", "well", "its", "how", "what", "who", "should", "must", "can",
    "based", "level", "strong", "basic", "working", "like", "into",
    "their", "them", "they", "were", "been", "being", "about", "which",
    "when", "where", "while", "with", "within", "without", "through",
    "across", "between", "among", "above", "below", "over", "under",
    "more", "less", "most", "least", "very", "too", "just", "only",
    "both", "each", "every", "any", "all", "few", "some", "other",
    "these", "those", "same", "different", "various", "multiple",# Add these to your existing JD_NOISE_WORDS set:
    "description", "eligibility", "familiarity", "exposure", "developers",
    "developing", "entry-level", "frameworks", "frontend", "graduate",
    "hands-on", "integration", "intermediate", "final", "fresher", "freshers",
    "computer", "field", "engineer", "accuracy", "detection", "experience",
    "assistive", "data", "full-stack", "full stack", "knowledge", "passion",
    "passionate", "grow", "growing", "stack", "tech", "technology",
    "technologies", "solution", "solutions", "service", "services",
    "performance", "model", "models", "application", "system", "systems",
    # Action verbs and generic job-posting words (not skills)
    "deploy", "deployments", "develop", "integrate", "optimize", "implement",
    "pipelines", "pipeline", "production", "product", "tasks", "task",
    "recent", "final-year", "real-world", "portfolio", "projects",
    "proficiency", "familiarity", "strong", "hands", "powered",
    "backend", "scalable", "scalability", "nutrition", "healthcare"
    # Generic English words that sneak through
"best", "code", "concepts", "continuously", "contributing", "academic",
"agile", "analytical", "basics", "learning", "practices", "oriented",
"detail", "motivated", "modern", "similar", "strong", "good", "basic",
"recent", "quality", "issues", "process", "processes", "oriented",
"object", "scalable", "responsive", "server", "side", "logic",
"review", "reviews", "participate", "improve", "maintain", "test",
"debug", "optimize", "performance", "foundation", "programming",
"problem", "solving", "building", "contribute", "real", "world",
"tools", "new", "frameworks", "practices", "continuously", "learn",
"knowledge", "understanding", "familiarity", "experience", "ability",
"best", "communication", "detail-oriented", "development", "engineering",
"front-end", "full", "stack", "oriented", "motivated", "passionate",
"scalable", "modern", "responsive", "server", "side", "logic",
"review", "reviews", "participate", "improve", "maintain", "test",
"debug", "optimize", "performance", "foundation", "programming",
"problem", "solving", "analytical", "agile", "academic", "concepts",
"continuously", "contributing", "basics", "code", "object", "oriented",
"structures", "algorithms", "cybersecurity", "familiarity", "graduate",
"internship", "cloud", "plus", "similar", "languages", "processes",
"quality", "issues", "tools", "frameworks", "practices", "knowledge",
"understanding", "ability", "learn", "apply", "detail", "oriented"
}

# Explicit tech terms that MUST be checked — always included regardless
MUST_MATCH_TERMS = {
    
    "python", "flask", "fastapi", "django", "react", "mysql", "sql",
    "tensorflow", "opencv", "yolo", "cnn", "machine_learning",
    "deep_learning", "computer_vision", "rest_api", "github", "aws",
    "regression", "classification", "supervised", "numpy",
    "pandas", "scikit-learn", "pytorch", "git", "javascript", "node",
    "docker", "kubernetes", "nlp", "data_analysis", "version_control",
    "object_detection"

}


def normalize(text: str) -> str:
    """Lowercase and normalize common variants."""
    text = text.lower()
    # Expand common abbreviations BEFORE tokenizing
    text = re.sub(r'\bml\b', 'machine_learning', text)
    text = re.sub(r'\bcv\b', 'computer_vision', text)
    text = re.sub(r'\bcnns?\b', 'cnn', text)
    text = re.sub(r'\byolov\d+\b', 'yolo', text)
    text = re.sub(r'\breact\.?js\b', 'react', text)
    text = re.sub(r'\bnode\.?js\b', 'node', text)
    text = re.sub(r'\bgithub\b', 'git github', text)
    # Normalize multi-word phrases BEFORE stripping punctuation
    text = re.sub(r'computer\s+vision', 'computer_vision', text)
    text = re.sub(r'machine\s+learning', 'machine_learning', text)
    text = re.sub(r'deep\s+learning', 'deep_learning', text)
    text = re.sub(r'natural\s+language\s+processing', 'nlp', text)
    text = re.sub(r'version\s+control', 'version_control', text)
    text = re.sub(r'object\s+detection', 'object_detection', text)
    text = re.sub(r'data\s+analysis', 'data_analysis', text)
    # Normalize REST API variants (must happen before stripping punctuation)
    text = re.sub(r'restful\s+apis?', 'rest_api', text)
    text = re.sub(r'rest\s+apis?', 'rest_api', text)
    text = re.sub(r'\bapis?\b', 'api', text)
    # Normalize compound JD tokens that never appear in resumes
    text = re.sub(r'tensorflow/opencv[^\s]*', 'tensorflow opencv', text)
    text = re.sub(r'web/backend', 'web backend', text)
    text = re.sub(r'[^\w\s/\-\+#]', ' ', text)
    return text


def extract_section(text: str, section_names: list) -> str:
    text_lower = text.lower()

    # Sort by length descending so multi-word phrases match before single words
    sorted_names = sorted(section_names, key=len, reverse=True)

    best_start = -1
    matched_name = ""
    for name in sorted_names:
        idx = 0
        while True:
            idx = text_lower.find(name, idx)
            if idx == -1:
                break
            # Only accept if at start of line (preceded by newline or start of string)
            preceding = text_lower[max(0, idx - 2):idx]
            if preceding.strip() == "" or preceding.endswith("\n"):
                if best_start == -1 or idx < best_start:
                    best_start = idx
                    matched_name = name
                break
            idx += 1

    if best_start == -1:
        return ""

    # Only match next section headers at the START of a line
    section_headers = [
        "education", "experience", "work experience", "projects", "skills",
        "technical skills", "certifications", "publications", "awards",
        "summary", "objective", "interests", "references",
        "achievements", "extra", "extra-curricular", "professional summary"
    ]
    end = len(text)
    search_start = best_start + len(matched_name) + 5
    for header in section_headers:
        if header == matched_name:
            continue
        idx = search_start
        while True:
            idx = text_lower.find(header, idx)
            if idx == -1:
                break
            # Only treat as section boundary if at start of line
            preceding = text_lower[max(0, idx - 2):idx]
            if preceding.strip() == "" or preceding.endswith("\n"):
                if idx < end:
                    end = idx
                break
            idx += 1
    return text[best_start:end]


def tfidf_similarity(text1: str, text2: str) -> float:
    if not text1.strip() or not text2.strip():
        return 0.0
    try:
        vec = TfidfVectorizer(ngram_range=(1, 2), max_features=5000, stop_words="english")
        tfidf = vec.fit_transform([text1, text2])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(float(score) * 100, 1)
    except Exception:
        return 0.0


def keyword_overlap_score(resume_text: str, jd_text: str, keyword_set: set) -> float:
    resume_n = normalize(resume_text)
    jd_n = normalize(jd_text)
    jd_hits = {kw for kw in keyword_set if kw in jd_n}
    if not jd_hits:
        return 100.0
    resume_hits = {kw for kw in jd_hits if kw in resume_n}
    return round(len(resume_hits) / len(jd_hits) * 100, 1)


def direct_match_score(resume_text: str, jd_text: str, label: str = "") -> float:
    """
    Match only real tech/skill terms from JD against resume.
    Excludes all noise/boilerplate words.
    """
    jd_n = normalize(jd_text)
    resume_n = normalize(resume_text)

    # Step 1: get all words from JD, remove noise
    words = jd_n.split()
    candidates = {w for w in words if len(w) >= 3 and w not in JD_NOISE_WORDS}

    # Step 2: always include must-match tech terms that appear in JD
    for term in MUST_MATCH_TERMS:
        if term in jd_n:
            candidates.add(term)

    # Step 3: remove words that are clearly not tech terms
    # (heuristic: all-alpha words under 4 chars that aren't known tech)
    known_short_tech = {"sql", "aws", "gcp", "git", "api", "cnn", "nlp",
                        "css", "vue", "r", "go", "c++", "c#"}
    final_terms = set()
    for w in candidates:
        if w in known_short_tech or w in MUST_MATCH_TERMS:
            final_terms.add(w)
        elif len(w) >= 4:
            final_terms.add(w)

    if not final_terms:
        return 0.0

    matched = {kw for kw in final_terms if kw in resume_n}
    score = len(matched) / len(final_terms) * 100

    print(f"[{label}] Terms: {len(final_terms)}, Matched: {len(matched)}, Score: {score:.1f}%")
    print(f"[{label}] Unmatched: {sorted(final_terms - matched)[:10]}")

    return round(score, 1)


def compute_scores(resume_text: str, jd_text: str) -> dict:
    # ── Skills Score (40%) ──────────────────────────────────────────────────
    skills_section = extract_section(resume_text, ["technical skills", "core competencies", "skills"])
    skills_text = skills_section if len(skills_section) > 50 else resume_text
    skills_kw   = keyword_overlap_score(resume_text, jd_text, SKILLS_KEYWORDS)
    skills_dir  = direct_match_score(skills_text, jd_text, "SKILLS")
    skills_tfidf = tfidf_similarity(skills_text, jd_text)
    skills_score = round(0.45 * skills_kw + 0.35 * skills_dir + 0.20 * skills_tfidf, 1)

    # ── Projects Score (30%) ────────────────────────────────────────────────
    projects_section = extract_section(resume_text, ["projects", "personal projects", "academic projects"])
    if len(projects_section) > 50:
    # Use full resume for keyword overlap (skills apply across whole resume)
    # Use only projects section for direct/tfidf match
       proj_kw    = keyword_overlap_score(resume_text, jd_text, SKILLS_KEYWORDS)
       proj_dir   = direct_match_score(projects_section, jd_text, "PROJECTS")
       proj_tfidf = tfidf_similarity(projects_section, jd_text)
       projects_score = round(0.45 * proj_kw + 0.35 * proj_dir + 0.20 * proj_tfidf, 1)
    else:
        projects_score = 0.0

    # ── Tools Score (20%) ───────────────────────────────────────────────────
    # Prefer full technical skills section (has all tools) over narrow "Tools & Cloud" subsection
    tools_section = extract_section(resume_text, ["tools", "technologies", "tech stack"])
    # If tools section is a subsection (< 200 chars), use the full skills section instead
    # since "Tools & Cloud: GitHub, AWS" alone misses all the ML/framework tools
    if len(tools_section) < 200 and len(skills_section) > 50:
        tools_text = skills_section
    elif len(tools_section) > 50:
        tools_text = tools_section
    else:
        tools_text = resume_text
    tools_kw   = keyword_overlap_score(resume_text, jd_text, TOOLS_KEYWORDS)
    tools_dir  = direct_match_score(tools_text, jd_text, "TOOLS")
    tools_tfidf = tfidf_similarity(tools_text, jd_text)
    tools_score = round(0.50 * tools_kw + 0.30 * tools_dir + 0.20 * tools_tfidf, 1)

    # ── Experience Score (10%) ──────────────────────────────────────────────
    exp_section = extract_section(resume_text, [
        "work experience", "employment",
        "internship", "professional experience"
    ])
    # For freshers with no work experience, fall back to projects (NOT summary)
    exp_text = exp_section if len(exp_section) > 50 else (
        projects_section if len(projects_section) > 50 else resume_text[-1000:]
    )
    exp_dir   = direct_match_score(exp_text, jd_text, "EXPERIENCE")
    exp_tfidf = tfidf_similarity(exp_text, jd_text)
    experience_score = round(0.55 * exp_dir + 0.45 * exp_tfidf, 1)

    # ── Overall ─────────────────────────────────────────────────────────────
    overall = round(
        0.40 * skills_score   +
        0.35 * projects_score +
        0.20 * tools_score    +
        0.05 * experience_score,
        1
    )

    print(f"\n=== FINAL SCORES ===")
    print(f"Skills: {skills_score} | Projects: {projects_score} | Tools: {tools_score} | Experience: {experience_score}")
    print(f"Overall: {overall}\n")

    return {
        "match_score": overall,
        "score_breakdown": {
            "skills":     skills_score,
            "projects":   projects_score,
            "tools":      tools_score,
            "experience": experience_score
        }
    }


def compute_weighted_score(resume_sections: dict, jd_keywords: set,
                            resume_text: str, jd_text: str):
    result = compute_scores(resume_text, jd_text)
    return result["match_score"], result["score_breakdown"]


def get_matched_keywords(resume_keywords: set, jd_keywords: set) -> set:
    return set(resume_keywords) & set(jd_keywords)


def get_missing_keywords(resume_keywords: set, jd_keywords: set) -> list:
    return sorted(list(set(jd_keywords) - set(resume_keywords)))


def compute_role_fit(resume_keywords: set) -> dict:
    ROLE_PROFILES = {
        "ML Engineer": {"python", "tensorflow", "pytorch", "scikit-learn", "machine learning", "deep learning"},
        "Data Scientist": {"python", "pandas", "numpy", "statistics", "machine learning", "sql", "data analysis"},
        "Backend Engineer": {"python", "java", "flask", "django", "fastapi", "sql", "rest", "docker"},
        "Frontend Engineer": {"javascript", "typescript", "react", "vue", "angular", "css", "html"},
        "DevOps Engineer": {"docker", "kubernetes", "ci/cd", "aws", "azure", "gcp", "terraform", "linux"},
        "AI/Computer Vision Engineer": {"opencv", "computer vision", "deep learning", "pytorch", "tensorflow", "python"},
        "Full Stack Engineer": {"react", "node", "python", "sql", "rest", "docker", "javascript"},
        "Data Engineer": {"spark", "hadoop", "airflow", "sql", "python", "kafka", "aws"},
    }
    kw_lower = {k.lower() for k in resume_keywords}
    role_scores = {}
    for role, required in ROLE_PROFILES.items():
        matched = required & kw_lower
        role_scores[role] = round(len(matched) / len(required) * 100, 1)
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    best_fit_roles = [r for r, s in sorted_roles if s >= 30][:3]
    return {
        "role_scores": role_scores,
        "best_fit_roles": best_fit_roles,
        "top_score": sorted_roles[0][1] if sorted_roles else 0
    }


def generate_smart_feedback(missing: list, match_score: float,
                             role_fit: dict, breakdown: dict) -> list:
    feedback = []
    if match_score < 40:
        feedback.append({"type": "error", "text": "Low match. Your profile and this role have significant skill gaps."})
    elif match_score < 65:
        feedback.append({"type": "warning", "text": "Moderate match. Targeted improvements could make you competitive."})
    else:
        feedback.append({"type": "success", "text": "Strong match! Your profile aligns well with this role."})
    if missing:
        feedback.append({"type": "tip", "text": f"Add these missing keywords: {', '.join(missing[:5])}."})
    weakest = min(breakdown, key=breakdown.get)
    feedback.append({"type": "tip", "text": f"Your weakest area is '{weakest}' ({breakdown[weakest]}%). Focus on strengthening this section."})
    if role_fit.get("best_fit_roles"):
        feedback.append({"type": "info", "text": f"Best suited for: {', '.join(role_fit['best_fit_roles'])}."})
    return feedback