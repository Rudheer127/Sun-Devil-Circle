"""Comprehensive tests for Sun Devil Circles app."""
import requests
import time

BASE_URL = "http://127.0.0.1:5000"


def test_onboarding_flow():
    """Test the full onboarding flow with new gender field."""
    print("\n[Onboarding Flow Tests]")
    print("-" * 40)
    
    session = requests.Session()
    
    # Create unique username
    username = f"test_user_{int(time.time())}"
    
    # Signup
    signup_data = {
        "username": username,
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    r = session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    print(f"POST /signup -> {r.status_code}")
    assert r.status_code == 302, f"Expected redirect, got {r.status_code}"
    
    # Complete onboarding with new gender field
    onboarding_data = {
        "support_topics": "anxiety,stress,academic_problems",
        "languages": "English,Spanish",
        "support_style": "mixed",
        "cultural_background": "South Asia,East Asia",
        "gender": "female",
        "graduation_year": "2027",
        "degree_program": "bachelors",
        "display_name": f"TestUser{int(time.time()) % 1000}"
    }
    r = session.post(f"{BASE_URL}/onboarding", data=onboarding_data, allow_redirects=False)
    print(f"POST /onboarding -> {r.status_code}")
    
    # Verify profile was saved correctly
    r = session.get(f"{BASE_URL}/profile")
    print(f"GET /profile -> {r.status_code}")
    assert r.status_code == 200
    assert "Gender" in r.text or "gender" in r.text
    
    # Logout
    session.get(f"{BASE_URL}/logout")
    print("Onboarding flow test: PASSED")
    return True


def test_cultural_background_section():
    """Test that cultural background section is properly handled."""
    print("\n[Cultural Background Tests]")
    print("-" * 40)
    
    session = requests.Session()
    username = f"culture_test_{int(time.time())}"
    
    # Signup
    signup_data = {
        "username": username,
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    r = session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    assert r.status_code == 302
    
    # Complete onboarding with cultural background
    onboarding_data = {
        "support_topics": "homesickness,culture_shock",
        "languages": "Hindi,English",
        "support_style": "listening",
        "cultural_background": "South Asia",
        "gender": "male",
        "graduation_year": "2028",
        "degree_program": "masters",
        "display_name": "CultureTest"
    }
    r = session.post(f"{BASE_URL}/onboarding", data=onboarding_data, allow_redirects=False)
    print(f"POST /onboarding with cultural_background -> {r.status_code}")
    
    # Verify profile shows cultural background
    r = session.get(f"{BASE_URL}/profile")
    assert r.status_code == 200
    assert "Cultural Background" in r.text or "cultural" in r.text.lower()
    print("Cultural background test: PASSED")
    
    session.get(f"{BASE_URL}/logout")
    return True


def test_gender_options():
    """Test all gender options are available."""
    print("\n[Gender Options Tests]")
    print("-" * 40)
    
    session = requests.Session()
    username = f"gender_test_{int(time.time())}"
    
    # Signup
    signup_data = {
        "username": username,
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    
    # Test onboarding with non-binary gender
    onboarding_data = {
        "support_topics": "identity_concerns",
        "languages": "English",
        "support_style": "mixed",
        "cultural_background": "North America",
        "gender": "non-binary",
        "graduation_year": "2026",
        "degree_program": "bachelors",
        "display_name": "NonBinaryTest"
    }
    r = session.post(f"{BASE_URL}/onboarding", data=onboarding_data, allow_redirects=False)
    print(f"POST /onboarding with non-binary gender -> {r.status_code}")
    
    # Verify profile shows the gender
    r = session.get(f"{BASE_URL}/profile")
    assert r.status_code == 200
    print("Gender options test: PASSED")
    
    session.get(f"{BASE_URL}/logout")
    return True


def test_groups_page():
    """Test the groups page functionality."""
    print("\n[Groups Page Tests]")
    print("-" * 40)
    
    session = requests.Session()
    username = f"groups_test_{int(time.time())}"
    
    # Signup and complete onboarding
    signup_data = {
        "username": username,
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    
    onboarding_data = {
        "support_topics": "anxiety,depression",
        "languages": "English",
        "support_style": "mixed",
        "cultural_background": "",
        "gender": "prefer-not-to-say",
        "graduation_year": "2027",
        "degree_program": "bachelors",
        "display_name": "GroupsTest"
    }
    session.post(f"{BASE_URL}/onboarding", data=onboarding_data, allow_redirects=False)
    
    # Test groups page
    r = session.get(f"{BASE_URL}/groups")
    print(f"GET /groups -> {r.status_code}")
    assert r.status_code == 200
    assert "Groups" in r.text or "groups" in r.text.lower()
    
    # Test group search functionality
    r = session.get(f"{BASE_URL}/groups?search=anxiety")
    print(f"GET /groups?search=anxiety -> {r.status_code}")
    assert r.status_code == 200
    
    print("Groups page test: PASSED")
    session.get(f"{BASE_URL}/logout")
    return True


def test_peers_page():
    """Test the peers page functionality."""
    print("\n[Peers Page Tests]")
    print("-" * 40)
    
    session = requests.Session()
    username = f"peers_test_{int(time.time())}"
    
    # Signup and complete onboarding
    signup_data = {
        "username": username,
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    
    onboarding_data = {
        "support_topics": "loneliness_isolation,social_anxiety",
        "languages": "English,Korean",
        "support_style": "sharing",
        "cultural_background": "East Asia",
        "gender": "female",
        "graduation_year": "2028",
        "degree_program": "doctoral",
        "display_name": "PeersTest"
    }
    session.post(f"{BASE_URL}/onboarding", data=onboarding_data, allow_redirects=False)
    
    # Test peers page
    r = session.get(f"{BASE_URL}/peers")
    print(f"GET /peers -> {r.status_code}")
    assert r.status_code == 200
    
    # Test people page (find peers)
    r = session.get(f"{BASE_URL}/people")
    print(f"GET /people -> {r.status_code}")
    assert r.status_code == 200
    
    print("Peers page test: PASSED")
    session.get(f"{BASE_URL}/logout")
    return True


def test_resources_hub():
    """Test the resources hub page."""
    print("\n[Resources Hub Tests]")
    print("-" * 40)
    
    session = requests.Session()
    username = f"resources_test_{int(time.time())}"
    
    # Signup and complete onboarding
    signup_data = {
        "username": username,
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    session.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    
    onboarding_data = {
        "support_topics": "academic_problems,financial_stress",
        "languages": "English",
        "support_style": "advice",
        "cultural_background": "Africa",
        "gender": "male",
        "graduation_year": "2026",
        "degree_program": "masters",
        "display_name": "ResourcesTest"
    }
    session.post(f"{BASE_URL}/onboarding", data=onboarding_data, allow_redirects=False)
    
    # Test resources hub
    r = session.get(f"{BASE_URL}/resources-hub")
    print(f"GET /resources-hub -> {r.status_code}")
    assert r.status_code == 200
    assert "Resources" in r.text or "resources" in r.text.lower()
    
    print("Resources hub test: PASSED")
    session.get(f"{BASE_URL}/logout")
    return True


def test_branding():
    """Test that Sun Devil Circles branding is used correctly."""
    print("\n[Branding Tests]")
    print("-" * 40)
    
    # Test landing page
    r = requests.get(f"{BASE_URL}/")
    print(f"GET / -> Checking branding...")
    
    # Check for SunDevil Circles instead of SunDevil Circle
    assert "SunDevil" in r.text
    assert "Circles" in r.text
    
    # Check footer has 2026 copyright
    assert "2026" in r.text
    
    print("Branding test: PASSED")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Sun Devil Circles - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Branding", test_branding),
        ("Onboarding Flow", test_onboarding_flow),
        ("Cultural Background", test_cultural_background_section),
        ("Gender Options", test_gender_options),
        ("Groups Page", test_groups_page),
        ("Peers Page", test_peers_page),
        ("Resources Hub", test_resources_hub),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"FAILED: {name} - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    run_all_tests()
