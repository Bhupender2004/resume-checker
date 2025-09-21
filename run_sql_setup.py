"""
Run SQL setup for Resume Hackathon database
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_sql_setup():
    """Run the SQL setup using Supabase"""
    try:
        from supabase import create_client
        
        # Use service key for admin operations
        url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not url or not service_key:
            print("❌ Missing Supabase credentials")
            return False
        
        print(f"🔗 Connecting to: {url}")
        supabase = create_client(url, service_key)
        
        # Read the SQL file
        try:
            with open('supabase_setup.sql', 'r') as f:
                sql_content = f.read()
            print("✅ SQL file loaded")
        except FileNotFoundError:
            print("❌ supabase_setup.sql file not found")
            return False
        
        # Split SQL into individual statements
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"📊 Found {len(sql_statements)} SQL statements")
        
        # Execute each statement
        success_count = 0
        for i, statement in enumerate(sql_statements, 1):
            if not statement:
                continue
                
            try:
                # Skip comments and empty lines
                if statement.startswith('--') or not statement.strip():
                    continue
                
                print(f"🔄 Executing statement {i}/{len(sql_statements)}")
                
                # Use RPC to execute SQL (this is a workaround for DDL statements)
                # Note: This might not work for all statements, manual execution in Supabase is recommended
                result = supabase.rpc('exec_sql', {'sql': statement}).execute()
                success_count += 1
                print(f"✅ Statement {i} executed successfully")
                
            except Exception as e:
                print(f"⚠️ Statement {i} failed: {e}")
                # Continue with other statements
                continue
        
        print(f"\n📊 Results: {success_count}/{len(sql_statements)} statements executed")
        
        # Test if tables were created
        try:
            result = supabase.table('users').select('count').execute()
            print("✅ Users table verified!")
            return True
        except Exception as e:
            print(f"⚠️ Table verification failed: {e}")
            print("Please run the SQL manually in Supabase SQL Editor")
            return False
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def manual_setup_instructions():
    """Show manual setup instructions"""
    print("\n" + "="*60)
    print("📋 MANUAL SETUP REQUIRED")
    print("="*60)
    print("""
The automatic setup didn't work completely. Please follow these steps:

1. 🌐 Go to: https://wfyiwytaozlbgbnquqaz.supabase.co
2. 🔑 Login to your Supabase account
3. 📝 Click "SQL Editor" in the left sidebar
4. 📋 Copy ALL the content from 'supabase_setup.sql' file
5. 📝 Paste it into the SQL Editor
6. ▶️ Click "Run" to execute all statements
7. ✅ Refresh your application page

The SQL file contains:
- Users table creation
- Resume evaluations table
- User preferences table
- Security policies
- Indexes and functions
""")
    print("="*60)

if __name__ == "__main__":
    print("🚀 Resume Hackathon Database Setup")
    print("="*50)
    
    success = run_sql_setup()
    
    if not success:
        manual_setup_instructions()
    else:
        print("\n🎉 Database setup complete!")
        print("🔄 Please refresh your application page to see the login form")
        print("🌐 Application: http://localhost:8506")
