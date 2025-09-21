"""
Main Resume Hackathon Application with Authentication
"""

import streamlit as st
import os

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.warning("python-dotenv not available. Using system environment variables.")
except Exception as e:
    st.warning(f"Could not load .env file: {e}")

# Import authentication module
try:
    from auth import (
        show_login_page, 
        is_authenticated, 
        show_user_menu, 
        require_auth,
        get_current_user
    )
    AUTH_AVAILABLE = True
except ImportError:
    st.error("Authentication module not available. Please install required packages.")
    AUTH_AVAILABLE = False

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }

    /* Login container styling */
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        border: 1px solid #e9ecef;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }

    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        border: none;
    }

    .stError {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        border: none;
    }

    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Navigation styling */
    .nav-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #dee2e6;
    }
    </style>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="Resume Hackathon - AI Resume Screening",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme
st.markdown("""
<script>
const doc = window.parent.document;
doc.body.classList.add('light-theme');
</script>
""", unsafe_allow_html=True)

# Custom CSS for white theme with color overrides
st.markdown("""
<style>
    /* Force white theme - Override all Streamlit defaults */
    .stApp {
        background: white !important;
        color: #2c3e50 !important;
    }
    
    /* Main content area - Pure white */
    .main .block-container {
        background: white !important;
        color: #2c3e50 !important;
        padding-top: 2rem !important;
    }
    
    /* Sidebar - Light gray */
    .css-1d391kg {
        background: #f8f9fa !important;
        color: #2c3e50 !important;
    }
    
    /* Override any dark theme elements */
    .stApp > header {
        background: transparent !important;
    }
    
    /* Main background - White theme */
    .main {
        background: white !important;
        color: #2c3e50 !important;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    
    /* Login container styling */
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    /* Navigation styling */
    .nav-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #dee2e6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(231, 76, 60, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def show_navigation():
    """Show navigation menu for authenticated users"""
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎯 Main Dashboard", use_container_width=True):
            st.session_state['current_page'] = 'dashboard'
    
    with col2:
        if st.button("⭐ Clean Interface", use_container_width=True):
            st.session_state['current_page'] = 'clean'
    
    with col3:
        if st.button("📋 Simple Interface", use_container_width=True):
            st.session_state['current_page'] = 'simple'
    
    with col4:
        if st.button("📊 My Analytics", use_container_width=True):
            st.session_state['current_page'] = 'analytics'
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    """Show main dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Resume Screening Dashboard</h1>
        <p>Advanced resume analysis with intelligent matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Import and run the main app logic
    try:
        import app
        # Note: This would need to be refactored to work as a function
        st.info("🔄 Loading main dashboard... Please use the individual applications for now.")
        st.markdown("### 🌐 Available Applications:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🎯 Main Dashboard**
            - Advanced analytics
            - Batch processing
            - Export functionality
            - [Open Application](http://localhost:8504)
            """)
        
        with col2:
            st.markdown("""
            **⭐ Clean Application**
            - Professional interface
            - Fast processing
            - Database integration
            - [Open Application](http://localhost:8507)
            """)
        
        with col3:
            st.markdown("""
            **📋 Simple Interface**
            - Streamlined workflow
            - Quick results
            - Easy to use
            - [Open Application](http://localhost:8505)
            """)
            
    except ImportError:
        st.error("Dashboard module not available")

def show_analytics():
    """Show user analytics"""
    user_data = get_current_user()
    user_name = user_data.get('full_name', 'User')
    
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Your resume processing statistics, {user_name}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample analytics (would be fetched from database)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Resumes", "0", "0 this week")
    
    with col2:
        st.metric("🟢 High Matches", "0", "0%")
    
    with col3:
        st.metric("🟡 Medium Matches", "0", "0%")
    
    with col4:
        st.metric("⭐ Success Rate", "0%", "0%")
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    st.info("No recent activity. Start processing resumes to see your analytics!")
    
    # Charts would go here
    st.markdown("### 📊 Performance Trends")
    st.info("Charts and trends will appear here after you process some resumes.")

def main():
    """Main application logic"""

    # Set page config
    st.set_page_config(
        page_title="Resume Hackathon - Login",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply custom CSS
    apply_custom_css()

    # Debug button to force refresh authentication
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Force Refresh Authentication", help="Click if login page is not showing"):
            st.cache_data.clear()
            st.cache_resource.clear()
            if 'authenticated' in st.session_state:
                del st.session_state['authenticated']
            st.rerun()

    if not AUTH_AVAILABLE:
        st.error("🔧 Authentication system not configured. Please check your setup.")
        return

    # Check authentication
    if not is_authenticated():
        show_login_page()
        return
    
    # Show user menu in sidebar
    show_user_menu()
    
    # Show navigation
    show_navigation()
    
    # Get current page from session state
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # Show appropriate page
    if current_page == 'dashboard':
        show_dashboard()
    elif current_page == 'analytics':
        show_analytics()
    elif current_page == 'clean':
        st.info("🔄 Redirecting to Clean Application...")
        st.markdown("[Open Clean Application](http://localhost:8507)")
    elif current_page == 'simple':
        st.info("🔄 Redirecting to Simple Application...")
        st.markdown("[Open Simple Application](http://localhost:8505)")
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
