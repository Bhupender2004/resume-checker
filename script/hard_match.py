try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    print("Warning: fuzzywuzzy not available. Using basic string matching.")
    FUZZYWUZZY_AVAILABLE = False

def calculate_hard_score(resume_text, must_have_skills):
    """
    Calculate hard skills score based on exact and fuzzy matching.
    """
    score = 0
    missing_skills = []
    resume_lower = resume_text.lower()

    for skill in must_have_skills:
        skill_lower = skill.lower()

        # Check for exact match first
        if skill_lower in resume_lower:
            score += 10
        elif FUZZYWUZZY_AVAILABLE:
            # Use fuzzy matching if available
            if fuzz.partial_ratio(skill_lower, resume_lower) > 70:
                score += 8  # Slightly lower score for fuzzy match
            else:
                missing_skills.append(skill)
        else:
            # Basic substring matching as fallback
            words = skill_lower.split()
            if any(word in resume_lower for word in words if len(word) > 2):
                score += 6  # Lower score for partial word match
            else:
                missing_skills.append(skill)

    return min(score, 50), missing_skills
