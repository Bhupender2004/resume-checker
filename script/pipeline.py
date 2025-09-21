import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# Add the script directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    from parse_resume import extract_text
    from parse_jd import extract_skills
    from hard_match import calculate_hard_score
    from semantic_match import calculate_semantic_score
    from feedback import generate_feedback
except ImportError:
    # Fallback to absolute imports
    from script.parse_resume import extract_text
    from script.parse_jd import extract_skills
    from script.hard_match import calculate_hard_score
    from script.semantic_match import calculate_semantic_score
    from script.feedback import generate_feedback

# Cache for processed job descriptions to avoid reprocessing
_jd_cache = {}
_cache_lock = threading.Lock()

def extract_skills_cached(jd_text):
    """Cache job description skill extraction to avoid reprocessing"""
    jd_hash = hash(jd_text)

    with _cache_lock:
        if jd_hash in _jd_cache:
            return _jd_cache[jd_hash]

    must_have, good_to_have = extract_skills(jd_text)

    with _cache_lock:
        _jd_cache[jd_hash] = (must_have, good_to_have)

    return must_have, good_to_have

def evaluate_resume_fast(resume_file, jd_text, skip_feedback=False):
    """
    Fast resume evaluation with simplified processing (no parallel execution to avoid hanging)
    """
    start_time = time.time()

    try:
        # Extract text (this is usually the slowest part)
        resume_text = extract_text(resume_file)

        if not resume_text:
            return {
                "Resume": resume_file.name,
                "Total Score": 0,
                "Verdict": "Error",
                "Missing Skills": [],
                "Feedback": "Could not extract text from resume",
                "Processing Time": round(time.time() - start_time, 2)
            }

        # Use cached skill extraction
        must_have, good_to_have = extract_skills_cached(jd_text)

        # Calculate scores sequentially for reliability (avoid parallel processing issues)
        hard_score, missing_skills = calculate_hard_score(resume_text, must_have)
        semantic_score = calculate_semantic_score(resume_text, must_have + good_to_have)

        total_score = hard_score + semantic_score
        verdict = "High" if total_score >= 75 else "Medium" if total_score >= 50 else "Low"

        # Skip feedback for faster processing if requested
        if skip_feedback:
            feedback = "Feedback skipped for faster processing"
        else:
            feedback = generate_feedback(resume_text, jd_text)

        processing_time = time.time() - start_time

        return {
            "Resume": resume_file.name,
            "Total Score": round(total_score, 2),
            "Verdict": verdict,
            "Missing Skills": missing_skills,
            "Feedback": feedback,
            "Processing Time": round(processing_time, 2)
        }

    except Exception as e:
        return {
            "Resume": resume_file.name,
            "Total Score": 0,
            "Verdict": "Error",
            "Missing Skills": [],
            "Feedback": f"Processing error: {str(e)}",
            "Processing Time": round(time.time() - start_time, 2)
        }

def evaluate_resume(resume_file, jd_text):
    """
    Standard resume evaluation (backward compatibility)
    """
    return evaluate_resume_fast(resume_file, jd_text, skip_feedback=False)

def evaluate_resumes_batch(resume_files, jd_text, max_workers=2, skip_feedback=True):
    """
    Batch process multiple resumes with simplified parallel processing
    """
    if not resume_files:
        return []

    start_time = time.time()
    results = []

    # Pre-cache the job description skills
    try:
        extract_skills_cached(jd_text)
    except Exception:
        pass  # Continue even if caching fails

    # For small batches, process sequentially to avoid issues
    if len(resume_files) <= 2:
        for resume_file in resume_files:
            try:
                result = evaluate_resume_fast(resume_file, jd_text, skip_feedback)
                results.append(result)
            except Exception as e:
                results.append({
                    "Resume": resume_file.name,
                    "Total Score": 0,
                    "Verdict": "Error",
                    "Missing Skills": [],
                    "Feedback": f"Processing error: {str(e)}",
                    "Processing Time": 0
                })
    else:
        # Process larger batches with limited parallelism
        try:
            with ThreadPoolExecutor(max_workers=min(max_workers, 2)) as executor:
                # Submit all resume processing tasks
                future_to_resume = {
                    executor.submit(evaluate_resume_fast, resume_file, jd_text, skip_feedback): resume_file
                    for resume_file in resume_files
                }

                # Collect results as they complete
                for future in future_to_resume:
                    try:
                        result = future.result(timeout=60)  # 60 second timeout per resume
                        results.append(result)
                    except Exception as e:
                        resume_file = future_to_resume[future]
                        results.append({
                            "Resume": resume_file.name,
                            "Total Score": 0,
                            "Verdict": "Error",
                            "Missing Skills": [],
                            "Feedback": f"Processing timeout or error: {str(e)}",
                            "Processing Time": 0
                        })
        except Exception as e:
            # Fallback to sequential processing if parallel fails
            for resume_file in resume_files:
                try:
                    result = evaluate_resume_fast(resume_file, jd_text, skip_feedback)
                    results.append(result)
                except Exception as e:
                    results.append({
                        "Resume": resume_file.name,
                        "Total Score": 0,
                        "Verdict": "Error",
                        "Missing Skills": [],
                        "Feedback": f"Processing error: {str(e)}",
                        "Processing Time": 0
                    })

    total_time = time.time() - start_time

    # Add batch processing stats
    for result in results:
        result["Batch Processing Time"] = round(total_time, 2)
        result["Batch Size"] = len(resume_files)

    return results
