"""
Authentication module using Supabase for login and signup
"""

import streamlit as st
import os
import hashlib
import re
from datetime import datetime, timedelta
import time

# Import Supabase with error handling
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError as e:
    print(f"Supabase import error: {e}")
    SUPABASE_AVAILABLE = False
except Exception as e:
    print(f"Supabase error: {e}")
    SUPABASE_AVAILABLE = False

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "your-anon-key")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Initialize Supabase client
def init_supabase():
    """Initialize Supabase client"""
    if not SUPABASE_AVAILABLE:
        return None

    # Check if credentials are configured
    if SUPABASE_URL == "https://your-project.supabase.co" or SUPABASE_KEY == "your-anon-key":
        return None

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return None

def check_tables_exist():
    """Check if database tables exist"""
    supabase = init_supabase()
    if not supabase:
        return False

    try:
        # Test if users table exists
        result = supabase.table('users').select('count').execute()
        return True
    except Exception as e:
        print(f"Tables check failed: {e}")
        return False

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def create_user_table():
    """Create users table if it doesn't exist"""
    supabase = init_supabase()
    if not supabase:
        return False
    
    try:
        # This would typically be done via Supabase dashboard or SQL
        # For demo purposes, we'll assume the table exists
        return True
    except Exception as e:
        st.error(f"Error creating user table: {e}")
        return False

def signup_user(email: str, password: str, full_name: str) -> tuple[bool, str]:
    """Sign up a new user"""
    supabase = init_supabase()
    if not supabase:
        return False, "Database not configured. Please set up Supabase credentials."
    
    # Validate inputs
    if not validate_email(email):
        return False, "Invalid email format"
    
    is_valid, message = validate_password(password)
    if not is_valid:
        return False, message
    
    if len(full_name.strip()) < 2:
        return False, "Full name must be at least 2 characters"
    
    try:
        # Check if user already exists
        existing_user = supabase.table('users').select('email').eq('email', email).execute()
        if existing_user.data:
            return False, "User with this email already exists"
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Insert new user
        user_data = {
            'email': email,
            'password_hash': hashed_password,
            'full_name': full_name.strip(),
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'is_active': True
        }
        
        result = supabase.table('users').insert(user_data).execute()
        
        if result.data:
            return True, "Account created successfully! Please log in."
        else:
            return False, "Failed to create account"
            
    except Exception as e:
        return False, f"Signup error: {str(e)}"

def login_user(email: str, password: str) -> tuple[bool, str, dict]:
    """Login user"""
    supabase = init_supabase()
    if not supabase:
        return False, "Database not configured. Please set up Supabase credentials.", {}
    
    # Validate inputs
    if not validate_email(email):
        return False, "Invalid email format", {}
    
    if len(password) < 1:
        return False, "Password is required", {}
    
    try:
        # Hash password
        hashed_password = hash_password(password)
        
        # Find user
        result = supabase.table('users').select('*').eq('email', email).eq('password_hash', hashed_password).execute()
        
        if not result.data:
            return False, "Invalid email or password", {}
        
        user = result.data[0]
        
        # Check if user is active
        if not user.get('is_active', True):
            return False, "Account is deactivated", {}
        
        # Update last login
        supabase.table('users').update({
            'last_login': datetime.now().isoformat()
        }).eq('id', user['id']).execute()
        
        # Remove password hash from user data
        user_data = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return True, "Login successful!", user_data
        
    except Exception as e:
        return False, f"Login error: {str(e)}", {}

def logout_user():
    """Logout user by clearing session state"""
    keys_to_clear = ['authenticated', 'user_data', 'user_email', 'user_name']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user() -> dict:
    """Get current user data"""
    return st.session_state.get('user_data', {})

def require_auth():
    """Decorator to require authentication"""
    if not is_authenticated():
        st.error("🔒 Please log in to access this page")
        st.stop()

def show_login_page():
    """Display login page"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🚀 Resume Hackathon</h1>
        <h3>AI-Powered Resume Screening Platform</h3>
        <p style="color: #666;">Please log in to continue</p>
    </div>
    """, unsafe_allow_html=True)

    # Check if Supabase and tables are available
    supabase = init_supabase()
    tables_exist = check_tables_exist()

    if not supabase or not tables_exist:
        show_demo_login()
        return

    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        show_login_form()

    with tab2:
        show_signup_form()

def show_demo_login():
    """Show demo login when database tables are not available"""
    # Check what's missing
    supabase = init_supabase()
    tables_exist = check_tables_exist()

    if not supabase:
        st.error("🔧 **Supabase Connection Issue**")
        st.markdown("Please check your Supabase credentials in the .env file")
    elif not tables_exist:
        st.info("🔧 **Database Tables Setup Required**")

        with st.expander("📋 **Complete These Steps**", expanded=True):
            st.markdown("""
            **You're almost there! Just run the SQL setup:**

            1. **Go to your Supabase project**: https://wfyiwytaozlbgbnquqaz.supabase.co
            2. **Open SQL Editor** in the dashboard
            3. **Copy and paste** the SQL from `supabase_setup.sql` file (you have it ready!)
            4. **Click "Run"** to create database tables
            5. **Refresh this page** to see the login form

            **Your credentials are configured!** ✅
            **Just need to create the tables!** 🗄️
            """)

    st.markdown("### 🎯 Demo Mode Available")
    st.markdown("You can continue in demo mode while setting up the database:")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Continue in Demo Mode", type="primary", use_container_width=True):
            st.session_state['authenticated'] = True
            st.session_state['user_data'] = {
                'id': 'demo-user',
                'email': 'demo@example.com',
                'full_name': 'Demo User'
            }
            st.session_state['user_email'] = 'demo@example.com'
            st.session_state['user_name'] = 'Demo User'
            st.success("✅ Logged in as Demo User!")
            time.sleep(1)
            st.rerun()

def show_login_form():
    """Display login form"""
    st.markdown("### 🔑 Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if login_button:
            if email and password:
                with st.spinner("🔄 Logging in..."):
                    success, message, user_data = login_user(email, password)
                
                if success:
                    st.session_state['authenticated'] = True
                    st.session_state['user_data'] = user_data
                    st.session_state['user_email'] = user_data.get('email', '')
                    st.session_state['user_name'] = user_data.get('full_name', '')
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

def show_signup_form():
    """Display signup form"""
    st.markdown("### 📝 Create New Account")
    
    with st.form("signup_form"):
        full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms and Conditions")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            signup_button = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
        
        if signup_button:
            if full_name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif not terms_accepted:
                    st.error("Please accept the Terms and Conditions")
                else:
                    with st.spinner("🔄 Creating account..."):
                        success, message = signup_user(email, password, full_name)
                    
                    if success:
                        st.success(message)
                        st.info("Please switch to the Login tab to sign in")
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def show_user_menu():
    """Display user menu in sidebar"""
    if is_authenticated():
        user_data = get_current_user()
        user_name = user_data.get('full_name', 'User')
        user_email = user_data.get('email', '')
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### 👤 Welcome, {user_name}!")
        st.sidebar.markdown(f"📧 {user_email}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # User stats (optional)
        st.sidebar.markdown("### 📊 Your Stats")
        st.sidebar.metric("🎯 Resumes Processed", "0")  # This would come from database
        st.sidebar.metric("⭐ Success Rate", "0%")  # This would be calculated
