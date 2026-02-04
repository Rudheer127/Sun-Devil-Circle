"""Test all routes and integration points."""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_all_routes():
    print("Testing Sun Devil Circles Routes...")
    print("=" * 60)

    # Test login/signup
    print("\n[Auth Tests]")
    r = requests.get(f"{BASE_URL}/", allow_redirects=False)
    print(f"GET / (unauthenticated) -> {r.status_code} (expected 302)")
    assert r.status_code == 302

    r = requests.get(f"{BASE_URL}/login")
    print(f"GET /login -> {r.status_code} (expected 200)")
    assert r.status_code == 200

    r = requests.get(f"{BASE_URL}/signup")
    print(f"GET /signup -> {r.status_code} (expected 200)")
    assert r.status_code == 200

    # Create session and signup
    print("\n[Session Flow Tests]")
    session = requests.Session()
    signup_data = {
        "username": "integration_test_user",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    r = session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    print(f"POST /signup -> {r.status_code}")

    # Access profile
    r = session.get(f"{BASE_URL}/")
    print(f"GET / (logged in) -> {r.status_code}")
    assert r.status_code == 200 or "profile" in r.text.lower() or "welcome" in r.text.lower()

    # Submit profile
    profile_data = {
        "display_name": "Test User",
        "gender": "male",
        "preferred_language": "Spanish",
        "primary_challenge": ["academic", "social"],
        "support_style": "mixed"
    }
    r = session.post(f"{BASE_URL}/", data=profile_data, allow_redirects=False)
    print(f"POST / (profile submit) -> {r.status_code}")
    assert r.status_code == 302

    # Submit issue
    r = session.get(f"{BASE_URL}/issue")
    print(f"GET /issue -> {r.status_code}")
    assert r.status_code == 200

    issue_data = {"issue_text": "I am feeling stressed about exams and missing home"}
    r = session.post(f"{BASE_URL}/issue", data=issue_data, allow_redirects=False)
    print(f"POST /issue -> {r.status_code}")
    assert r.status_code == 302

    # Resources page
    print("\n[Resources Tests]")
    r = session.get(f"{BASE_URL}/resources")
    print(f"GET /resources -> {r.status_code}")
    assert r.status_code == 200
    assert "Support Options" in r.text
    assert "Recommended Peer Groups" in r.text

    # Follow-up questions
    for i in range(3):
        followup_data = {"followup_question": f"Test question {i+1}"}
        r = session.post(f"{BASE_URL}/resources", data=followup_data)
        print(f"POST /resources (followup {i+1}) -> {r.status_code}")
        assert r.status_code == 200

    # Decision page
    print("\n[Decision/Groups Tests]")
    r = session.get(f"{BASE_URL}/decision")
    print(f"GET /decision -> {r.status_code}")
    assert r.status_code == 200
    assert "Recommended for You" in r.text or "Available Groups" in r.text

    # People page
    print("\n[People Tests]")
    r = session.get(f"{BASE_URL}/people")
    print(f"GET /people -> {r.status_code}")
    assert r.status_code == 200

    # Join group
    join_data = {"group_topic": "Academic Pressure"}
    r = session.post(f"{BASE_URL}/join_group", data=join_data, allow_redirects=False)
    print(f"POST /join_group -> {r.status_code}")
    assert r.status_code == 302

    # Chat page
    r = session.get(f"{BASE_URL}/chat")
    print(f"GET /chat -> {r.status_code}")
    assert r.status_code == 200
    assert "Academic Pressure" in r.text

    # Send message
    msg_data = {"message_text": "Hello everyone!"}
    r = session.post(f"{BASE_URL}/chat", data=msg_data)
    print(f"POST /chat (message) -> {r.status_code}")
    assert r.status_code == 200

    # API messages endpoint
    r = session.get(f"{BASE_URL}/api/messages")
    print(f"GET /api/messages -> {r.status_code}")
    assert r.status_code == 200
    data = r.json()
    assert "messages" in data
    print(f"  Messages count: {len(data['messages'])}")

    # Leave group
    r = session.post(f"{BASE_URL}/leave_group", allow_redirects=False)
    print(f"POST /leave_group -> {r.status_code}")
    assert r.status_code == 302

    # Connection request
    print("\n[Connection Tests]")
    connect_data = {"recipient_id": "999", "message": "Hi!"}
    r = session.post(f"{BASE_URL}/connect", data=connect_data)
    print(f"POST /connect (invalid recipient) -> {r.status_code}")
    # Should return error for non-existent user

    # Logout
    r = session.get(f"{BASE_URL}/logout", allow_redirects=False)
    print(f"GET /logout -> {r.status_code}")
    assert r.status_code == 302

    print("\n" + "=" * 60)
    print("All integration tests passed!")

if __name__ == "__main__":
    test_all_routes()
