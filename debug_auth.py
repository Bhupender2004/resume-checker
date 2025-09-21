"""
Debug authentication system
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_auth_system():
    """Debug the authentication system"""
    print("🔧 Debugging Authentication System")
    print("=" * 50)
    
    # Test imports
    try:
        from supabase import create_client
        print("✅ Supabase import successful")
    except Exception as e:
        print(f"❌ Supabase import failed: {e}")
        return
    
    # Test credentials
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"📊 SUPABASE_URL: {url}")
    print(f"📊 SUPABASE_ANON_KEY: {key[:30]}..." if key else "❌ No key")
    
    if not url or not key:
        print("❌ Missing credentials")
        return
    
    # Test connection
    try:
        supabase = create_client(url, key)
        print("✅ Supabase client created")
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return
    
    # Test tables
    tables = ['users', 'resume_evaluations', 'user_preferences', 'user_sessions']
    all_tables_exist = True
    
    for table in tables:
        try:
            result = supabase.table(table).select('count').execute()
            print(f"✅ {table} table exists")
        except Exception as e:
            print(f"❌ {table} table missing: {e}")
            all_tables_exist = False
    
    # Test auth module
    try:
        from auth import init_supabase, check_tables_exist, show_login_page
        print("✅ Auth module imported")
        
        # Test init_supabase
        supabase_client = init_supabase()
        if supabase_client:
            print("✅ init_supabase() returns client")
        else:
            print("❌ init_supabase() returns None")
        
        # Test check_tables_exist
        tables_exist = check_tables_exist()
        print(f"📊 check_tables_exist(): {tables_exist}")
        
    except Exception as e:
        print(f"❌ Auth module error: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"Supabase Connection: {'✅ Working' if supabase else '❌ Failed'}")
    print(f"All Tables Exist: {'✅ Yes' if all_tables_exist else '❌ No'}")
    print(f"Should Show Login: {'✅ Yes' if all_tables_exist else '❌ No (Demo Mode)'}")
    
    if all_tables_exist:
        print("\n🎉 Everything looks good! Login page should be showing.")
        print("If you're still seeing demo mode, try:")
        print("1. Hard refresh the browser (Ctrl+F5)")
        print("2. Clear browser cache")
        print("3. Restart the Streamlit app")
    else:
        print("\n⚠️ Some tables are missing. Please run the SQL setup.")

if __name__ == "__main__":
    debug_auth_system()
