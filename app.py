"""
Sun Devil Circle - Peer Support Platform for International Freshman Students at ASU
Flask backend with in-memory storage, AI abstraction, and safety moderation.
"""

import os
import re
import secrets
import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Use a stable secret key for session persistence
app.secret_key = os.environ.get("SECRET_KEY", "sun-devil-circle-dev-key-2024")

# AI Configuration - Set defaults so AI works out of the box
if not os.environ.get("CEREBRAS_API_KEY"):
    os.environ["CEREBRAS_API_KEY"] = "csk-kyp53f5c5ev35p9hxjf8txpd2xdmf4ne4v3f3venh5t28kpy"
if not os.environ.get("LIVE_AI"):
    os.environ["LIVE_AI"] = "1"


DATABASE = "auth.db"



# -----------------------------------------------------------------------------
# Database Functions (SQLite for credentials only)
# -----------------------------------------------------------------------------

def get_db():
    """Get database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database with users and profiles tables."""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                display_name TEXT,
                is_international_freshman INTEGER DEFAULT 0,
                preferred_language TEXT DEFAULT '',
                primary_challenge TEXT DEFAULT '',
                support_style TEXT DEFAULT 'mixed',
                support_topics TEXT DEFAULT '',
                languages TEXT DEFAULT '',
                cultural_background TEXT DEFAULT '',
                onboarding_complete INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        # Migrate existing tables to add new columns if they don't exist
        try:
            db.execute('ALTER TABLE profiles ADD COLUMN support_topics TEXT DEFAULT ""')
        except:
            pass
        try:
            db.execute('ALTER TABLE profiles ADD COLUMN languages TEXT DEFAULT ""')
        except:
            pass
        try:
            db.execute('ALTER TABLE profiles ADD COLUMN cultural_background TEXT DEFAULT ""')
        except:
            pass
        try:
            db.execute('ALTER TABLE profiles ADD COLUMN onboarding_complete INTEGER DEFAULT 0')
        except:
            pass
        db.commit()


def save_profile_to_db(user_id, profile_dict):
    """Save profile to database."""
    db = get_db()
    challenges = ','.join(profile_dict.get('primary_challenge', []))
    support_topics = ','.join(profile_dict.get('support_topics', []))
    languages = ','.join(profile_dict.get('languages', []))
    cultural_background = ','.join(profile_dict.get('cultural_background', []))
    db.execute('''
        INSERT OR REPLACE INTO profiles 
        (user_id, display_name, is_international_freshman, preferred_language, primary_challenge, support_style, support_topics, languages, cultural_background, onboarding_complete)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        profile_dict.get('display_name', ''),
        1 if profile_dict.get('is_international_freshman') else 0,
        profile_dict.get('preferred_language', ''),
        challenges,
        profile_dict.get('support_style', 'mixed'),
        support_topics,
        languages,
        cultural_background,
        1 if profile_dict.get('onboarding_complete') else 0
    ))
    db.commit()


def load_profile_from_db(user_id):
    """Load profile from database and return dict."""
    db = get_db()
    row = db.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,)).fetchone()
    if row:
        challenges = row['primary_challenge'].split(',') if row['primary_challenge'] else []
        # Handle new columns that might not exist in older databases
        support_topics = []
        languages = []
        cultural_background = []
        onboarding_complete = False
        try:
            support_topics = row['support_topics'].split(',') if row['support_topics'] else []
            languages = row['languages'].split(',') if row['languages'] else []
            cultural_background = row['cultural_background'].split(',') if row['cultural_background'] else []
            onboarding_complete = bool(row['onboarding_complete'])
        except:
            pass
        return {
            'display_name': row['display_name'] or '',
            'is_international_freshman': bool(row['is_international_freshman']),
            'preferred_language': row['preferred_language'] or '',
            'primary_challenge': challenges,
            'support_style': row['support_style'] or 'mixed',
            'support_topics': support_topics,
            'languages': languages,
            'cultural_background': cultural_background,
            'onboarding_complete': onboarding_complete
        }
    return None



def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------------------------------------------------------
# In-Memory Storage
# -----------------------------------------------------------------------------

# Preset topic groups
PRESET_GROUPS = [
    "Homesickness and Family",
    "Academic Pressure",
    "Making Friends",
    "Cultural Adjustment",
    "Language Barriers",
    "Financial Stress",
    "Health and Wellness",
    "Career and Internships",
]

# In-memory groups: { "topic": [ {"timestamp": str, "display_name": str, "text": str}, ... ] }
groups = {topic: [] for topic in PRESET_GROUPS}

# Connection requests: { recipient_user_id: [ {sender_id, sender_display_name, message, timestamp}, ... ] }
pending_requests = {}

# User profiles cache for display: { user_id: {display_name, profile_summary} }
user_profiles = {}

# Basic profanity list for validation
PROFANITY_LIST = [
    "damn", "hell", "crap", "bastard", "idiot", "stupid", "dumb", "loser",
    "jerk", "moron", "fool", "imbecile", "ass", "shut up"
]

# Severe distress keywords
SEVERE_DISTRESS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "self-harm",
    "cutting myself", "overdose", "no reason to live", "better off dead"
]

# Offensive language patterns
OFFENSIVE_PATTERNS = [
    r"\b(hate\s+you|go\s+to\s+hell|f\s*u\s*c\s*k|s\s*h\s*i\s*t)\b",
    r"\b(retard|faggot|nigger|bitch|whore|slut)\b"
]

# -----------------------------------------------------------------------------
# ASU Resources (Real URLs)
# -----------------------------------------------------------------------------

ASU_RESOURCES = [
    {"name": "ASU Counseling Services", "url": "https://eoss.asu.edu/counseling"},
    {"name": "International Students and Scholars Center", "url": "https://issc.asu.edu/"},
    {"name": "ASU Health Services", "url": "https://eoss.asu.edu/health"},
    {"name": "Dean of Students", "url": "https://eoss.asu.edu/dos"},
    {"name": "ASU Career and Professional Development Services", "url": "https://career.asu.edu/"},
    {"name": "ASU Tutoring and Academic Success", "url": "https://tutoring.asu.edu/"},
    {"name": "Sun Devil Fitness Complex", "url": "https://fitness.asu.edu/"},
    {"name": "ASU Writing Centers", "url": "https://tutoring.asu.edu/writing-centers"},
]

EMERGENCY_RESOURCE = {
    "name": "988 Suicide and Crisis Lifeline",
    "url": "https://988lifeline.org/"
}

# -----------------------------------------------------------------------------
# Semantic Matching (Hugging Face Embeddings)
# -----------------------------------------------------------------------------

# In-memory embedding storage
user_embeddings = {}  # {user_id: [float, ...]}
group_embeddings = {}  # {group_name: [float, ...]}

# HF model for embeddings
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HF_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{HF_EMBEDDING_MODEL}"


def build_profile_text(profile_dict):
    """Build a readable text block from profile fields for embedding."""
    parts = []

    if profile_dict.get("is_international_freshman"):
        parts.append("I am an international freshman student.")

    challenges = profile_dict.get("primary_challenge", [])
    if challenges:
        challenge_text = ", ".join(challenges)
        parts.append(f"My main challenges are: {challenge_text}.")

    language = profile_dict.get("preferred_language")
    if language:
        parts.append(f"My preferred language is {language}.")

    support_style = profile_dict.get("support_style", "mixed")
    if support_style == "listening":
        parts.append("I prefer to listen and receive support.")
    elif support_style == "sharing":
        parts.append("I prefer to share my experiences with others.")
    else:
        parts.append("I am open to both listening and sharing.")

    interests = profile_dict.get("interests", [])
    if interests:
        interest_text = ", ".join(interests)
        parts.append(f"My interests include: {interest_text}.")

    display_name = profile_dict.get("display_name", "")
    if display_name:
        parts.insert(0, f"My name is {display_name}.")

    return " ".join(parts) if parts else "International student looking for peer support."


def embed_text(text):
    """
    Get embedding vector from Hugging Face Inference API.
    Returns list of floats or None if API fails.
    """
    if os.environ.get("LIVE_AI") != "1":
        return None

    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return None

    try:
        import requests
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {"inputs": text, "options": {"wait_for_model": True}}
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    return result[0]
                return result
        return None
    except Exception:
        return None


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def get_top_matches(target_embedding, candidates, top_n=5, threshold=0.3):
    """
    Find top matching candidates based on cosine similarity.
    candidates: dict of {key: embedding}
    Returns: list of (key, similarity_score) sorted by score descending
    """
    if not target_embedding:
        return []

    scores = []
    for key, embedding in candidates.items():
        if embedding:
            sim = cosine_similarity(target_embedding, embedding)
            if sim >= threshold:
                scores.append((key, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


def keyword_score(text_a, text_b):
    """Fallback keyword-based similarity scoring."""
    if not text_a or not text_b:
        return 0.0

    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())

    stopwords = {"i", "am", "a", "an", "the", "is", "are", "my", "to", "and", "or", "for", "with", "in", "on", "at"}
    words_a = words_a - stopwords
    words_b = words_b - stopwords

    if not words_a or not words_b:
        return 0.0

    intersection = len(words_a & words_b)
    union = len(words_a | words_b)

    return intersection / union if union > 0 else 0.0


def get_keyword_matches(target_text, candidates_text, top_n=5, threshold=0.1):
    """
    Fallback matching using keyword overlap.
    candidates_text: dict of {key: text}
    Returns: list of (key, score) sorted by score descending
    """
    scores = []
    for key, text in candidates_text.items():
        score = keyword_score(target_text, text)
        if score >= threshold:
            scores.append((key, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


def store_user_embedding(user_id, profile_dict):
    """Generate and store embedding for a user profile."""
    profile_text = build_profile_text(profile_dict)
    embedding = embed_text(profile_text)

    if embedding:
        user_embeddings[user_id] = embedding
    else:
        user_embeddings[user_id] = {"text": profile_text}

    return embedding is not None


def store_group_embedding(group_name):
    """Generate and store embedding for a group topic."""
    if group_name in group_embeddings:
        return True

    embedding = embed_text(group_name)

    if embedding:
        group_embeddings[group_name] = embedding
    else:
        group_embeddings[group_name] = {"text": group_name}

    return embedding is not None


def init_group_embeddings():
    """Initialize embeddings for all preset groups."""
    for group_name in PRESET_GROUPS:
        store_group_embedding(group_name)


def get_recommended_groups_semantic(user_id, top_n=5):
    """
    Get recommended groups for a user using semantic matching.
    Falls back to keyword matching if embeddings unavailable.
    """
    user_data = user_embeddings.get(user_id)

    if not user_data:
        return list(PRESET_GROUPS)[:top_n]

    if isinstance(user_data, list):
        valid_embeddings = {
            k: v for k, v in group_embeddings.items()
            if isinstance(v, list)
        }
        if valid_embeddings:
            matches = get_top_matches(user_data, valid_embeddings, top_n=top_n, threshold=0.2)
            if matches:
                return [m[0] for m in matches]

    user_text = user_data.get("text", "") if isinstance(user_data, dict) else ""
    if user_text:
        group_texts = {
            k: v.get("text", k) if isinstance(v, dict) else k
            for k, v in group_embeddings.items()
        }
        matches = get_keyword_matches(user_text, group_texts, top_n=top_n, threshold=0.05)
        if matches:
            return [m[0] for m in matches]

    return list(PRESET_GROUPS)[:top_n]


def get_similar_users(user_id, top_n=5, threshold=0.4):
    """
    Find similar users based on profile embeddings.
    Excludes self from results.
    Falls back to keyword matching if embeddings unavailable.
    """
    user_data = user_embeddings.get(user_id)

    if not user_data:
        return []

    other_users = {k: v for k, v in user_embeddings.items() if k != user_id}

    if not other_users:
        return []

    if isinstance(user_data, list):
        valid_embeddings = {
            k: v for k, v in other_users.items()
            if isinstance(v, list)
        }
        if valid_embeddings:
            matches = get_top_matches(user_data, valid_embeddings, top_n=top_n, threshold=threshold)
            return [(m[0], m[1]) for m in matches]

    user_text = user_data.get("text", "") if isinstance(user_data, dict) else ""
    if user_text:
        other_texts = {
            k: v.get("text", "") if isinstance(v, dict) else ""
            for k, v in other_users.items()
        }
        matches = get_keyword_matches(user_text, other_texts, top_n=top_n, threshold=0.1)
        return [(m[0], m[1]) for m in matches]

    return []


def get_users_for_group(group_name, top_n=10):
    """
    Find users who might be interested in a specific group.
    Used for group creation and suggestions.
    """
    group_data = group_embeddings.get(group_name)

    if not group_data:
        store_group_embedding(group_name)
        group_data = group_embeddings.get(group_name)

    if not group_data:
        return []

    if isinstance(group_data, list):
        valid_users = {
            k: v for k, v in user_embeddings.items()
            if isinstance(v, list)
        }
        if valid_users:
            matches = get_top_matches(group_data, valid_users, top_n=top_n, threshold=0.3)
            return [(m[0], m[1]) for m in matches]

    group_text = group_data.get("text", group_name) if isinstance(group_data, dict) else group_name
    user_texts = {
        k: v.get("text", "") if isinstance(v, dict) else ""
        for k, v in user_embeddings.items()
    }
    matches = get_keyword_matches(group_text, user_texts, top_n=top_n, threshold=0.05)
    return [(m[0], m[1]) for m in matches]

# -----------------------------------------------------------------------------
# AI Abstraction Functions
# -----------------------------------------------------------------------------

def detect_severe_distress(text):
    """Check if text contains severe distress signals."""
    text_lower = text.lower()
    for keyword in SEVERE_DISTRESS_KEYWORDS:
        if keyword in text_lower:
            return True
    return False


def detect_offensive_language(text):
    """Check if text contains offensive language."""
    text_lower = text.lower()
    for pattern in OFFENSIVE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    for word in PROFANITY_LIST:
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            return True
    return False


def get_mock_support_options(issue_text, profile_dict):
    """Generate deterministic support options based on keywords."""
    options = ["Talk to a peer who understands your situation"]
    issue_lower = issue_text.lower()

    if any(w in issue_lower for w in ["lonely", "alone", "isolated", "miss"]):
        options.append("Join a peer support group for homesickness")
    if any(w in issue_lower for w in ["stress", "pressure", "overwhelm", "exam", "grade"]):
        options.append("Explore academic support resources")
    if any(w in issue_lower for w in ["friend", "social", "connect", "people"]):
        options.append("Attend a campus social event")
    if any(w in issue_lower for w in ["language", "english", "speak", "communication"]):
        options.append("Use language exchange or tutoring services")
    if any(w in issue_lower for w in ["money", "financial", "expensive", "afford"]):
        options.append("Consult financial aid or emergency assistance")
    if any(w in issue_lower for w in ["health", "sick", "doctor", "tired", "sleep"]):
        options.append("Visit campus health services")

    if len(options) == 1:
        options.append("Reach out to the International Students Center")
        options.append("Speak with a counselor for guidance")

    return options[:5]


def get_mock_recommended_groups(issue_text, profile_dict):
    """Recommend groups based on issue keywords."""
    recommended = []
    issue_lower = issue_text.lower()

    keyword_map = {
        "Homesickness and Family": ["home", "homesick", "family", "miss", "lonely", "alone"],
        "Academic Pressure": ["exam", "grade", "study", "stress", "class", "professor"],
        "Making Friends": ["friend", "social", "connect", "people", "meet"],
        "Cultural Adjustment": ["culture", "different", "adjust", "custom", "food"],
        "Language Barriers": ["language", "english", "speak", "understand", "communication"],
        "Financial Stress": ["money", "financial", "expensive", "afford", "job"],
        "Health and Wellness": ["health", "sick", "tired", "sleep", "exercise", "mental"],
        "Career and Internships": ["career", "internship", "job", "resume", "interview"],
    }

    for group, keywords in keyword_map.items():
        if any(kw in issue_lower for kw in keywords):
            recommended.append(group)

    if not recommended:
        recommended = ["Homesickness and Family", "Making Friends"]

    return recommended[:3]


def mock_ai_suggest_resources_and_options(issue_text, profile_dict, followup_count, followup_question=None):
    """Deterministic mock AI for resource suggestions."""
    support_options = get_mock_support_options(issue_text, profile_dict)
    recommended_groups = get_mock_recommended_groups(issue_text, profile_dict)

    resources = ASU_RESOURCES[:8].copy()
    if detect_severe_distress(issue_text):
        resources.insert(0, EMERGENCY_RESOURCE)

    disclaimer = (
        "These suggestions are informational only and do not constitute professional "
        "or medical advice. If you are in crisis, please contact a professional immediately."
    )

    if followup_question:
        followup_lower = followup_question.lower()
        if "how" in followup_lower or "what" in followup_lower:
            support_options.insert(0, "Consider starting with the first resource listed above")
        if "more" in followup_lower:
            support_options.append("Explore the ASU Student Services portal for additional options")

    return {
        "support_options": support_options,
        "asu_resources": resources,
        "recommended_groups": recommended_groups,
        "safe_disclaimer": disclaimer
    }


def mock_ai_moderate_message(message_text):
    """Deterministic mock AI for chat moderation."""
    if detect_offensive_language(message_text):
        return {
            "allowed": False,
            "reason": "offensive_language",
            "user_message": "Your message was not sent because it contains inappropriate language."
        }
    if detect_severe_distress(message_text):
        return {
            "allowed": True,
            "reason": "severe_distress",
            "user_message": message_text
        }
    return {
        "allowed": True,
        "reason": "ok",
        "user_message": message_text
    }


def call_live_ai(endpoint, payload):
    """Call live AI endpoint if configured."""
    import requests
    ai_url = os.environ.get("AI_ENDPOINT_URL")
    ai_key = os.environ.get("AI_ENDPOINT_KEY")

    if not ai_url or not ai_key:
        return None

    try:
        headers = {"Authorization": f"Bearer {ai_key}", "Content-Type": "application/json"}
        response = requests.post(f"{ai_url}/{endpoint}", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def call_ai_api(prompt, max_tokens=300):
    """Call Cerebras AI API for text generation."""
    if os.environ.get("LIVE_AI") != "1":
        return None

    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        return None

    try:
        from cerebras.cloud.sdk import Cerebras

        client = Cerebras(api_key=api_key)

        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b",
            max_completion_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            stream=False
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Cerebras API error: {e}")
        return None






def generate_support_response(issue_text, profile_dict):
    """Generate personalized support response with empathetic message, suggestions, and relevant resources."""
    profile_summary = build_profile_text(profile_dict)
    
    # Format available resources for the prompt
    resources_list = "\n".join([f"{i+1}. {r['name']}" for i, r in enumerate(ASU_RESOURCES)])

    prompt = f"""You are a caring, supportive counselor at ASU helping an international freshman student who is struggling.

Student Profile: {profile_summary}

Student's Issue: {issue_text}

Available ASU Resources:
{resources_list}

Task:
1. Write a warm, empathetic message (2-3 sentences) acknowledging their feelings and validating their experience.
2. Provide 5 specific, actionable suggestions.
3. Select the 3 most relevant ASU Resources from the list above by their number (e.g., 1, 4, 7).

Format your response EXACTLY like this:
MESSAGE: [Your empathetic message here]

SUGGESTIONS:
1. [First suggestion]
2. [Second suggestion]  
3. [Third suggestion]
4. [Fourth suggestion]
5. [Fifth suggestion]

RESOURCES: [comma separated numbers, e.g. 1, 5, 8]"""

    response = call_ai_api(prompt, max_tokens=500)

    if response:
        # Parse message, suggestions, and resources
        empathetic_message = ""
        suggestions = []
        resource_indices = []
        
        # Extract Message
        if "MESSAGE:" in response:
            parts = response.split("SUGGESTIONS:")
            if len(parts) >= 2:
                empathetic_message = parts[0].replace("MESSAGE:", "").strip()
                remaining = parts[1]
                
                # Extract Suggestions and Resources
                if "RESOURCES:" in remaining:
                    sugg_parts = remaining.split("RESOURCES:")
                    suggestion_text = sugg_parts[0]
                    resource_text = sugg_parts[1].strip()
                    
                    # Parse Suggestions
                    lines = suggestion_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 3:
                            if line[0].isdigit() and '.' in line[:3]:
                                line = line.split('.', 1)[1].strip()
                            if line:
                                suggestions.append(line)

                    # Parse Resource Indices
                    try:
                        # Extract numbers using regex to handle various formats
                        import re
                        numbers = re.findall(r'\d+', resource_text)
                        resource_indices = [int(n) - 1 for n in numbers if n.isdigit()] # Convert 1-based to 0-based
                        # Filter valid indices
                        resource_indices = [idx for idx in resource_indices if 0 <= idx < len(ASU_RESOURCES)]
                    except Exception:
                        pass
        
        if empathetic_message or suggestions:
            return {
                "message": empathetic_message,
                "suggestions": suggestions[:5] if suggestions else [],
                "resource_indices": resource_indices
            }

    return None




def generate_followup_answer(issue_text, followup_question, profile_dict, history=None):
    """Generate answer to a follow-up question using AI."""
    profile_summary = build_profile_text(profile_dict)

    history_text = ""
    if history:
        history_text = "\n\nPrevious Q&A:\n"
        for item in history[-3:]:  # Last 3 items only
            history_text += f"Q: {item['question']}\nA: {item['answer']}\n"

    prompt = f"""You are a supportive counselor at ASU helping an international freshman student.

Student Profile: {profile_summary}
Original Issue: {issue_text}
{history_text}
Current Question: {followup_question}

Provide a helpful, specific answer to the student's question. Be warm, practical, and reference ASU resources when relevant. Keep your response to 2-3 sentences.

Answer:"""

    response = call_ai_api(prompt, max_tokens=150)

    if response:
        # Clean up the response
        answer = response.strip()
        if answer.startswith("Answer:"):
            answer = answer[7:].strip()
        if answer:
            return answer

    return None


def ai_suggest_resources_and_options(issue_text, profile_dict, followup_count, followup_question=None):
    """AI abstraction for resource suggestions. Falls back to mock if live AI unavailable."""
    # Try to get AI-generated response
    ai_response = None
    empathetic_message = ""
    support_options = []

    if os.environ.get("LIVE_AI") == "1":
        ai_response = generate_support_response(issue_text, profile_dict)

    if ai_response:
        empathetic_message = ai_response.get("message", "")
        support_options = ai_response.get("suggestions", [])
        
    # Get resources
    resources = []
    
    # Use AI-selected resources if available
    if ai_response and ai_response.get("resource_indices"):
        for idx in ai_response["resource_indices"]:
            if 0 <= idx < len(ASU_RESOURCES):
                resources.append(ASU_RESOURCES[idx])
    
    # If no valid AI resources, use default fallback (first 8)
    if not resources:
        resources = ASU_RESOURCES[:8].copy()

    # Always add emergency resource if distress detected
    if detect_severe_distress(issue_text):
        resources.insert(0, EMERGENCY_RESOURCE)

    # Fall back to mock if AI didn't provide suggestions
    if not support_options:
        support_options = get_mock_support_options(issue_text, profile_dict)

    # Get recommended groups
    recommended_groups = get_mock_recommended_groups(issue_text, profile_dict)

    disclaimer = (

        "These suggestions are informational only and do not constitute professional "
        "or medical advice. If you are in crisis, please contact a professional immediately."
    )

    return {
        "empathetic_message": empathetic_message,
        "support_options": support_options,
        "asu_resources": resources,
        "recommended_groups": recommended_groups,
        "safe_disclaimer": disclaimer
    }



def ai_generate_followup_response(issue_text, followup_question, profile_dict, history=None):
    """Generate a response to a follow-up question."""
    if os.environ.get("LIVE_AI") == "1":
        ai_response = generate_followup_answer(issue_text, followup_question, profile_dict, history)
        if ai_response:
            return ai_response

    # Fallback response
    return ("Based on your question, consider exploring the resources listed above. "
            "Start with the option that feels most relevant to your situation.")


def ai_moderate_message(message_text):
    """AI abstraction for chat moderation. Falls back to mock if live AI unavailable."""
    if os.environ.get("LIVE_AI") == "1":
        payload = {"message_text": message_text}
        result = call_live_ai("moderate", payload)
        if result:
            return result

    return mock_ai_moderate_message(message_text)


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def get_profile_dict():
    """Extract profile fields from session."""
    return {
        "display_name": session.get("display_name", ""),
        "is_international_freshman": session.get("is_international_freshman", False),
        "preferred_language": session.get("preferred_language", ""),
        "primary_challenge": session.get("primary_challenge", []),
        "support_style": session.get("support_style", "mixed"),
    }


def check_profanity(text):
    """Basic profanity check for group topic validation."""
    text_lower = text.lower()
    for word in PROFANITY_LIST:
        if word in text_lower:
            return True
    return False


def find_relevant_group(topic_text):
    """Check if a relevant active group exists based on keyword overlap."""
    topic_lower = topic_text.lower()
    words = set(topic_lower.split())

    for group_topic in groups.keys():
        group_words = set(group_topic.lower().split())
        if words & group_words:
            return group_topic
    return None


# -----------------------------------------------------------------------------
# Landing Page Route
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """Landing page with hero section."""
    return render_template("index.html")


# -----------------------------------------------------------------------------
# Authentication Routes
# -----------------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page."""
    if session.get("user_id"):
        # Check if onboarding is complete
        profile = load_profile_from_db(session.get("user_id"))
        if profile and profile.get("onboarding_complete"):
            return redirect(url_for("decision"))
        return redirect(url_for("onboarding"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            error = "Username and password are required."
        else:
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()

            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]

                # Load profile from database if exists
                profile = load_profile_from_db(user["id"])
                if profile:
                    session["display_name"] = profile["display_name"]
                    session["is_international_freshman"] = profile["is_international_freshman"]
                    session["preferred_language"] = profile["preferred_language"]
                    session["primary_challenge"] = profile["primary_challenge"]
                    session["support_style"] = profile["support_style"]
                    session["support_topics"] = profile.get("support_topics", [])
                    session["languages"] = profile.get("languages", [])
                    session["cultural_background"] = profile.get("cultural_background", [])
                    session["onboarding_complete"] = profile.get("onboarding_complete", False)
                    
                    # Redirect based on onboarding status
                    if profile.get("onboarding_complete"):
                        return redirect(url_for("decision"))
                    else:
                        return redirect(url_for("onboarding"))
                else:
                    return redirect(url_for("onboarding"))
            else:
                error = "Invalid username or password."

    return render_template("login.html", error=error)



@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup page."""
    if session.get("user_id"):
        return redirect(url_for("profile"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password cannot be empty."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif len(username) > 50:
            error = "Username must be 50 characters or less."
        else:
            db = get_db()
            existing = db.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()

            if existing:
                error = "Username already exists. Please choose another."
            else:
                password_hash = generate_password_hash(password)
                created_at = datetime.now().isoformat()
                db.execute(
                    "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                    (username, password_hash, created_at)
                )
                db.commit()

                user = db.execute(
                    "SELECT * FROM users WHERE username = ?", (username,)
                ).fetchone()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("onboarding"))

    return render_template("signup.html", error=error)


@app.route("/logout")
def logout():
    """Logout and clear session."""
    session.clear()
    return redirect(url_for("index"))


# -----------------------------------------------------------------------------
# Onboarding Routes
# -----------------------------------------------------------------------------

@app.route("/onboarding")
@login_required
def onboarding():
    """Multi-step onboarding wizard."""
    # If onboarding already complete, redirect to dashboard
    user_id = session.get("user_id")
    profile = load_profile_from_db(user_id)
    if profile and profile.get("onboarding_complete"):
        return redirect(url_for("decision"))
    return render_template("onboarding.html")


@app.route("/onboarding/submit", methods=["POST"])
@login_required
def onboarding_submit():
    """Process onboarding form submission."""
    user_id = session.get("user_id")
    
    # Parse form data
    support_topics = request.form.get("support_topics", "").split(",")
    support_topics = [t.strip() for t in support_topics if t.strip()]
    
    languages = request.form.get("languages", "").split(",")
    languages = [l.strip() for l in languages if l.strip()]
    
    support_style = request.form.get("support_style", "mixed")
    
    cultural_background = request.form.get("cultural_background", "").split(",")
    cultural_background = [c.strip() for c in cultural_background if c.strip()]
    
    is_freshman = request.form.get("is_international_freshman") == "1"
    display_name = request.form.get("display_name", "").strip()[:50]
    
    # Build profile dict
    profile_dict = {
        "display_name": display_name,
        "is_international_freshman": is_freshman,
        "preferred_language": languages[0] if languages else "",
        "primary_challenge": support_topics,
        "support_style": support_style,
        "support_topics": support_topics,
        "languages": languages,
        "cultural_background": cultural_background,
        "onboarding_complete": True
    }
    
    # Save to database
    save_profile_to_db(user_id, profile_dict)
    
    # Store in session for quick access
    session["display_name"] = display_name
    session["is_international_freshman"] = is_freshman
    session["preferred_language"] = languages[0] if languages else ""
    session["primary_challenge"] = support_topics
    session["support_style"] = support_style
    session["support_topics"] = support_topics
    session["languages"] = languages
    session["cultural_background"] = cultural_background
    session["onboarding_complete"] = True
    
    # Store user embedding for semantic matching
    store_user_embedding(user_id, profile_dict)
    
    return redirect(url_for("decision"))


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Profile setup page."""
    # If profile already exists, skip to issue page
    if request.method == "GET" and session.get("display_name"):
        return redirect(url_for("issue"))

    if request.method == "POST":

        session["display_name"] = request.form.get("display_name", "").strip()[:50]
        session["is_international_freshman"] = request.form.get("is_international_freshman") == "yes"
        session["preferred_language"] = request.form.get("preferred_language", "").strip()[:30]

        challenges = request.form.getlist("primary_challenge")
        session["primary_challenge"] = challenges[:2]

        support_style = request.form.get("support_style", "mixed")
        if support_style not in ["listening", "sharing", "mixed"]:
            support_style = "mixed"
        session["support_style"] = support_style

        session["followup_count"] = 0
        session["followup_history"] = []
        session["current_group"] = None

        # Store user embedding for semantic matching and save to DB
        user_id = session.get("user_id")
        if user_id:
            profile_dict = get_profile_dict()
            store_user_embedding(user_id, profile_dict)
            cache_user_profile(user_id, session.get("display_name"), profile_dict)
            save_profile_to_db(user_id, profile_dict)

        return redirect(url_for("issue"))


    return render_template("profile.html", username=session.get("username"))


@app.route("/issue", methods=["GET", "POST"])
@login_required
def issue():
    """Issue input page."""
    if not session.get("display_name"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        issue_text = request.form.get("issue_text", "").strip()
        if issue_text:
            session["current_issue"] = issue_text
            session["followup_count"] = 0
            return redirect(url_for("resources"))

    return render_template("issue.html", username=session.get("username"))


@app.route("/resources", methods=["GET", "POST"])
@login_required
def resources():
    """Resource page with AI suggestions and follow-up Q and A."""
    if not session.get("display_name"):
        return redirect(url_for("profile"))

    issue_text = session.get("current_issue", "")
    if not issue_text:
        return redirect(url_for("issue"))

    # Initialize follow-up history if not present
    if "followup_history" not in session:
        session["followup_history"] = []

    followup_count = session.get("followup_count", 0)
    followup_question = None
    followup_response = None
    limit_reached = followup_count >= 5

    if request.method == "POST" and not limit_reached:
        followup_question = request.form.get("followup_question", "").strip()
        if followup_question:
            session["followup_count"] = followup_count + 1
            followup_count = session["followup_count"]
            limit_reached = followup_count >= 5

            # Generate AI response
            profile_dict = get_profile_dict()
            history = session.get("followup_history", [])
            followup_response = ai_generate_followup_response(
                issue_text, followup_question, profile_dict, history
            )

            # Store in history
            history.append({
                "question": followup_question,
                "answer": followup_response
            })
            session["followup_history"] = history

    profile_dict = get_profile_dict()
    ai_result = ai_suggest_resources_and_options(issue_text, profile_dict, followup_count, followup_question)

    # Get semantically ranked groups
    user_id = session.get("user_id")
    semantic_groups = []
    if user_id:
        semantic_groups = get_recommended_groups_semantic(user_id, top_n=5)

    # Combine AI-recommended and semantic groups
    ai_groups = ai_result.get("recommended_groups", [])
    combined_groups = []
    seen = set()
    for g in semantic_groups + ai_groups:
        if g not in seen:
            combined_groups.append(g)
            seen.add(g)
    combined_groups = combined_groups[:5]

    return render_template(
        "resources.html",
        empathetic_message=ai_result.get("empathetic_message", ""),
        support_options=ai_result.get("support_options", []),
        asu_resources=ai_result.get("asu_resources", []),
        recommended_groups=combined_groups,
        disclaimer=ai_result.get("safe_disclaimer", ""),
        followup_count=followup_count,
        limit_reached=limit_reached,
        followup_question=followup_question,
        followup_response=followup_response,
        followup_history=session.get("followup_history", [])[:-1] if followup_question else session.get("followup_history", []),
        username=session.get("username")

    )


@app.route("/decision", methods=["GET"])
@login_required
def decision():
    """Decision page to join or create groups."""
    if not session.get("display_name"):
        return redirect(url_for("profile"))

    user_id = session.get("user_id")
    issue_text = session.get("current_issue", "")
    profile_dict = get_profile_dict()

    # Get semantic group recommendations if user has embedding
    semantic_groups = []
    if user_id:
        semantic_groups = get_recommended_groups_semantic(user_id, top_n=5)

    # Fallback to keyword-based recommendations
    ai_result = ai_suggest_resources_and_options(issue_text, profile_dict, 0)
    keyword_groups = ai_result.get("recommended_groups", [])

    # Combine: semantic first, then keyword, deduplicated
    recommended = []
    seen = set()
    for g in semantic_groups + keyword_groups:
        if g not in seen:
            recommended.append(g)
            seen.add(g)
    recommended = recommended[:5]

    # Get similar users for "People you may want to connect with"
    similar_users = []
    if user_id:
        similar_users = get_similar_users(user_id, top_n=5, threshold=0.3)

    available_groups = list(groups.keys())

    return render_template(
        "decision.html",
        recommended_groups=recommended,
        available_groups=available_groups,
        similar_users=similar_users,
        username=session.get("username"),
        display_name=session.get("display_name"),
        current_group=session.get("current_group")
    )


@app.route("/join_group", methods=["POST"])
@login_required
def join_group():
    """Join an existing group."""
    if not session.get("display_name"):
        return redirect(url_for("profile"))

    group_topic = request.form.get("group_topic", "").strip()
    if group_topic in groups:
        session["current_group"] = group_topic
        return redirect(url_for("chat"))

    return redirect(url_for("decision"))


@app.route("/create_group", methods=["POST"])
@login_required
def create_group():
    """Create a new group if no relevant active group exists."""
    if not session.get("display_name"):
        return redirect(url_for("profile"))

    new_topic = request.form.get("new_topic", "").strip()[:40]

    if not new_topic:
        return redirect(url_for("decision"))

    if check_profanity(new_topic):
        return redirect(url_for("decision"))

    relevant = find_relevant_group(new_topic)
    if relevant:
        session["current_group"] = relevant
        return redirect(url_for("chat"))

    groups[new_topic] = []
    store_group_embedding(new_topic)  # Store embedding for semantic matching
    session["current_group"] = new_topic
    return redirect(url_for("chat"))


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    """Topic room chat with moderation."""
    if not session.get("display_name"):
        return redirect(url_for("profile"))

    current_group = session.get("current_group")
    if not current_group or current_group not in groups:
        return redirect(url_for("decision"))

    warning = None
    distress_banner = False

    if request.method == "POST":
        message_text = request.form.get("message_text", "").strip()
        if message_text:
            moderation = ai_moderate_message(message_text)

            if not moderation["allowed"]:
                warning = moderation["user_message"]
            else:
                # Generate unique message ID
                msg_id = f"{session.get('user_id')}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                groups[current_group].append({
                    "id": msg_id,
                    "user_id": session.get("user_id"),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "display_name": session.get("display_name", "Anonymous"),
                    "text": moderation["user_message"]
                })
                if moderation["reason"] == "severe_distress":
                    distress_banner = True

    messages = groups.get(current_group, [])[-50:]

    return render_template(
        "chat.html",
        group_topic=current_group,
        messages=messages,
        warning=warning,
        distress_banner=distress_banner,
        username=session.get("username"),
        current_user_id=session.get("user_id")
    )



@app.route("/api/messages", methods=["GET"])
@login_required
def api_messages():
    """API endpoint for polling chat messages."""
    current_group = session.get("current_group")
    if not current_group or current_group not in groups:
        return jsonify({"messages": [], "error": "No active group"})

    messages = groups.get(current_group, [])[-50:]
    return jsonify({"messages": messages})


def format_human_timestamp(timestamp_str):
    """Convert timestamp to human-readable format."""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - dt

        if diff.seconds < 60:
            return "Just now"
        elif diff.seconds < 3600:
            mins = diff.seconds // 60
            return f"{mins} min ago"
        elif diff.days == 0:
            return dt.strftime("%I:%M %p")
        elif diff.days == 1:
            return "Yesterday " + dt.strftime("%I:%M %p")
        else:
            return dt.strftime("%b %d, %I:%M %p")
    except Exception:
        return timestamp_str


@app.route("/leave_group", methods=["POST"])
@login_required
def leave_group():
    """Leave current group and add system message."""
    current_group = session.get("current_group")
    display_name = session.get("display_name", "Someone")

    if current_group and current_group in groups:
        groups[current_group].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "display_name": "System",
            "text": f"{display_name} has left the group.",
            "is_system": True
        })

    session["current_group"] = None
    return redirect(url_for("decision"))


@app.route("/api/message/edit", methods=["POST"])
@login_required
def edit_message():
    """Edit a user's own message."""
    data = request.get_json()
    msg_id = data.get("message_id")
    new_text = data.get("text", "").strip()
    
    if not msg_id or not new_text:
        return jsonify({"success": False, "error": "Missing message ID or text"})
    
    current_group = session.get("current_group")
    user_id = session.get("user_id")
    
    if not current_group or current_group not in groups:
        return jsonify({"success": False, "error": "No active group"})
    
    # Find and edit the message
    for msg in groups[current_group]:
        if msg.get("id") == msg_id and msg.get("user_id") == user_id:
            # Moderate the new text
            moderation = ai_moderate_message(new_text)
            if not moderation["allowed"]:
                return jsonify({"success": False, "error": moderation["user_message"]})
            
            msg["text"] = moderation["user_message"]
            msg["edited"] = True
            return jsonify({"success": True, "text": msg["text"]})
    
    return jsonify({"success": False, "error": "Message not found or not authorized"})


@app.route("/api/message/delete", methods=["POST"])
@login_required
def delete_message():
    """Delete a user's own message."""
    data = request.get_json()
    msg_id = data.get("message_id")
    
    if not msg_id:
        return jsonify({"success": False, "error": "Missing message ID"})
    
    current_group = session.get("current_group")
    user_id = session.get("user_id")
    
    if not current_group or current_group not in groups:
        return jsonify({"success": False, "error": "No active group"})
    
    # Find and delete the message
    for i, msg in enumerate(groups[current_group]):
        if msg.get("id") == msg_id and msg.get("user_id") == user_id:
            groups[current_group].pop(i)
            return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Message not found or not authorized"})


# -----------------------------------------------------------------------------
# Peer Connection Routes
# -----------------------------------------------------------------------------

def get_profile_summary(profile_dict):
    """Generate a short profile summary for display."""
    parts = []
    
    if profile_dict.get("is_international_freshman"):
        parts.append("International freshman")
    
    challenges = profile_dict.get("primary_challenge", [])
    if challenges:
        parts.append(f"Facing: {', '.join(challenges[:2])}")
    
    language = profile_dict.get("preferred_language")
    if language:
        parts.append(f"Speaks: {language}")
    
    return " | ".join(parts) if parts else "ASU Student"


def cache_user_profile(user_id, display_name, profile_dict):
    """Cache user profile for peer display."""
    user_profiles[user_id] = {
        "display_name": display_name,
        "profile_summary": get_profile_summary(profile_dict)
    }


def get_pending_requests_for_user(user_id):
    """Get all pending connection requests for a user."""
    return pending_requests.get(user_id, [])


def add_connection_request(sender_id, sender_display_name, recipient_id, message):
    """Add a connection request to pending requests."""
    if recipient_id not in pending_requests:
        pending_requests[recipient_id] = []
    
    # Check if request already exists
    for req in pending_requests[recipient_id]:
        if req["sender_id"] == sender_id:
            return False  # Already sent
    
    pending_requests[recipient_id].append({
        "sender_id": sender_id,
        "sender_display_name": sender_display_name,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True


def remove_connection_request(recipient_id, sender_id):
    """Remove a connection request."""
    if recipient_id in pending_requests:
        pending_requests[recipient_id] = [
            req for req in pending_requests[recipient_id]
            if req["sender_id"] != sender_id
        ]


@app.route("/people", methods=["GET"])
@login_required
def people():
    """Show recommended peers based on semantic matching."""
    if not session.get("display_name"):
        return redirect(url_for("onboarding"))
    
    user_id = session.get("user_id")
    filter_challenge = request.args.get("filter", "")
    
    # Get all profiles from database
    db = get_db()
    all_profiles = db.execute('''
        SELECT p.*, u.username FROM profiles p 
        JOIN users u ON p.user_id = u.id 
        WHERE p.user_id != ? AND p.display_name IS NOT NULL AND p.display_name != ''
    ''', (user_id,)).fetchall()
    
    peers = []
    for row in all_profiles:
        challenges = row['primary_challenge'] or ''
        support_topics = row['support_topics'] or ''
        all_challenges = challenges + ',' + support_topics
        
        # Apply filter if specified
        if filter_challenge:
            filter_lower = filter_challenge.lower()
            all_challenges_lower = all_challenges.lower()
            if filter_lower not in all_challenges_lower:
                # Check for category matches
                if filter_lower == 'homesickness' and 'homesickness' not in all_challenges_lower:
                    continue
                elif filter_lower == 'academic' and 'academic' not in all_challenges_lower:
                    continue
                elif filter_lower == 'social' and 'loneliness' not in all_challenges_lower and 'relationships' not in all_challenges_lower:
                    continue
                elif filter_lower == 'cultural' and 'culture' not in all_challenges_lower:
                    continue
                elif filter_lower == 'language' and 'language' not in all_challenges_lower:
                    continue
        
        peers.append({
            "user_id": row['user_id'],
            "display_name": row['display_name'] or 'Anonymous',
            "is_international_freshman": bool(row['is_international_freshman']),
            "preferred_language": row['preferred_language'] or '',
            "primary_challenge": row['primary_challenge'] or '',
            "support_style": row['support_style'] or 'mixed'
        })
    
    # Also add from in-memory cache for real-time peers
    if user_id:
        similar = get_similar_users(user_id, top_n=10, threshold=0.2)
        for peer_id, score in similar:
            peer_profile = user_profiles.get(peer_id)
            if peer_profile and not any(p['user_id'] == peer_id for p in peers):
                peers.append({
                    "user_id": peer_id,
                    "display_name": peer_profile.get("display_name", "Anonymous"),
                    "is_international_freshman": peer_profile.get("is_international_freshman", False),
                    "preferred_language": peer_profile.get("preferred_language", ""),
                    "primary_challenge": ",".join(peer_profile.get("primary_challenge", [])),
                    "support_style": peer_profile.get("support_style", "mixed")
                })
    
    # Get pending requests for current user
    incoming_requests = get_pending_requests_for_user(user_id)
    
    return render_template(
        "people.html",
        peers=peers,
        filter=filter_challenge,
        incoming_requests=incoming_requests,
        username=session.get("username")
    )


@app.route("/connect", methods=["POST"])
@login_required
def connect():
    """Send a connection request to another user."""
    if not session.get("display_name"):
        return jsonify({"success": False, "error": "Profile required"}), 400
    
    sender_id = session.get("user_id")
    sender_display_name = session.get("display_name")
    recipient_id = request.form.get("recipient_id")
    message = request.form.get("message", "").strip()[:200]
    
    if not recipient_id:
        return jsonify({"success": False, "error": "Recipient required"}), 400
    
    try:
        recipient_id = int(recipient_id)
    except ValueError:
        return jsonify({"success": False, "error": "Invalid recipient"}), 400
    
    if sender_id == recipient_id:
        return jsonify({"success": False, "error": "Cannot connect with yourself"}), 400
    
    # Moderate message if provided
    distress_detected = False
    if message:
        moderation = ai_moderate_message(message)
        if not moderation["allowed"]:
            return jsonify({
                "success": False,
                "error": moderation["user_message"]
            }), 400
        if moderation["reason"] == "severe_distress":
            distress_detected = True
    
    # Add the request
    success = add_connection_request(sender_id, sender_display_name, recipient_id, message)
    
    if success:
        return jsonify({
            "success": True,
            "message": "Connection request sent",
            "distress_detected": distress_detected
        })
    else:
        return jsonify({
            "success": False,
            "error": "Request already sent"
        }), 400


@app.route("/connect/accept", methods=["POST"])
@login_required
def connect_accept():
    """Accept a connection request."""
    user_id = session.get("user_id")
    sender_id = request.form.get("sender_id")
    action = request.form.get("action", "group")  # "group" or "message"
    
    if not sender_id:
        flash("Sender required", "error")
        return redirect(url_for("people"))
    
    try:
        sender_id = int(sender_id)
    except ValueError:
        flash("Invalid sender", "error")
        return redirect(url_for("people"))
    
    # Find the request
    requests_list = get_pending_requests_for_user(user_id)
    request_found = None
    for req in requests_list:
        if req["sender_id"] == sender_id:
            request_found = req
            break
    
    if not request_found:
        flash("Request not found", "error")
        return redirect(url_for("people"))
    
    # Remove the request
    remove_connection_request(user_id, sender_id)
    
    flash(f"Connection with {request_found['sender_display_name']} accepted!", "success")
    return redirect(url_for("people"))


@app.route("/connect/ignore", methods=["POST"])
@login_required
def connect_ignore():
    """Ignore/remove a connection request."""
    user_id = session.get("user_id")
    sender_id = request.form.get("sender_id")
    
    if not sender_id:
        flash("Sender required", "error")
        return redirect(url_for("people"))
    
    try:
        sender_id = int(sender_id)
    except ValueError:
        flash("Invalid sender", "error")
        return redirect(url_for("people"))
    
    remove_connection_request(user_id, sender_id)
    
    flash("Request removed", "info")
    return redirect(url_for("people"))


# -----------------------------------------------------------------------------
# Run Application
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    init_group_embeddings()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
