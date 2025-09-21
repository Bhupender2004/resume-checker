#!/usr/bin/env python3
"""
Quick test to verify the pipeline is working correctly
"""

import sys
import os
import time
from io import BytesIO

# Add the script directory to the Python path
script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script')
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    from script.pipeline import evaluate_resume_fast, extract_skills_cached
    from script.parse_jd import extract_skills
    from script.hard_match import calculate_hard_score
    from script.semantic_match import calculate_semantic_score
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def test_individual_functions():
    """Test each function individually"""
    print("🧪 Testing individual functions...")
    
    # Test job description parsing
    print("1. Testing job description parsing...")
    jd_text = "We need a Python developer with experience in Django, React, and SQL databases."
    try:
        must_have, good_to_have = extract_skills(jd_text)
        print(f"   ✅ Must have skills: {must_have}")
        print(f"   ✅ Good to have skills: {good_to_have}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test hard matching
    print("2. Testing hard skills matching...")
    resume_text = "I am a Python developer with 3 years of experience in Django and React development."
    try:
        hard_score, missing = calculate_hard_score(resume_text, must_have)
        print(f"   ✅ Hard score: {hard_score}, Missing: {missing}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test semantic matching
    print("3. Testing semantic matching...")
    try:
        semantic_score = calculate_semantic_score(resume_text, must_have + good_to_have)
        print(f"   ✅ Semantic score: {semantic_score}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True

def test_pipeline():
    """Test the complete pipeline"""
    print("\n🚀 Testing complete pipeline...")
    
    # Create a mock resume file
    resume_content = b"""
    John Doe
    Software Developer
    
    Experience:
    - 3 years of Python development
    - Django web framework
    - React frontend development
    - SQL database management
    - Git version control
    
    Education:
    - Bachelor's in Computer Science
    
    Skills:
    - Python, Django, React, SQL, Git
    - Problem solving and teamwork
    """
    
    class MockFile:
        def __init__(self, content, name):
            self.content = content
            self.name = name
            self.position = 0
        
        def read(self, size=-1):
            if size == -1:
                result = self.content[self.position:]
                self.position = len(self.content)
            else:
                result = self.content[self.position:self.position + size]
                self.position += len(result)
            return result
        
        def seek(self, position):
            self.position = position
        
        def getvalue(self):
            return self.content
    
    mock_resume = MockFile(resume_content, "test_resume.pdf")
    jd_text = "We are looking for a Python developer with Django and React experience. SQL knowledge required."
    
    try:
        print("   Testing fast evaluation...")
        start_time = time.time()
        result = evaluate_resume_fast(mock_resume, jd_text, skip_feedback=True)
        end_time = time.time()
        
        print(f"   ✅ Processing time: {end_time - start_time:.2f} seconds")
        print(f"   ✅ Result: {result}")
        
        if result.get("Total Score", 0) > 0:
            print("   ✅ Pipeline working correctly!")
            return True
        else:
            print("   ❌ Pipeline returned zero score")
            return False
            
    except Exception as e:
        print(f"   ❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔧 Resume Processing Pipeline Test")
    print("=" * 50)
    
    # Test individual functions first
    if not test_individual_functions():
        print("\n❌ Individual function tests failed!")
        return
    
    # Test complete pipeline
    if not test_pipeline():
        print("\n❌ Pipeline test failed!")
        return
    
    print("\n✅ All tests passed! Pipeline is working correctly.")
    print("\n🚀 Your resume processing should now work without hanging!")

if __name__ == "__main__":
    main()
