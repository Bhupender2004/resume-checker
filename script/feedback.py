import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("Warning: OpenAI package not available. Using basic feedback generation.")
    OPENAI_AVAILABLE = False

def generate_feedback(resume_text, jd_text):
    """
    Generate feedback for resume improvement using OpenAI API.
    Falls back to a simple rule-based feedback if API key is not available.
    """
    if not OPENAI_AVAILABLE:
        return generate_simple_feedback(resume_text, jd_text)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # Fallback to simple rule-based feedback
        return generate_simple_feedback(resume_text, jd_text)

    try:
        client = OpenAI(api_key=api_key)
        prompt = f"Resume: {resume_text[:1000]}...\nJob Description: {jd_text[:1000]}...\nProvide 3 specific suggestions to improve this resume for the job:"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume advisor. Provide concise, actionable feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return generate_simple_feedback(resume_text, jd_text)

def generate_simple_feedback(resume_text, jd_text):
    """
    Generate fast rule-based feedback optimized for speed.
    """
    # Limit text processing for speed
    jd_lower = jd_text[:1000].lower() if len(jd_text) > 1000 else jd_text.lower()
    resume_lower = resume_text[:1000].lower() if len(resume_text) > 1000 else resume_text.lower()

    feedback_points = []

    # Quick skill check with most common technologies
    quick_skills = ['python', 'java', 'javascript', 'react', 'sql', 'aws']
    missing_tech = [skill for skill in quick_skills if skill in jd_lower and skill not in resume_lower]

    if missing_tech:
        feedback_points.append(f"Add skills: {', '.join(missing_tech[:2])}")

    # Quick experience check
    if 'experience' in jd_lower and len(resume_text.split()) < 150:
        feedback_points.append("Add more work experience details")

    # Default positive feedback for speed
    if not feedback_points:
        feedback_points.append("Resume matches job requirements well")

    return " • ".join(feedback_points)

def generate_feedback_fast(resume_text, jd_text):
    """
    Ultra-fast feedback generation for batch processing
    """
    return "Feedback available after detailed analysis"
