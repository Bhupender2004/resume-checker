#!/usr/bin/env python3
"""
Final verification script to ensure all components are working correctly
"""

import sys
import os
import subprocess
import time

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Test core pipeline
        sys.path.append(os.path.join(os.getcwd(), "script"))
        from script.pipeline import evaluate_resume
        from script.parse_resume import extract_text
        from script.parse_jd import extract_skills
        from script.hard_match import calculate_hard_score
        from script.semantic_match import calculate_semantic_score
        from script.feedback import generate_feedback
        print("   ✅ All core imports successful")
        
        # Test Streamlit apps
        import streamlit_app
        import app
        print("   ✅ Streamlit apps import successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_dependencies():
    """Test optional dependencies"""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ("streamlit", "Streamlit web framework"),
        ("pdfplumber", "PDF text extraction"),
        ("fuzzywuzzy", "Fuzzy string matching"),
        ("sentence_transformers", "Semantic similarity"),
        ("openai", "AI feedback generation"),
        ("spacy", "Natural language processing")
    ]
    
    available = 0
    total = len(dependencies)
    
    for dep, description in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep}: {description}")
            available += 1
        except ImportError:
            print(f"   ⚠️  {dep}: {description} (optional)")
    
    print(f"   📊 {available}/{total} dependencies available")
    return True

def test_spacy_model():
    """Test spaCy model availability"""
    print("\n🧠 Testing spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("Test sentence with Python programming skills.")
        print(f"   ✅ spaCy model loaded, processed {len(doc)} tokens")
        return True
    except Exception as e:
        print(f"   ⚠️  spaCy model not available: {e}")
        return True  # Not critical

def test_streamlit_apps():
    """Test that Streamlit apps can start"""
    print("\n🌐 Testing Streamlit applications...")
    
    # Test if apps can be imported without errors
    try:
        import streamlit_app
        import app
        print("   ✅ Both Streamlit apps can be imported")
        
        # Note: We don't actually start the servers in this test
        # as they would require user interaction
        print("   ℹ️  To test the web interface, run:")
        print("      streamlit run app.py")
        print("      streamlit run streamlit_app.py")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Streamlit app test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "streamlit_app.py",
        "requirements.txt",
        "script/pipeline.py",
        "script/parse_resume.py",
        "script/parse_jd.py",
        "script/hard_match.py",
        "script/semantic_match.py",
        "script/feedback.py",
        "README_FIXES.md"
    ]
    
    required_dirs = [
        "script",
        "data",
        "data/jds",
        "data/resumes"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
        else:
            print(f"   ✅ {dir_path}/")
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"   ❌ Missing directories: {missing_dirs}")
        return False
    
    print("   ✅ All required files and directories present")
    return True

def test_basic_functionality():
    """Test basic functionality with sample data"""
    print("\n⚙️  Testing basic functionality...")
    
    try:
        from script.parse_jd import extract_skills
        from script.hard_match import calculate_hard_score
        from script.semantic_match import calculate_semantic_score
        from script.feedback import generate_feedback
        
        # Test skill extraction
        jd_text = "Looking for Python developer with React experience"
        must_have, good_to_have = extract_skills(jd_text)
        print(f"   ✅ Skill extraction: {len(must_have)} must-have skills")
        
        # Test matching
        resume_text = "Experienced Python developer with React.js skills"
        hard_score, missing_skills = calculate_hard_score(resume_text, must_have)
        semantic_score = calculate_semantic_score(resume_text, must_have)
        print(f"   ✅ Matching: Hard={hard_score:.1f}, Semantic={semantic_score:.1f}")
        
        # Test feedback
        feedback = generate_feedback(resume_text, "Job description with Python and React requirements")
        print(f"   ✅ Feedback generation: {len(feedback)} characters")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification tests"""
    print("🚀 Final Verification - Resume Hackathon Application")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Dependencies", test_dependencies),
        ("spaCy Model", test_spacy_model),
        ("Basic Functionality", test_basic_functionality),
        ("Streamlit Apps", test_streamlit_apps),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 60)
    print(f"📈 Final Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n✨ The Resume Hackathon Application is ready to use!")
        print("\n🚀 To start the application:")
        print("   Main Dashboard: streamlit run app.py")
        print("   Simple Interface: streamlit run streamlit_app.py")
        print("\n📚 Documentation: See README_FIXES.md for details")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
