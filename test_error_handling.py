#!/usr/bin/env python3
"""
Test script to verify error handling with invalid files
"""

import sys
import os
import tempfile
from io import BytesIO

# Add script directory to path
sys.path.append(os.path.join(os.getcwd(), "script"))

try:
    from script.pipeline import evaluate_resume
    from script.parse_resume import extract_text
    from script.parse_jd import extract_skills
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def create_invalid_pdf():
    """Create an invalid PDF file"""
    return b"This is not a valid PDF file content"

def create_empty_file():
    """Create an empty file"""
    return b""

def create_corrupted_pdf():
    """Create a corrupted PDF-like file"""
    return b"%PDF-1.4\nThis is corrupted PDF content that will fail to parse"

def test_invalid_pdf_handling():
    """Test handling of invalid PDF files"""
    print("\n📄 Testing invalid PDF handling...")
    
    try:
        # Create invalid PDF file
        invalid_content = create_invalid_pdf()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(invalid_content)
            temp_file_path = temp_file.name
        
        class MockFile:
            def __init__(self, path):
                self.name = os.path.basename(path)
                self.path = path
        
        mock_file = MockFile(temp_file_path)
        
        # Test extract_text with invalid PDF
        print("   🔍 Testing text extraction from invalid PDF...")
        text = extract_text(mock_file)
        print(f"   📝 Extracted text length: {len(text)} characters")
        print("   ✅ Invalid PDF handled gracefully")
        
        # Test full pipeline with invalid PDF
        print("   ⚙️  Testing full pipeline with invalid PDF...")
        jd_text = "Looking for Python developer with experience in web development"
        result = evaluate_resume(mock_file, jd_text)
        print(f"   📊 Pipeline result: {result}")
        print("   ✅ Pipeline handled invalid PDF gracefully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Invalid PDF test failed: {e}")
        return False
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

def test_empty_file_handling():
    """Test handling of empty files"""
    print("\n📭 Testing empty file handling...")
    
    try:
        # Create empty file
        empty_content = create_empty_file()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(empty_content)
            temp_file_path = temp_file.name
        
        class MockFile:
            def __init__(self, path):
                self.name = os.path.basename(path)
                self.path = path
        
        mock_file = MockFile(temp_file_path)
        
        # Test extract_text with empty file
        print("   🔍 Testing text extraction from empty file...")
        text = extract_text(mock_file)
        print(f"   📝 Extracted text: '{text}'")
        print("   ✅ Empty file handled gracefully")
        
        # Test full pipeline with empty file
        print("   ⚙️  Testing full pipeline with empty file...")
        jd_text = "Looking for Python developer"
        result = evaluate_resume(mock_file, jd_text)
        print(f"   📊 Pipeline result: {result}")
        print("   ✅ Pipeline handled empty file gracefully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Empty file test failed: {e}")
        return False
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

def test_corrupted_pdf_handling():
    """Test handling of corrupted PDF files"""
    print("\n💥 Testing corrupted PDF handling...")
    
    try:
        # Create corrupted PDF file
        corrupted_content = create_corrupted_pdf()
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(corrupted_content)
            temp_file_path = temp_file.name
        
        class MockFile:
            def __init__(self, path):
                self.name = os.path.basename(path)
                self.path = path
        
        mock_file = MockFile(temp_file_path)
        
        # Test extract_text with corrupted PDF
        print("   🔍 Testing text extraction from corrupted PDF...")
        text = extract_text(mock_file)
        print(f"   📝 Extracted text length: {len(text)} characters")
        print("   ✅ Corrupted PDF handled gracefully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Corrupted PDF test failed: {e}")
        return False
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

def test_invalid_jd_handling():
    """Test handling of invalid job descriptions"""
    print("\n📋 Testing invalid JD handling...")
    
    try:
        # Test with empty JD
        print("   📝 Testing empty JD...")
        must_have, good_to_have = extract_skills("")
        print(f"   📊 Empty JD result: must_have={must_have}, good_to_have={good_to_have}")
        
        # Test with very long JD
        print("   📝 Testing very long JD...")
        long_jd = "Python " * 10000  # Very long text
        must_have, good_to_have = extract_skills(long_jd)
        print(f"   📊 Long JD result: {len(must_have)} must_have, {len(good_to_have)} good_to_have")
        
        # Test with special characters
        print("   📝 Testing JD with special characters...")
        special_jd = "Looking for Python developer with @#$%^&*() experience in 中文 and émojis 🚀"
        must_have, good_to_have = extract_skills(special_jd)
        print(f"   📊 Special chars JD result: must_have={must_have}, good_to_have={good_to_have}")
        
        print("   ✅ All JD tests handled gracefully")
        return True
        
    except Exception as e:
        print(f"   ❌ Invalid JD test failed: {e}")
        return False

def test_missing_file_handling():
    """Test handling of missing files"""
    print("\n🚫 Testing missing file handling...")
    
    try:
        class MockMissingFile:
            def __init__(self):
                self.name = "nonexistent.pdf"
                self.path = "/path/that/does/not/exist.pdf"
        
        mock_file = MockMissingFile()
        
        # Test extract_text with missing file
        print("   🔍 Testing text extraction from missing file...")
        text = extract_text(mock_file)
        print(f"   📝 Extracted text: '{text}'")
        print("   ✅ Missing file handled gracefully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Missing file test failed: {e}")
        return False

def main():
    """Run all error handling tests"""
    print("🛡️  Starting Error Handling Tests")
    print("=" * 50)
    
    tests = [
        test_invalid_pdf_handling,
        test_empty_file_handling,
        test_corrupted_pdf_handling,
        test_invalid_jd_handling,
        test_missing_file_handling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All error handling tests passed! The application handles errors gracefully.")
        return True
    else:
        print("⚠️  Some error handling tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
