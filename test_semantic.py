"""Test semantic matching functions."""
import sys
sys.path.insert(0, ".")

from app import (
    build_profile_text,
    cosine_similarity,
    keyword_score,
    get_keyword_matches,
    store_user_embedding,
    store_group_embedding,
    get_recommended_groups_semantic,
    get_similar_users,
    user_embeddings,
    group_embeddings,
    init_group_embeddings,
    PRESET_GROUPS
)

def test_semantic_functions():
    print("Testing Semantic Matching Functions...")
    print("=" * 50)
    
    # Test build_profile_text
    profile = {
        "display_name": "John",
        "is_international_freshman": True,
        "primary_challenge": ["academic", "social"],
        "preferred_language": "Spanish",
        "support_style": "mixed"
    }
    text = build_profile_text(profile)
    print(f"Profile text: {text[:100]}...")
    assert "John" in text
    assert "international" in text
    assert "academic" in text or "challenges" in text
    print("build_profile_text: OK")
    
    # Test cosine_similarity
    vec_a = [1.0, 0.0, 0.0]
    vec_b = [1.0, 0.0, 0.0]
    sim = cosine_similarity(vec_a, vec_b)
    print(f"Cosine similarity (identical): {sim}")
    assert abs(sim - 1.0) < 0.001
    
    vec_c = [0.0, 1.0, 0.0]
    sim2 = cosine_similarity(vec_a, vec_c)
    print(f"Cosine similarity (orthogonal): {sim2}")
    assert abs(sim2) < 0.001
    print("cosine_similarity: OK")
    
    # Test keyword_score
    score = keyword_score("academic stress exams", "stress about exams")
    print(f"Keyword score: {score}")
    assert score > 0
    print("keyword_score: OK")
    
    # Test get_keyword_matches
    candidates = {
        "Academic Pressure": "academic exams stress grades",
        "Making Friends": "social friends connect people",
        "Homesickness": "home family miss lonely"
    }
    matches = get_keyword_matches("stress about exams", candidates)
    print(f"Keyword matches: {matches}")
    assert len(matches) > 0
    print("get_keyword_matches: OK")
    
    # Test store functions (fallback mode without HF API)
    store_user_embedding(1, profile)
    print(f"User embeddings count: {len(user_embeddings)}")
    assert 1 in user_embeddings
    print("store_user_embedding: OK")
    
    init_group_embeddings()
    print(f"Group embeddings count: {len(group_embeddings)}")
    assert len(group_embeddings) == len(PRESET_GROUPS)
    print("init_group_embeddings: OK")
    
    # Test get_recommended_groups_semantic
    recommendations = get_recommended_groups_semantic(1, top_n=3)
    print(f"Recommended groups: {recommendations}")
    assert len(recommendations) > 0
    print("get_recommended_groups_semantic: OK")
    
    # Test get_similar_users with multiple users
    profile2 = {
        "display_name": "Maria",
        "is_international_freshman": True,
        "primary_challenge": ["academic"],
        "preferred_language": "Spanish",
        "support_style": "sharing"
    }
    store_user_embedding(2, profile2)
    
    profile3 = {
        "display_name": "Alex",
        "is_international_freshman": False,
        "primary_challenge": ["financial"],
        "preferred_language": "English",
        "support_style": "listening"
    }
    store_user_embedding(3, profile3)
    
    similar = get_similar_users(1, top_n=3, threshold=0.05)
    print(f"Similar users to user 1: {similar}")
    print("get_similar_users: OK")
    
    print("=" * 50)
    print("All semantic matching tests passed!")

if __name__ == "__main__":
    test_semantic_functions()
