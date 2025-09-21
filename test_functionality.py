#!/usr/bin/env python3
"""
Test script to verify the resume evaluation functionality
"""

import sys
import os
import tempfile
from io import BytesIO

# Add script directory to path
sys.path.append(os.path.join(os.getcwd(), "script"))

try:
    from script.pipeline import evaluate_resume
    print("✅ Pipeline import successful")
except ImportError as e:
    print(f"❌ Pipeline import failed: {e}")
    sys.exit(1)

def create_sample_resume_content():
    """Create sample resume content as bytes"""
    # This would normally be a PDF, but for testing we'll create a simple text
    resume_text = """
    John Doe
    Software Engineer
    
    Experience:
    - 5 years of Python development
    - Experience with React.js and JavaScript
    - Worked with PostgreSQL and MySQL databases
    - Familiar with AWS cloud services
    - Used Git for version control
    - Developed RESTful APIs
    - Experience with Docker containers
    - Worked in agile development teams
    
    Education:
    - Bachelor's degree in Computer Science
    - Certified AWS Solutions Architect
    
    Skills:
    - Python, JavaScript, React, Node.js
    - SQL, PostgreSQL, MySQL
    - AWS, Docker, Git
    - RESTful APIs, Microservices
    - Agile, Scrum
    """
    return resume_text.encode('utf-8')

def create_mock_file_object(content_bytes, filename="test_resume.pdf"):
    """Create a mock file object for testing"""
    class MockFile:
        def __init__(self, content, name):
            self.content = content
            self.name = name
            self._io = BytesIO(content)
        
        def read(self):
            return self.content
        
        def getvalue(self):
            return self.content
            
        def __enter__(self):
            return self
            
        def __exit__(self, *args):
            pass
    
    return MockFile(content_bytes, filename)

def test_basic_functionality():
    """Test basic resume evaluation functionality"""
    print("\n🧪 Testing basic functionality...")
    
    # Sample job description
    jd_text = """
    We are looking for a Software Engineer with experience in:
    - Python programming
    - JavaScript and React.js
    - SQL databases
    - AWS cloud services
    - Git version control
    - RESTful API development
    - Docker containerization
    - Agile development
    
    Requirements:
    - Bachelor's degree in Computer Science
    - 3+ years of experience
    """
    
    # Create mock resume file
    resume_content = create_sample_resume_content()
    
    # For testing, we'll save the content to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
        temp_file.write(resume_content)
        temp_file_path = temp_file.name
    
    try:
        # Test with file path (simulating PDF processing)
        class MockPDFFile:
            def __init__(self, path):
                self.name = os.path.basename(path)
                self.path = path
        
        mock_file = MockPDFFile(temp_file_path)
        
        # This will test the pipeline
        result = evaluate_resume(mock_file, jd_text)
        
        print(f"✅ Evaluation completed successfully!")
        print(f"📊 Results:")
        print(f"   - Resume: {result.get('Resume', 'N/A')}")
        print(f"   - Total Score: {result.get('Total Score', 0)}")
        print(f"   - Verdict: {result.get('Verdict', 'N/A')}")
        print(f"   - Missing Skills: {result.get('Missing Skills', [])}")
        print(f"   - Feedback: {result.get('Feedback', 'N/A')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        try:
            os.unlink(temp_file_path)
        except:
            pass

def test_skill_extraction():
    """Test skill extraction functionality"""
    print("\n🔍 Testing skill extraction...")
    
    try:
        from script.parse_jd import extract_skills
        
        jd_text = """
        Required skills: Python, JavaScript, React, SQL, AWS
        Good to have: Docker, Kubernetes, machine learning
        """
        
        must_have, good_to_have = extract_skills(jd_text)
        print(f"✅ Skill extraction successful!")
        print(f"   - Must have skills: {must_have}")
        print(f"   - Good to have skills: {good_to_have}")
        
        return True
        
    except Exception as e:
        print(f"❌ Skill extraction failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Resume Evaluation System Tests")
    print("=" * 50)
    
    tests = [
        test_skill_extraction,
        test_basic_functionality,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
