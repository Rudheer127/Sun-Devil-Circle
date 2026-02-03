"""Quick test script for the Flask app routes."""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_routes():
    print("Testing Sun Devil Circle Routes...")
    print("=" * 50)
    
    # Test / (should redirect to login)
    r = requests.get(f"{BASE_URL}/", allow_redirects=False)
    print(f"GET / -> Status: {r.status_code}, Redirect: {r.headers.get('Location', 'N/A')}")
    assert r.status_code == 302, "Expected redirect"
    assert "/login" in r.headers.get("Location", ""), "Expected redirect to /login"
    
    # Test /login (should return 200)
    r = requests.get(f"{BASE_URL}/login")
    print(f"GET /login -> Status: {r.status_code}")
    assert r.status_code == 200, "Expected 200"
    assert "Log In" in r.text or "Login" in r.text, "Expected login form"
    
    # Test /signup (should return 200)
    r = requests.get(f"{BASE_URL}/signup")
    print(f"GET /signup -> Status: {r.status_code}")
    assert r.status_code == 200, "Expected 200"
    assert "Sign Up" in r.text or "Signup" in r.text, "Expected signup form"
    
    # Test signup flow
    session = requests.Session()
    signup_data = {
        "username": "testuser_check",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    r = session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    print(f"POST /signup -> Status: {r.status_code}, Redirect: {r.headers.get('Location', 'N/A')}")
    
    # Follow redirect to profile
    if r.status_code == 302:
        r = session.get(f"{BASE_URL}/")
        print(f"GET / (logged in) -> Status: {r.status_code}")
        assert r.status_code == 200, "Expected 200"
        assert "Profile" in r.text or "profile" in r.text or "Welcome" in r.text, "Expected profile page"
    
    # Test protected routes without login
    r2 = requests.get(f"{BASE_URL}/issue", allow_redirects=False)
    print(f"GET /issue (no auth) -> Status: {r2.status_code}, Redirect: {r2.headers.get('Location', 'N/A')}")
    assert r2.status_code == 302, "Expected redirect to login"
    
    print("=" * 50)
    print("All route tests passed!")

if __name__ == "__main__":
    test_routes()
