"""
Setup database tables for Resume Hackathon application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Create database tables"""
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_SERVICE_KEY')  # Use service key for admin operations
        
        if not url or not key:
            print("❌ Missing Supabase credentials")
            return False
        
        print(f"🔗 Connecting to: {url}")
        supabase = create_client(url, key)
        
        # Create users table
        print("📊 Creating users table...")
        users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            last_login TIMESTAMP WITH TIME ZONE,
            is_active BOOLEAN DEFAULT TRUE,
            profile_picture_url TEXT,
            company VARCHAR(255),
            role VARCHAR(100) DEFAULT 'user'
        );
        """
        
        # Create resume_evaluations table
        print("📊 Creating resume_evaluations table...")
        evaluations_sql = """
        CREATE TABLE IF NOT EXISTS resume_evaluations (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            resume_name VARCHAR(255) NOT NULL,
            job_description_name VARCHAR(255) NOT NULL,
            total_score DECIMAL(5,2) NOT NULL,
            verdict VARCHAR(50) NOT NULL,
            missing_skills TEXT[],
            feedback TEXT,
            processing_time DECIMAL(5,2),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            resume_file_path TEXT,
            jd_file_path TEXT
        );
        """
        
        # Create user_preferences table
        print("📊 Creating user_preferences table...")
        preferences_sql = """
        CREATE TABLE IF NOT EXISTS user_preferences (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            theme VARCHAR(20) DEFAULT 'light',
            fast_mode_default BOOLEAN DEFAULT TRUE,
            email_notifications BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Execute SQL commands using RPC
        try:
            # Note: Supabase Python client doesn't directly support DDL
            # You need to run these in the Supabase SQL Editor
            print("⚠️ Please run the SQL commands in your Supabase SQL Editor:")
            print("\n" + "="*50)
            print("COPY AND PASTE THIS SQL INTO SUPABASE SQL EDITOR:")
            print("="*50)
            print(users_sql)
            print(evaluations_sql)
            print(preferences_sql)
            print("="*50)
            
            # Test if tables exist by trying to query them
            try:
                result = supabase.table('users').select('count').execute()
                print("✅ Users table exists!")
                return True
            except:
                print("❌ Tables need to be created manually in Supabase SQL Editor")
                return False
                
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Resume Hackathon Database...")
    success = setup_database()
    
    if success:
        print("\n🎉 Database setup complete!")
    else:
        print("\n📝 Manual setup required:")
        print("1. Go to your Supabase project dashboard")
        print("2. Open SQL Editor")
        print("3. Copy and paste the SQL from supabase_setup.sql")
        print("4. Run the SQL to create tables")
        print("5. Restart the application")
