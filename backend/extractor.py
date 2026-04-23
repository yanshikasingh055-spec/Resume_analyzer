import spacy
import re

try:
    nlp = spacy.load("en_core_web_md")
    HAS_VECTORS = True
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")
        HAS_VECTORS = False
    except OSError:
        nlp = None
        HAS_VECTORS = False

TECH_SKILLS = {
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
    "r", "scala", "kotlin", "swift", "php", "ruby", "sql", "html", "css",
    "bash", "shell", "matlab",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost",
    "lightgbm", "huggingface", "transformers", "spacy", "nltk", "gensim",
    "opencv", "yolo", "yolov3", "yolov5", "yolov8", "detectron",
    "machine learning", "deep learning", "neural network", "neural networks",
    "natural language processing", "nlp", "computer vision",
    "reinforcement learning", "transfer learning", "fine-tuning",
    "regression", "classification", "clustering", "segmentation",
    "object detection", "image classification", "text classification",
    "convolutional neural network", "cnn", "cnns",
    "recurrent neural network", "rnn", "lstm", "gru",
    "transformer", "bert", "gpt", "attention mechanism",
    "random forest", "decision tree", "support vector machine", "svm",
    "gradient descent", "backpropagation",
    "feature engineering", "feature extraction",
    "model evaluation", "model deployment", "hyperparameter tuning",
    "cross validation", "precision", "recall", "f1 score", "accuracy",
    "supervised learning", "unsupervised learning",
    "text to speech", "speech recognition", "tts", "gtts",
    "react", "react.js", "reactjs", "angular", "vue",
    "node", "node.js", "nodejs", "express",
    "flask", "django", "fastapi", "spring",
    "rest api", "restful", "restful api", "graphql",
    "html5", "css3", "tailwind", "bootstrap",
    "microservices", "api development",
    "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
    "firebase", "dynamodb", "elasticsearch",
    "database", "query optimization",
    "aws", "azure", "gcp", "google cloud", "heroku", "render", "vercel",
    "docker", "kubernetes", "git", "github", "gitlab",
    "ci/cd", "jenkins", "linux", "ubuntu",
    "version control", "agile", "scrum",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "data analysis", "data science", "data visualization",
    "big data", "etl", "data pipeline",
    "excel", "power query", "pivot table",
    "cybersecurity", "network security",
    "generative ai", "llm", "prompt engineering",
    "accessibility", "responsive design",
}

ALIASES = {
    "react.js": "react", "reactjs": "react",
    "node.js": "node", "nodejs": "node",
    "sklearn": "scikit-learn", "scikit learn": "scikit-learn",
    "postgres": "postgresql",
    "ml": "machine learning", "dl": "deep learning",
    "convolutional neural network": "cnn", "cnns": "cnn",
    "recurrent neural network": "rnn",
    "nlp": "natural language processing",
    "restful api": "rest api", "restful": "rest api",
    "yolov3": "yolo", "yolov5": "yolo", "yolov8": "yolo",
    "gtts": "text to speech",
}

SEMANTIC_SYNONYMS = {
    # Computer Vision
    "opencv": "computer vision", "yolo": "computer vision",
    "yolov3": "computer vision", "yolov5": "computer vision", "yolov8": "computer vision",
    "detectron": "computer vision", "image recognition": "computer vision",
    "image processing": "computer vision", "object detection": "computer vision",
    "image classification": "computer vision", "visual recognition": "computer vision",
    "video analysis": "computer vision", "visual features": "computer vision",
    "image analysis": "computer vision", "video processing": "computer vision",
    "face detection": "computer vision", "face recognition": "computer vision",
    "image segmentation": "computer vision", "food recognition": "computer vision",
    "visual ai": "computer vision", "scene understanding": "computer vision",
    # Deep Learning
    "tensorflow": "deep learning", "pytorch": "deep learning", "keras": "deep learning",
    "cnn": "deep learning", "cnns": "deep learning",
    "convolutional neural network": "deep learning",
    "neural network": "deep learning", "neural networks": "deep learning",
    "lstm": "deep learning", "gru": "deep learning", "rnn": "deep learning",
    "transformer": "deep learning", "bert": "deep learning", "gpt": "deep learning",
    "deep neural network": "deep learning", "dnn": "deep learning",
    "neural net": "deep learning", "backpropagation": "deep learning",
    # Machine Learning
    "ml model": "machine learning", "ml models": "machine learning",
    "predictive modeling": "machine learning", "predictive model": "machine learning",
    "predictive analytics": "machine learning", "statistical modeling": "machine learning",
    "ai model": "machine learning", "artificial intelligence": "machine learning",
    "sklearn": "machine learning", "scikit-learn": "machine learning",
    "xgboost": "machine learning", "random forest": "machine learning",
    "decision tree": "machine learning", "gradient descent": "machine learning",
    # NLP
    "text processing": "natural language processing",
    "text mining": "natural language processing",
    "language model": "natural language processing",
    "sentiment analysis": "natural language processing",
    "named entity recognition": "natural language processing",
    "huggingface": "natural language processing",
    # Database
    "databases": "database", "relational database": "database", "rdbms": "database",
    "data storage": "database", "sql database": "database", "nosql": "database",
    "data management": "database", "mysql": "database", "postgresql": "database",
    "mongodb": "database", "sqlite": "database", "redis": "database",
    # REST API
    "restful api": "rest api", "web api": "rest api", "flask api": "rest api",
    "fastapi": "rest api", "django api": "rest api",
    # Cloud
    "cloud computing": "aws", "cloud platform": "aws", "cloud services": "aws",
    "cloud infrastructure": "aws", "cloud deployment": "aws",
    # Docker
    "containerization": "docker", "containers": "docker", "container": "docker",
    "container orchestration": "kubernetes",
    # Git
    "version control system": "git", "source control": "git", "github": "git", "gitlab": "git",
    # Data
    "exploratory data analysis": "data analysis", "eda": "data analysis",
    "statistical analysis": "data analysis", "pandas": "data analysis", "numpy": "data analysis",
    # Agile
    "agile methodology": "agile", "sprint planning": "scrum",
    # LLM
    "large language model": "llm", "large language models": "llm",
    "generative model": "generative ai", "chatbot": "llm",
    # Transfer Learning
    "pretrained model": "transfer learning", "fine tuning": "fine-tuning",
    # CI/CD
    "continuous integration": "ci/cd", "continuous deployment": "ci/cd", "devops": "ci/cd",
    # Text to speech
    "gtts": "text to speech", "audio feedback": "text to speech",
    # Classification
    "logistic regression": "regression", "linear regression": "regression",
    "binary classification": "classification", "k-means": "clustering",
}

# Section headers to identify resume sections
SECTION_HEADERS = {
    "skills": ["technical skills", "skills", "technologies", "tech stack", "core competencies",
               "programming languages", "tools", "frameworks", "expertise"],
    "projects": ["projects", "personal projects", "academic projects", "key projects",
                 "portfolio", "work samples", "notable projects"],
    "experience": ["experience", "work experience", "professional experience", "employment",
                   "work history", "internship", "internships", "job history"],
    "education": ["education", "academic background", "qualifications", "degrees"],
    "certifications": ["certifications", "certificates", "courses", "training", "achievements"],
}


def normalize(kw):
    return ALIASES.get(kw.strip().lower(), kw.strip().lower())


def extract_keywords(text):
    text_lower = text.lower()
    text_lower = re.sub(r'\s+', ' ', text_lower)
    keywords = set()

    sorted_skills = sorted(TECH_SKILLS, key=len, reverse=True)
    for skill in sorted_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            keywords.add(normalize(skill))

    sorted_synonyms = sorted(SEMANTIC_SYNONYMS.keys(), key=len, reverse=True)
    for phrase in sorted_synonyms:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        if re.search(pattern, text_lower):
            keywords.add(SEMANTIC_SYNONYMS[phrase])

    if nlp:
        try:
            doc = nlp(text[:50000])
            for ent in doc.ents:
                if ent.label_ in ("ORG", "PRODUCT", "WORK_OF_ART"):
                    kw = ent.text.lower().strip()
                    if 2 < len(kw) < 40 and not kw.isnumeric():
                        keywords.add(normalize(kw))
        except Exception:
            pass

    if nlp and HAS_VECTORS:
        try:
            keywords = _expand_with_vectors(text_lower, keywords)
        except Exception:
            pass

    noise = {"the", "and", "for", "with", "this", "that", "are", "was",
             "has", "have", "been", "will", "from", "not", "but", "its",
             "also", "via", "our", "your", "their", "both", "each",
             "any", "all", "new", "can", "may", "more", "well", "team"}
    keywords = {kw for kw in keywords if kw not in noise and len(kw) > 1}
    return keywords


def extract_section_keywords(resume_text):
    """
    Split resume into sections and extract keywords per section.
    Returns dict: { 'skills': set, 'projects': set, 'experience': set, 'other': set }
    """
    lines = resume_text.split('\n')
    sections = {"skills": "", "projects": "", "experience": "", "education": "", "other": ""}
    current_section = "other"

    for line in lines:
        line_lower = line.strip().lower()
        matched_section = None
        for section, headers in SECTION_HEADERS.items():
            if any(h in line_lower for h in headers) and len(line_lower) < 60:
                matched_section = section
                break
        if matched_section:
            current_section = matched_section
        else:
            sections[current_section] += " " + line

    return {
        section: extract_keywords(text)
        for section, text in sections.items()
        if text.strip()
    }


def _expand_with_vectors(text_lower, existing_keywords, threshold=0.82):
    missing_skills = {s for s in TECH_SKILLS if normalize(s) not in existing_keywords}
    if not missing_skills:
        return existing_keywords
    words = text_lower.split()
    candidates = set()
    for i, w in enumerate(words):
        candidates.add(w)
        if i + 1 < len(words):
            candidates.add(f"{w} {words[i+1]}")
        if i + 2 < len(words):
            candidates.add(f"{w} {words[i+1]} {words[i+2]}")
    expanded = set(existing_keywords)
    for skill in missing_skills:
        skill_doc = nlp(skill)
        if not skill_doc.has_vector:
            continue
        for candidate in candidates:
            cand_doc = nlp(candidate)
            if not cand_doc.has_vector:
                continue
            if skill_doc.similarity(cand_doc) >= threshold:
                expanded.add(normalize(skill))
                break
    return expanded


def get_keyword_frequency(text, keywords):
    text_lower = text.lower()
    return {kw: len(re.findall(r'\b' + re.escape(kw) + r'\b', text_lower))
            for kw in keywords}
