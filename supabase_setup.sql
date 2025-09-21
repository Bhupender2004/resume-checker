-- Supabase Database Setup for Resume Hackathon Application
-- Run these SQL commands in your Supabase SQL Editor

-- 1. Create users table
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

-- 2. Create resume_evaluations table to track user's resume processing
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

-- 3. Create user_sessions table for session management (optional)
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create user_preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(20) DEFAULT 'light',
    fast_mode_default BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_resume_evaluations_user_id ON resume_evaluations(user_id);
CREATE INDEX IF NOT EXISTS idx_resume_evaluations_created_at ON resume_evaluations(created_at);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);

-- 6. Create Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE resume_evaluations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- 7. Create policies for users table
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- 8. Create policies for resume_evaluations table
CREATE POLICY "Users can view own evaluations" ON resume_evaluations
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own evaluations" ON resume_evaluations
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own evaluations" ON resume_evaluations
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own evaluations" ON resume_evaluations
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- 9. Create policies for user_sessions table
CREATE POLICY "Users can manage own sessions" ON user_sessions
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 10. Create policies for user_preferences table
CREATE POLICY "Users can manage own preferences" ON user_preferences
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 11. Create functions for user statistics
CREATE OR REPLACE FUNCTION get_user_stats(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    total_resumes INTEGER;
    high_matches INTEGER;
    medium_matches INTEGER;
    low_matches INTEGER;
    avg_score DECIMAL(5,2);
    success_rate DECIMAL(5,2);
BEGIN
    -- Get total resumes processed
    SELECT COUNT(*) INTO total_resumes
    FROM resume_evaluations
    WHERE user_id = user_uuid;
    
    -- Get match counts
    SELECT 
        COUNT(CASE WHEN verdict = 'High' THEN 1 END),
        COUNT(CASE WHEN verdict = 'Medium' THEN 1 END),
        COUNT(CASE WHEN verdict = 'Low' THEN 1 END),
        AVG(total_score)
    INTO high_matches, medium_matches, low_matches, avg_score
    FROM resume_evaluations
    WHERE user_id = user_uuid;
    
    -- Calculate success rate (High + Medium matches)
    IF total_resumes > 0 THEN
        success_rate = ((high_matches + medium_matches)::DECIMAL / total_resumes) * 100;
    ELSE
        success_rate = 0;
    END IF;
    
    RETURN json_build_object(
        'total_resumes', COALESCE(total_resumes, 0),
        'high_matches', COALESCE(high_matches, 0),
        'medium_matches', COALESCE(medium_matches, 0),
        'low_matches', COALESCE(low_matches, 0),
        'avg_score', COALESCE(avg_score, 0),
        'success_rate', COALESCE(success_rate, 0)
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 12. Create trigger to automatically create user preferences
CREATE OR REPLACE FUNCTION create_user_preferences()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_preferences (user_id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_user_preferences
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_user_preferences();

-- 13. Create view for user dashboard data
CREATE OR REPLACE VIEW user_dashboard AS
SELECT 
    u.id,
    u.full_name,
    u.email,
    u.created_at as member_since,
    COUNT(re.id) as total_evaluations,
    COUNT(CASE WHEN re.verdict = 'High' THEN 1 END) as high_matches,
    COUNT(CASE WHEN re.verdict = 'Medium' THEN 1 END) as medium_matches,
    COUNT(CASE WHEN re.verdict = 'Low' THEN 1 END) as low_matches,
    AVG(re.total_score) as avg_score,
    MAX(re.created_at) as last_evaluation
FROM users u
LEFT JOIN resume_evaluations re ON u.id = re.user_id
GROUP BY u.id, u.full_name, u.email, u.created_at;

-- 14. Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;
