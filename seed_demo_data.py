"""
Seed script to create demo data for Sun Devil Circles.
Creates 20 test profiles, groups, messages, and connection requests.
"""
import sqlite3
import random
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DATABASE = "auth.db"

# Test user data with diverse backgrounds
TEST_USERS = [
    {
        "username": "maya_patel",
        "password": "demo123",
        "display_name": "Maya Patel",
        "gender": "female",
        "cultural_background": "South Asia",
        "languages": "English,Hindi,Gujarati",
        "preferred_language": "English",
        "support_topics": "anxiety,academic_problems,homesickness",
        "private_topics": "anxiety",
        "support_style": "mixed",
        "graduation_year": "2027",
        "degree_program": "bachelors"
    },
    {
        "username": "wei_chen",
        "password": "demo123",
        "display_name": "Wei Chen",
        "gender": "male",
        "cultural_background": "East Asia",
        "languages": "English,Mandarin",
        "preferred_language": "Mandarin",
        "support_topics": "academic_problems,loneliness_isolation,culture_shock",
        "private_topics": "",
        "support_style": "listening",
        "graduation_year": "2026",
        "degree_program": "masters"
    },
    {
        "username": "sarah_johnson",
        "password": "demo123",
        "display_name": "Sarah Johnson",
        "gender": "female",
        "cultural_background": "North America",
        "languages": "English,Spanish",
        "preferred_language": "English",
        "support_topics": "depression,relationship_issues,family_pressure",
        "private_topics": "depression",
        "support_style": "sharing",
        "graduation_year": "2027",
        "degree_program": "bachelors"
    },
    {
        "username": "ahmed_hassan",
        "password": "demo123",
        "display_name": "Ahmed Hassan",
        "gender": "male",
        "cultural_background": "Middle East",
        "languages": "English,Arabic",
        "preferred_language": "Arabic",
        "support_topics": "discrimination_bias,identity_concerns,loneliness_isolation",
        "private_topics": "identity_concerns",
        "support_style": "mixed",
        "graduation_year": "2028",
        "degree_program": "bachelors"
    },
    {
        "username": "kim_nguyen",
        "password": "demo123",
        "display_name": "Kim Nguyen",
        "gender": "non-binary",
        "cultural_background": "Southeast Asia",
        "languages": "English,Vietnamese",
        "preferred_language": "English",
        "support_topics": "identity_concerns,loneliness_isolation,self_esteem",
        "private_topics": "",
        "support_style": "listening",
        "graduation_year": "2026",
        "degree_program": "bachelors"
    },
    {
        "username": "priya_sharma",
        "password": "demo123",
        "display_name": "Priya Sharma",
        "gender": "female",
        "cultural_background": "South Asia",
        "languages": "English,Hindi,Tamil",
        "preferred_language": "English",
        "support_topics": "family_pressure,academic_problems,career_concerns",
        "private_topics": "family_pressure",
        "support_style": "advice",
        "graduation_year": "2027",
        "degree_program": "masters"
    },
    {
        "username": "james_wilson",
        "password": "demo123",
        "display_name": "James Wilson",
        "gender": "male",
        "cultural_background": "North America",
        "languages": "English",
        "preferred_language": "English",
        "support_topics": "financial_stress,academic_problems,time_management",
        "private_topics": "financial_stress",
        "support_style": "mixed",
        "graduation_year": "2026",
        "degree_program": "bachelors"
    },
    {
        "username": "yuki_tanaka",
        "password": "demo123",
        "display_name": "Yuki Tanaka",
        "gender": "female",
        "cultural_background": "East Asia",
        "languages": "English,Japanese",
        "preferred_language": "English",
        "support_topics": "culture_shock,social_anxiety,homesickness",
        "private_topics": "social_anxiety",
        "support_style": "listening",
        "graduation_year": "2028",
        "degree_program": "doctoral"
    },
    {
        "username": "alex_rodrigues",
        "password": "demo123",
        "display_name": "Alex Rodrigues",
        "gender": "male",
        "cultural_background": "Latin America",
        "languages": "English,Spanish,Portuguese",
        "preferred_language": "Spanish",
        "support_topics": "homesickness,loneliness_isolation,academic_problems",
        "private_topics": "",
        "support_style": "sharing",
        "graduation_year": "2027",
        "degree_program": "bachelors"
    },
    {
        "username": "fatima_ali",
        "password": "demo123",
        "display_name": "Fatima Ali",
        "gender": "female",
        "cultural_background": "Middle East",
        "languages": "English,Arabic,Urdu",
        "preferred_language": "English",
        "support_topics": "discrimination_bias,identity_concerns,family_pressure",
        "private_topics": "identity_concerns",
        "support_style": "mixed",
        "graduation_year": "2026",
        "degree_program": "masters"
    },
    {
        "username": "david_kim",
        "password": "demo123",
        "display_name": "David Kim",
        "gender": "male",
        "cultural_background": "East Asia",
        "languages": "English,Korean",
        "preferred_language": "English",
        "support_topics": "career_concerns,academic_problems,time_management",
        "private_topics": "",
        "support_style": "advice",
        "graduation_year": "2027",
        "degree_program": "masters"
    },
    {
        "username": "nina_okoye",
        "password": "demo123",
        "display_name": "Nina Okoye",
        "gender": "female",
        "cultural_background": "Africa",
        "languages": "English,Igbo",
        "preferred_language": "English",
        "support_topics": "culture_shock,discrimination_bias,loneliness_isolation",
        "private_topics": "discrimination_bias",
        "support_style": "mixed",
        "graduation_year": "2028",
        "degree_program": "bachelors"
    },
    {
        "username": "carlos_mendez",
        "password": "demo123",
        "display_name": "Carlos Mendez",
        "gender": "male",
        "cultural_background": "Latin America",
        "languages": "English,Spanish",
        "preferred_language": "Spanish",
        "support_topics": "financial_stress,homesickness,family_pressure",
        "private_topics": "financial_stress",
        "support_style": "listening",
        "graduation_year": "2027",
        "degree_program": "bachelors"
    },
    {
        "username": "emma_larsson",
        "password": "demo123",
        "display_name": "Emma Larsson",
        "gender": "female",
        "cultural_background": "Europe",
        "languages": "English,Swedish,German",
        "preferred_language": "English",
        "support_topics": "anxiety,relationship_issues,self_esteem",
        "private_topics": "relationship_issues",
        "support_style": "sharing",
        "graduation_year": "2026",
        "degree_program": "doctoral"
    },
    {
        "username": "raj_kumar",
        "password": "demo123",
        "display_name": "Raj Kumar",
        "gender": "male",
        "cultural_background": "South Asia",
        "languages": "English,Hindi,Punjabi",
        "preferred_language": "English",
        "support_topics": "academic_problems,career_concerns,family_pressure",
        "private_topics": "",
        "support_style": "advice",
        "graduation_year": "2027",
        "degree_program": "masters"
    },
    {
        "username": "lily_zhang",
        "password": "demo123",
        "display_name": "Lily Zhang",
        "gender": "female",
        "cultural_background": "East Asia",
        "languages": "English,Mandarin,Cantonese",
        "preferred_language": "English",
        "support_topics": "anxiety,homesickness,culture_shock",
        "private_topics": "anxiety",
        "support_style": "mixed",
        "graduation_year": "2028",
        "degree_program": "bachelors"
    },
    {
        "username": "omar_hassan",
        "password": "demo123",
        "display_name": "Omar Hassan",
        "gender": "male",
        "cultural_background": "Africa",
        "languages": "English,Arabic,Swahili",
        "preferred_language": "English",
        "support_topics": "loneliness_isolation,academic_problems,career_concerns",
        "private_topics": "",
        "support_style": "mixed",
        "graduation_year": "2027",
        "degree_program": "bachelors"
    },
    {
        "username": "sofia_garcia",
        "password": "demo123",
        "display_name": "Sofia Garcia",
        "gender": "female",
        "cultural_background": "Latin America",
        "languages": "English,Spanish",
        "preferred_language": "Spanish",
        "support_topics": "depression,family_pressure,relationship_issues",
        "private_topics": "depression",
        "support_style": "listening",
        "graduation_year": "2026",
        "degree_program": "bachelors"
    },
    {
        "username": "jason_lee",
        "password": "demo123",
        "display_name": "Jason Lee",
        "gender": "male",
        "cultural_background": "East Asia",
        "languages": "English,Korean,Japanese",
        "preferred_language": "English",
        "support_topics": "social_anxiety,identity_concerns,self_esteem",
        "private_topics": "identity_concerns",
        "support_style": "sharing",
        "graduation_year": "2027",
        "degree_program": "bachelors"
    },
    {
        "username": "aisha_mohammed",
        "password": "demo123",
        "display_name": "Aisha Mohammed",
        "gender": "female",
        "cultural_background": "Middle East",
        "languages": "English,Arabic,French",
        "preferred_language": "English",
        "support_topics": "discrimination_bias,culture_shock,family_pressure",
        "private_topics": "",
        "support_style": "mixed",
        "graduation_year": "2028",
        "degree_program": "masters"
    }
]

# User-created groups
USER_GROUPS = [
    {
        "name": "ASU Foodies 🍜",
        "description": "Share your favorite food spots and recipes from home!",
        "topic": "culture_shock",
        "created_by_index": 1  # Wei Chen
    },
    {
        "name": "Grad Student Support 📚",
        "description": "A space for graduate students to share challenges and tips",
        "topic": "academic_problems",
        "created_by_index": 5  # Priya Sharma
    },
    {
        "name": "South Asian Connect 🌸",
        "description": "For students from South Asian backgrounds to connect and share",
        "topic": "homesickness",
        "created_by_index": 0  # Maya Patel
    },
    {
        "name": "First-Gen Students 🌟",
        "description": "Support for first-generation college students",
        "topic": "family_pressure",
        "created_by_index": 6  # James Wilson
    },
    {
        "name": "International Coffee Hour ☕",
        "description": "Virtual coffee chats to make new friends",
        "topic": "loneliness_isolation",
        "created_by_index": 8  # Alex Rodrigues
    }
]

# Sample messages for groups
SAMPLE_MESSAGES = [
    ("Hey everyone! New here. Anyone else struggling with the time zone difference?", 0),
    ("Welcome! Yes, it's tough. I try to schedule calls with family on weekends.", 1),
    ("The dining hall food is so different from home. Missing my mom's cooking!", 2),
    ("Same here! I found a great restaurant downtown that has authentic food.", 3),
    ("Does anyone else feel overwhelmed by the workload this semester?", 4),
    ("You're not alone! Office hours have been really helpful for me.", 5),
    ("Just wanted to say this group has been so supportive. Thank you all! 💜", 6),
    ("We're all in this together! Don't hesitate to reach out.", 7),
    ("Anyone taking CSE classes? Looking for study buddies!", 8),
    ("I'm in CSE 340! Let's connect.", 9),
    ("The weather here is so different. Any tips for dealing with the heat?", 10),
    ("Hydrate constantly! And the library is air-conditioned 😅", 11),
    ("Feeling homesick today. It's a festival back home and I miss my family.", 12),
    ("Virtual hugs! 🤗 We could organize a small celebration here too?", 13),
    ("That's a great idea! Count me in.", 14),
]


def seed_database():
    """Seed the database with test data."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("🌱 Seeding database with demo data...")
    
    # Create users and profiles
    user_ids = []
    for i, user in enumerate(TEST_USERS):
        # Insert user
        cursor.execute('''
            INSERT INTO users (username, password_hash, created_at)
            VALUES (?, ?, ?)
        ''', (user["username"], generate_password_hash(user["password"]), datetime.now().isoformat()))
        user_id = cursor.lastrowid
        user_ids.append(user_id)
        
        # Insert profile
        cursor.execute('''
            INSERT INTO profiles 
            (user_id, display_name, gender, preferred_language, primary_challenge, 
             support_style, support_topics, private_topics, languages, 
             cultural_background, onboarding_complete, graduation_year, degree_program)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            user["display_name"],
            user["gender"],
            user["preferred_language"],
            user["support_topics"],
            user["support_style"],
            user["support_topics"],
            user["private_topics"],
            user["languages"],
            user["cultural_background"],
            1,  # onboarding_complete
            user["graduation_year"],
            user["degree_program"]
        ))
        print(f"  ✅ Created user: {user['display_name']}")
    
    conn.commit()
    print(f"\n📊 Created {len(user_ids)} users and profiles")
    
    conn.close()
    return user_ids


def seed_in_memory_data():
    """Seed in-memory data by making requests to the running Flask app."""
    import requests
    
    BASE_URL = "http://127.0.0.1:5000"
    sessions = []
    
    print("\n🔐 Logging in users and populating in-memory data...")
    
    # Login each user to populate their session/in-memory data
    for user in TEST_USERS:
        session = requests.Session()
        r = session.post(f"{BASE_URL}/login", data={
            "username": user["username"],
            "password": user["password"]
        }, allow_redirects=False)
        if r.status_code == 302:
            print(f"  ✅ Logged in: {user['display_name']}")
            sessions.append((session, user))
        else:
            print(f"  ❌ Failed to login: {user['username']}")
    
    # Create user-generated groups
    print("\n🏠 Creating user-generated groups...")
    created_groups = []
    for group in USER_GROUPS:
        session, user = sessions[group["created_by_index"]]
        r = session.post(f"{BASE_URL}/groups/create", data={
            "name": group["name"],
            "description": group["description"],
            "topic": group["topic"],
            "visibility": "public"
        }, allow_redirects=False)
        if r.status_code == 302:
            print(f"  ✅ Created group: {group['name']} by {user['display_name']}")
            created_groups.append(group["name"])
        else:
            print(f"  ❌ Failed to create group: {group['name']}")
    
    # Join users to groups (preset and user-created)
    print("\n👥 Joining users to groups...")
    preset_groups = [
        "Anxiety & Stress Support",
        "International Student Life",
        "LGBTQ+ at ASU",
        "Academic Pressure",
        "First-Year Experience"
    ]
    
    for i, (session, user) in enumerate(sessions):
        # Join a preset group based on user index
        group_to_join = preset_groups[i % len(preset_groups)]
        r = session.post(f"{BASE_URL}/join_group", data={
            "group_topic": group_to_join
        }, allow_redirects=False)
        
        # Also join a user-created group if available
        if created_groups and i < len(created_groups):
            r2 = session.post(f"{BASE_URL}/groups/{created_groups[i % len(created_groups)]}/join", 
                             allow_redirects=False)
    
    # Send messages to groups
    print("\n💬 Sending messages to groups...")
    for i, (message, sender_idx) in enumerate(SAMPLE_MESSAGES):
        if sender_idx < len(sessions):
            session, user = sessions[sender_idx]
            # First make sure user is in a group by joining
            group = preset_groups[sender_idx % len(preset_groups)]
            session.post(f"{BASE_URL}/join_group", data={"group_topic": group}, allow_redirects=False)
            # Then send message
            r = session.post(f"{BASE_URL}/chat", data={"message_text": message})
            if r.status_code == 200:
                print(f"  💬 {user['display_name'][:10]}...: '{message[:40]}...'")
    
    # Create connection requests
    print("\n🤝 Creating connection requests...")
    connection_pairs = [
        (0, 5, "Hi! I saw we're both from South Asia. Would love to connect!"),
        (1, 7, "Hey Yuki! Fellow East Asian student here. Let's chat!"),
        (2, 13, "Hi Emma! Would love to connect about student life."),
        (3, 9, "Salaam! Noticed we have similar backgrounds."),
        (4, 18, "Hey! Saw your profile, would love to connect."),
        (8, 12, "Hola Carlos! Fellow Latin American here! 🌎"),
        (10, 14, "Hi Raj! Would love to connect about grad school life."),
        (11, 16, "Hey Omar! Let's connect!"),
    ]
    
    accepted_pairs = [(0, 5), (1, 7), (8, 12)]  # These will be accepted
    
    for sender_idx, recipient_idx, message in connection_pairs:
        if sender_idx < len(sessions) and recipient_idx < len(sessions):
            session, sender = sessions[sender_idx]
            recipient = TEST_USERS[recipient_idx]
            
            # Get recipient user_id from database
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (recipient["username"],))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                recipient_id = row[0]
                r = session.post(f"{BASE_URL}/connect", data={
                    "recipient_id": recipient_id,
                    "message": message
                })
                status = "SENT" if r.status_code == 200 else "FAILED"
                print(f"  📨 {sender['display_name'][:12]} → {recipient['display_name'][:12]}: {status}")
                
                # Accept some requests
                if (sender_idx, recipient_idx) in accepted_pairs:
                    recipient_session, _ = sessions[recipient_idx]
                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM users WHERE username = ?", (sender["username"],))
                    sender_row = cursor.fetchone()
                    conn.close()
                    if sender_row:
                        r2 = recipient_session.post(f"{BASE_URL}/connect/accept", data={
                            "sender_id": sender_row[0]
                        })
                        if r2.status_code == 200:
                            print(f"    ✅ {recipient['display_name'][:12]} ACCEPTED")
    
    print("\n✨ Demo data seeding complete!")
    print("\n📋 Login credentials for demo:")
    print("-" * 50)
    for user in TEST_USERS[:5]:
        print(f"  Username: {user['username']:<20} Password: {user['password']}")
    print("  ... and 15 more users with password 'demo123'")
    print("-" * 50)
    print("\n🎬 Ready for demo video!")


if __name__ == "__main__":
    user_ids = seed_database()
    seed_in_memory_data()
