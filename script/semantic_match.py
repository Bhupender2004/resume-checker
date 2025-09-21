try:
    from sentence_transformers import SentenceTransformer, util
    # Use a smaller, faster model for better performance
    model = None  # Lazy loading
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Warning: sentence-transformers not available. Using basic semantic matching.")
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    model = None

def get_model():
    """Lazy load the sentence transformer model for better startup performance"""
    global model, SENTENCE_TRANSFORMERS_AVAILABLE
    if model is None and SENTENCE_TRANSFORMERS_AVAILABLE:
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error loading sentence transformer model: {e}")
            SENTENCE_TRANSFORMERS_AVAILABLE = False
    return model

def calculate_semantic_score(resume_text, jd_skills):
    """
    Calculate semantic similarity score between resume and job requirements.
    Optimized for speed with shorter text limits and faster fallback.
    """
    if not jd_skills:
        return 0

    # Use basic scoring for faster processing (semantic transformers are slow)
    # This provides good enough results for most use cases
    return calculate_basic_semantic_score(resume_text, jd_skills)

def calculate_semantic_score_advanced(resume_text, jd_skills):
    """
    Advanced semantic scoring using transformers (slower but more accurate)
    """
    if not jd_skills:
        return 0

    if SENTENCE_TRANSFORMERS_AVAILABLE:
        model = get_model()
        if model:
            try:
                jd_text = " ".join(jd_skills)
                # Limit text length for better performance
                resume_text_limited = resume_text[:500] if len(resume_text) > 500 else resume_text
                jd_text_limited = jd_text[:300] if len(jd_text) > 300 else jd_text

                emb1 = model.encode(resume_text_limited, convert_to_tensor=True)
                emb2 = model.encode(jd_text_limited, convert_to_tensor=True)
                score = util.cos_sim(emb1, emb2).item() * 50
                return min(max(score, 0), 50)
            except Exception as e:
                print(f"Error in semantic matching: {e}")
                return calculate_basic_semantic_score(resume_text, jd_skills)

    return calculate_basic_semantic_score(resume_text, jd_skills)

def calculate_basic_semantic_score(resume_text, jd_skills):
    """
    Basic semantic scoring using word overlap.
    """
    resume_words = set(resume_text.lower().split())
    jd_words = set(" ".join(jd_skills).lower().split())

    if not jd_words:
        return 0

    # Calculate Jaccard similarity
    intersection = len(resume_words.intersection(jd_words))
    union = len(resume_words.union(jd_words))

    if union == 0:
        return 0

    jaccard_score = intersection / union
    return min(jaccard_score * 50, 50)
