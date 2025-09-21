import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Using basic skill extraction.")
    nlp = None

def extract_skills(jd_text):
    """
    Extract skills from job description text.
    Fast keyword-based extraction to avoid hanging issues.
    """
    try:
        # Limit text length for faster processing
        if len(jd_text) > 2000:
            jd_text = jd_text[:2000]

        # Common technical skills and keywords
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
            'html', 'css', 'bootstrap', 'tailwind', 'sass', 'less',
            'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net',
            'machine learning', 'deep learning', 'ai', 'data science', 'pandas', 'numpy',
            'tensorflow', 'pytorch', 'scikit-learn', 'opencv', 'nlp',
            'agile', 'scrum', 'devops', 'ci/cd', 'microservices', 'api', 'rest', 'graphql'
        ]

        soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
            'creative', 'adaptable', 'organized', 'detail-oriented', 'time management'
        ]

        jd_lower = jd_text.lower()

        # Extract skills using keyword matching
        found_technical = []
        found_soft = []

        for skill in technical_skills:
            if skill in jd_lower:
                found_technical.append(skill)

        for skill in soft_skills:
            if skill in jd_lower:
                found_soft.append(skill)

        # Skip spaCy processing to avoid hanging issues
        # Use simple regex patterns instead
        requirement_patterns = [
            r'(?:required|must have|essential)[\s\w]*?:\s*([^.]+)',
            r'(?:experience with|knowledge of|proficient in)\s+([^.]+)'
        ]

        try:
            for pattern in requirement_patterns:
                matches = re.finditer(pattern, jd_lower, re.IGNORECASE)
                for match in matches:
                    requirement_text = match.group(1)
                    # Extract individual skills from the requirement text
                    for skill in technical_skills[:10]:  # Limit to first 10 skills for speed
                        if skill in requirement_text and skill not in found_technical:
                            found_technical.append(skill)
        except Exception:
            pass  # Continue even if regex fails

        # Remove duplicates and clean up
        must_have = list(set(found_technical))
        good_to_have = list(set(found_soft))

        return must_have, good_to_have

    except Exception as e:
        # Fallback to basic skills if everything fails
        return ['python', 'java', 'javascript'], ['communication', 'teamwork']
