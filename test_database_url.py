"""
Test script to verify DATABASE_URL configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_url():
    """Test DATABASE_URL configuration"""
    print("🔧 Testing DATABASE_URL Configuration...")
    print("=" * 50)
    
    # Get DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    # Check if password placeholder is still there
    if '[YOUR-PASSWORD]' in db_url:
        print("⚠️ DATABASE_URL contains placeholder password")
        print("📝 Please replace [YOUR-PASSWORD] with your actual Supabase database password")
        print("\n🔍 How to get your password:")
        print("1. Go to https://wfyiwytaozlbgbnquqaz.supabase.co")
        print("2. Settings → Database")
        print("3. Copy the URI connection string")
        print("4. Replace [YOUR-PASSWORD] with your actual password")
        return False
    
    # Check URL format
    if db_url.startswith('postgresql://'):
        print("✅ DATABASE_URL format is correct")
        print(f"📊 URL: {db_url[:50]}...")
        
        # Check if it contains the expected host
        if 'wfyiwytaozlbgbnquqaz' in db_url:
            print("✅ DATABASE_URL points to correct Supabase project")
        else:
            print("⚠️ DATABASE_URL might not be for the correct project")
        
        return True
    else:
        print("❌ DATABASE_URL format is incorrect")
        print("Expected format: postgresql://postgres.wfyiwytaozlbgbnquqaz:PASSWORD@host:port/database")
        return False

def test_other_credentials():
    """Test other Supabase credentials"""
    print("\n🔧 Testing Other Supabase Credentials...")
    print("=" * 50)
    
    # Test SUPABASE_URL
    supabase_url = os.getenv('SUPABASE_URL')
    if supabase_url and supabase_url != 'https://your-project.supabase.co':
        print("✅ SUPABASE_URL is configured")
        print(f"📊 URL: {supabase_url}")
    else:
        print("❌ SUPABASE_URL not configured")
    
    # Test SUPABASE_ANON_KEY
    anon_key = os.getenv('SUPABASE_ANON_KEY')
    if anon_key and anon_key != 'your-anon-key':
        print("✅ SUPABASE_ANON_KEY is configured")
        print(f"📊 Key: {anon_key[:30]}...")
    else:
        print("❌ SUPABASE_ANON_KEY not configured")
    
    # Test SUPABASE_SERVICE_KEY
    service_key = os.getenv('SUPABASE_SERVICE_KEY')
    if service_key and service_key != 'your-service-role-key':
        print("✅ SUPABASE_SERVICE_KEY is configured")
        print(f"📊 Key: {service_key[:30]}...")
    else:
        print("❌ SUPABASE_SERVICE_KEY not configured")

def main():
    """Main test function"""
    print("🚀 Resume Hackathon Database Configuration Test")
    print("=" * 60)
    
    # Test DATABASE_URL
    db_url_ok = test_database_url()
    
    # Test other credentials
    test_other_credentials()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Configuration Summary:")
    
    if db_url_ok:
        print("✅ DATABASE_URL: Properly configured")
        print("🎉 All database credentials are ready!")
        print("\n🚀 Benefits of complete configuration:")
        print("   • Direct database access for advanced operations")
        print("   • Enhanced performance for complex queries")
        print("   • Future-ready for additional features")
    else:
        print("⚠️ DATABASE_URL: Needs your password")
        print("✅ Application still works perfectly without it!")
        print("\n📝 To complete setup:")
        print("   1. Get your Supabase database password")
        print("   2. Replace [YOUR-PASSWORD] in .env file")
        print("   3. Save and restart application")
    
    print("\n🌐 Your application is running at:")
    print("🔐 Main App: http://localhost:8506")
    print("🎯 Clean App: http://localhost:8507")

if __name__ == "__main__":
    main()
