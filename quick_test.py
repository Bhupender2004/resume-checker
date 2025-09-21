"""
Quick test to verify all imports are working
"""

print("🔧 Testing all imports...")

# Test basic imports
try:
    import streamlit as st
    print("✅ Streamlit: OK")
except Exception as e:
    print(f"❌ Streamlit: {e}")

try:
    import os
    print("✅ OS: OK")
except Exception as e:
    print(f"❌ OS: {e}")

# Test optional imports
try:
    from dotenv import load_dotenv
    print("✅ python-dotenv: OK")
except Exception as e:
    print(f"⚠️ python-dotenv: {e}")

try:
    from supabase import create_client
    print("✅ Supabase: OK")
except Exception as e:
    print(f"⚠️ Supabase: {e}")

# Test auth module
try:
    from auth import show_login_page, is_authenticated
    print("✅ Auth module: OK")
except Exception as e:
    print(f"❌ Auth module: {e}")

print("\n🎯 Import test complete!")
print("✅ Applications should be running at:")
print("🔐 Main App: http://localhost:8506")
print("🎯 Clean App: http://localhost:8507")
