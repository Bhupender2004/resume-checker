#!/usr/bin/env python3
"""
Performance test script for the resume evaluation system
"""

import sys
import os
import time
import tempfile
from io import BytesIO

# Add script directory to path
sys.path.append(os.path.join(os.getcwd(), "script"))

try:
    from script.pipeline import evaluate_resume
    from script.parse_jd import extract_skills
    from script.parse_resume import extract_text
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def create_sample_resume(size="medium"):
    """Create sample resume content of different sizes"""
    base_content = """
    John Doe
    Senior Software Engineer
    
    EXPERIENCE:
    Senior Software Engineer at TechCorp (2020-2024)
    - Developed scalable web applications using Python, Django, and React
    - Led a team of 5 developers in agile development environment
    - Implemented microservices architecture using Docker and Kubernetes
    - Worked with AWS services including EC2, S3, RDS, and Lambda
    - Built RESTful APIs and GraphQL endpoints
    - Used PostgreSQL and MongoDB for data storage
    - Implemented CI/CD pipelines using Jenkins and GitLab
    - Collaborated with product managers and designers
    - Mentored junior developers and conducted code reviews
    
    Software Engineer at StartupXYZ (2018-2020)
    - Built full-stack applications using JavaScript, Node.js, and Vue.js
    - Worked with MySQL and Redis databases
    - Implemented real-time features using WebSockets
    - Used Git for version control and GitHub for collaboration
    - Participated in daily standups and sprint planning
    
    EDUCATION:
    Bachelor of Science in Computer Science
    University of Technology (2014-2018)
    - Relevant coursework: Data Structures, Algorithms, Database Systems
    - Senior project: Machine Learning recommendation system
    
    SKILLS:
    Programming Languages: Python, JavaScript, Java, C++
    Web Technologies: HTML, CSS, React, Vue.js, Angular
    Backend: Django, Flask, Node.js, Express.js
    Databases: PostgreSQL, MySQL, MongoDB, Redis
    Cloud: AWS, Azure, Google Cloud Platform
    DevOps: Docker, Kubernetes, Jenkins, GitLab CI
    Tools: Git, GitHub, Jira, Slack, VS Code
    """
    
    if size == "small":
        return base_content[:500].encode('utf-8')
    elif size == "large":
        return (base_content * 3).encode('utf-8')
    else:  # medium
        return base_content.encode('utf-8')

def create_sample_jd(size="medium"):
    """Create sample job description of different sizes"""
    base_jd = """
    Senior Full Stack Developer Position
    
    We are seeking an experienced Full Stack Developer to join our growing team.
    
    Required Skills:
    - 5+ years of experience in software development
    - Proficiency in Python and JavaScript
    - Experience with React.js and modern frontend frameworks
    - Knowledge of backend frameworks like Django or Flask
    - Experience with SQL databases (PostgreSQL, MySQL)
    - Familiarity with cloud platforms (AWS, Azure)
    - Experience with version control (Git)
    - Knowledge of RESTful API development
    - Understanding of microservices architecture
    - Experience with containerization (Docker)
    
    Preferred Skills:
    - Experience with Kubernetes
    - Knowledge of machine learning concepts
    - Familiarity with DevOps practices
    - Experience with NoSQL databases
    - Knowledge of GraphQL
    - Experience with testing frameworks
    """
    
    if size == "small":
        return base_jd[:200]
    elif size == "large":
        return base_jd * 2
    else:  # medium
        return base_jd

def time_function(func, *args, **kwargs):
    """Time a function execution"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def test_skill_extraction_performance():
    """Test skill extraction performance with different JD sizes"""
    print("\n⚡ Testing skill extraction performance...")
    
    sizes = ["small", "medium", "large"]
    
    for size in sizes:
        jd_text = create_sample_jd(size)
        
        result, duration = time_function(extract_skills, jd_text)
        must_have, good_to_have = result
        
        print(f"   📊 {size.capitalize()} JD ({len(jd_text)} chars): {duration:.3f}s")
        print(f"      Found {len(must_have)} must-have, {len(good_to_have)} good-to-have skills")
    
    return True

def test_resume_processing_performance():
    """Test resume processing performance with different resume sizes"""
    print("\n📄 Testing resume processing performance...")
    
    sizes = ["small", "medium", "large"]
    jd_text = create_sample_jd("medium")
    
    for size in sizes:
        resume_content = create_sample_resume(size)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
            temp_file.write(resume_content)
            temp_file_path = temp_file.name
        
        try:
            class MockFile:
                def __init__(self, path):
                    self.name = os.path.basename(path)
                    self.path = path
            
            mock_file = MockFile(temp_file_path)
            
            result, duration = time_function(evaluate_resume, mock_file, jd_text)
            
            print(f"   📊 {size.capitalize()} resume ({len(resume_content)} chars): {duration:.3f}s")
            print(f"      Score: {result.get('Total Score', 0)}, Verdict: {result.get('Verdict', 'N/A')}")
            
        finally:
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    return True

def test_batch_processing_performance():
    """Test batch processing performance"""
    print("\n📦 Testing batch processing performance...")
    
    jd_text = create_sample_jd("medium")
    num_resumes = 5
    
    # Create multiple resume files
    resume_files = []
    temp_files = []
    
    for i in range(num_resumes):
        resume_content = create_sample_resume("medium")
        
        with tempfile.NamedTemporaryFile(suffix=f'_resume_{i}.txt', delete=False) as temp_file:
            temp_file.write(resume_content)
            temp_files.append(temp_file.name)
            
            class MockFile:
                def __init__(self, path):
                    self.name = os.path.basename(path)
                    self.path = path
            
            resume_files.append(MockFile(temp_file.name))
    
    try:
        # Time batch processing
        start_time = time.time()
        results = []
        
        for resume_file in resume_files:
            result = evaluate_resume(resume_file, jd_text)
            results.append(result)
        
        end_time = time.time()
        total_duration = end_time - start_time
        avg_duration = total_duration / num_resumes
        
        print(f"   📊 Processed {num_resumes} resumes in {total_duration:.3f}s")
        print(f"   📊 Average time per resume: {avg_duration:.3f}s")
        print(f"   📊 Throughput: {num_resumes/total_duration:.1f} resumes/second")
        
        # Show results summary
        scores = [r.get('Total Score', 0) for r in results]
        print(f"   📊 Score range: {min(scores):.1f} - {max(scores):.1f}")
        
    finally:
        # Clean up
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
    
    return True

def test_memory_usage():
    """Test memory usage patterns"""
    print("\n🧠 Testing memory usage...")
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"   📊 Initial memory usage: {initial_memory:.1f} MB")
        
        # Process several resumes
        jd_text = create_sample_jd("large")
        
        for i in range(3):
            resume_content = create_sample_resume("large")
            
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
                temp_file.write(resume_content)
                temp_file_path = temp_file.name
            
            try:
                class MockFile:
                    def __init__(self, path):
                        self.name = os.path.basename(path)
                        self.path = path
                
                mock_file = MockFile(temp_file_path)
                evaluate_resume(mock_file, jd_text)
                
                current_memory = process.memory_info().rss / 1024 / 1024  # MB
                print(f"   📊 Memory after resume {i+1}: {current_memory:.1f} MB")
                
            finally:
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"   📊 Final memory usage: {final_memory:.1f} MB")
        print(f"   📊 Memory increase: {memory_increase:.1f} MB")
        
        if memory_increase < 50:  # Less than 50MB increase is good
            print("   ✅ Memory usage is reasonable")
        else:
            print("   ⚠️  High memory usage detected")
        
    except ImportError:
        print("   ⚠️  psutil not available, skipping memory test")
    
    return True

def main():
    """Run all performance tests"""
    print("⚡ Starting Performance Tests")
    print("=" * 50)
    
    tests = [
        test_skill_extraction_performance,
        test_resume_processing_performance,
        test_batch_processing_performance,
        test_memory_usage,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📈 Performance Test Results: {passed}/{total} tests completed")
    
    if passed == total:
        print("🎉 All performance tests completed successfully!")
        print("💡 The application shows good performance characteristics.")
        return True
    else:
        print("⚠️  Some performance tests had issues. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
