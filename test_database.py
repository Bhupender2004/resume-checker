#!/usr/bin/env python3
"""
Test script to verify the database functionality
"""

import sqlite3
import os
import sys

# Import the database functions from streamlit_app
sys.path.append(os.getcwd())

def test_database_operations():
    """Test all database operations"""
    print("🗄️  Testing database operations...")
    
    # Test database file path
    DB_PATH = 'test_results.db'
    
    # Clean up any existing test database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    try:
        # Test database initialization
        print("   📝 Testing database initialization...")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            jd_name TEXT,
            score INTEGER,
            verdict TEXT,
            feedback TEXT,
            missing_elements TEXT
        )''')
        conn.commit()
        conn.close()
        print("   ✅ Database initialization successful")
        
        # Test saving results
        print("   💾 Testing save result...")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO results (resume_name, jd_name, score, verdict, feedback, missing_elements)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  ('test_resume.pdf', 'test_jd.txt', 75, 'High', 'Great resume!', 'docker, kubernetes'))
        conn.commit()
        conn.close()
        print("   ✅ Save result successful")
        
        # Test searching results
        print("   🔍 Testing search results...")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Search without filters
        c.execute('SELECT * FROM results WHERE 1=1')
        all_results = c.fetchall()
        print(f"   📊 Found {len(all_results)} total results")
        
        # Search with JD filter
        jd_filter = 'test'
        query = 'SELECT * FROM results WHERE 1=1 AND jd_name LIKE ?'
        c.execute(query, [f'%{jd_filter}%'])
        filtered_results = c.fetchall()
        print(f"   📊 Found {len(filtered_results)} results with JD filter")
        
        # Search with verdict filter
        verdict_filter = 'High'
        query = 'SELECT * FROM results WHERE 1=1 AND verdict = ?'
        c.execute(query, [verdict_filter])
        verdict_results = c.fetchall()
        print(f"   📊 Found {len(verdict_results)} results with verdict filter")
        
        conn.close()
        print("   ✅ Search results successful")
        
        # Test data integrity
        print("   🔒 Testing data integrity...")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM results WHERE id = 1')
        result = c.fetchone()
        
        if result:
            print(f"   📋 Retrieved result: {result[1]} -> {result[4]} (Score: {result[3]})")
            assert result[1] == 'test_resume.pdf'
            assert result[2] == 'test_jd.txt'
            assert result[3] == 75
            assert result[4] == 'High'
            print("   ✅ Data integrity verified")
        else:
            raise Exception("No result found with id=1")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up test database
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("   🧹 Test database cleaned up")

def test_streamlit_app_functions():
    """Test the specific functions from streamlit_app.py"""
    print("\n📱 Testing streamlit_app functions...")
    
    try:
        # Import functions from streamlit_app
        import streamlit_app
        
        # Test init_db
        print("   🏗️  Testing init_db...")
        streamlit_app.init_db()
        print("   ✅ init_db successful")
        
        # Test save_result
        print("   💾 Testing save_result...")
        streamlit_app.save_result(
            'test_resume2.pdf', 
            'test_jd2.txt', 
            85, 
            'High', 
            'Excellent match!', 
            'machine learning'
        )
        print("   ✅ save_result successful")
        
        # Test search_results
        print("   🔍 Testing search_results...")
        
        # Search all results
        all_results = streamlit_app.search_results()
        print(f"   📊 Found {len(all_results)} total results")
        
        # Search with filters
        jd_results = streamlit_app.search_results(jd_filter='test')
        print(f"   📊 Found {len(jd_results)} results with JD filter")
        
        verdict_results = streamlit_app.search_results(verdict_filter='High')
        print(f"   📊 Found {len(verdict_results)} results with verdict filter")
        
        print("   ✅ search_results successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Streamlit app functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        if os.path.exists(streamlit_app.DB_PATH):
            try:
                os.remove(streamlit_app.DB_PATH)
                print("   🧹 Streamlit database cleaned up")
            except:
                pass

def main():
    """Run all database tests"""
    print("🗄️  Starting Database Functionality Tests")
    print("=" * 50)
    
    tests = [
        test_database_operations,
        test_streamlit_app_functions,
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
        print("🎉 All database tests passed! Database functionality is working correctly.")
        return True
    else:
        print("⚠️  Some database tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
