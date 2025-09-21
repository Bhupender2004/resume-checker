import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime
import time
from script.pipeline import evaluate_resume, evaluate_resume_fast

# Page configuration
st.set_page_config(
    page_title="Resume Evaluator Pro",
    page_icon="🎯",
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

# Custom CSS - White theme with color overrides
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

    /* Header styling - Vibrant blue */
    .main-header {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(52, 152, 219, 0.3);
    }

    /* Tab styling - Purple theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border-radius: 15px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        color: #4a148c;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border: 2px solid transparent;
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
        color: white;
        border: 2px solid #4a148c;
    }

    /* Upload section - Light green theme */
    .upload-section {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
        border: 2px solid #28a745;
        color: #155724;
    }

    .upload-section h3 {
        color: #155724;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Result cards with better colors */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid;
        font-weight: 500;
        color: #2c3e50;
    }

    .high-score {
        border-left-color: #27ae60;
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
    }
    .medium-score {
        border-left-color: #f39c12;
        background: linear-gradient(135deg, #fef9e7 0%, #fcf3cf 100%);
    }
    .low-score {
        border-left-color: #e74c3c;
        background: linear-gradient(135deg, #fdedec 0%, #fadbd8 100%);
    }

    /* Metric containers - Different colors */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        font-weight: 600;
        color: #2c3e50;
    }

    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .metric-container-blue {
        border-left: 5px solid #3498db;
        background: linear-gradient(135deg, #ebf3fd 0%, #d6eaff 100%);
    }

    .metric-container-green {
        border-left: 5px solid #27ae60;
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
    }

    .metric-container-orange {
        border-left: 5px solid #f39c12;
        background: linear-gradient(135deg, #fef9e7 0%, #fcf3cf 100%);
    }

    /* Search container - Light orange theme */
    .search-container {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid #ff9800;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
        color: #e65100;
    }

    .search-container h3 {
        color: #e65100;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Button styling - Colorful */
    .stButton > button {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
        font-size: 1rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.6);
        background: linear-gradient(45deg, #c0392b, #a93226);
    }

    /* File uploader styling */
    .stFileUploader {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 1rem;
        border: 2px dashed #3498db;
        box-shadow: 0 2px 10px rgba(52, 152, 219, 0.1);
    }

    .stFileUploader label {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* Text visibility improvements */
    .stMarkdown {
        color: #2c3e50;
        font-weight: 500;
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50;
        font-weight: 700;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DB_PATH = 'results.db'

# Database setup
def init_db():
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

# Save result to DB
def save_result(resume_name, jd_name, score, verdict, feedback, missing_elements):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO results (resume_name, jd_name, score, verdict, feedback, missing_elements)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (resume_name, jd_name, score, verdict, feedback, missing_elements))
    conn.commit()
    conn.close()

# Search results
def search_results(jd_filter=None, verdict_filter=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = 'SELECT * FROM results WHERE 1=1'
    params = []
    if jd_filter:
        query += ' AND jd_name LIKE ?'
        params.append(f'%{jd_filter}%')
    if verdict_filter:
        query += ' AND verdict = ?'
        params.append(verdict_filter)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Resume Evaluator Pro</h1>
    <p>Professional resume evaluation with AI-powered insights</p>
</div>
""", unsafe_allow_html=True)

# Initialize database
init_db()

# Debug info
st.write("Debug: Application loaded successfully")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["📝 Evaluate Resume", "🔍 Search Results", "📊 Analytics"])

# Debug tab content
st.write(f"Debug: Tabs created - tab1: {tab1 is not None}, tab2: {tab2 is not None}, tab3: {tab3 is not None}")

with tab1:
    st.write("Debug: Inside tab1")
    st.markdown("## 📁 Upload Documents")
    st.write("Upload your job description and candidate resume to get started")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Job Description")
        jd_file = st.file_uploader(
            "Upload Job Description",
            type=["txt", "pdf"],
            help="Upload the job description in TXT format",
            key='jd'
        )

        if jd_file:
            st.success(f"✅ Loaded: {jd_file.name}")

    with col2:
        st.markdown("### 📋 Resume")
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf"],
            help="Upload the candidate's resume in PDF format",
            key='resume'
        )

        if resume_file:
            st.success(f"✅ Loaded: {resume_file.name}")

    # Processing options
    st.markdown("---")
    fast_mode = st.checkbox("⚡ Fast Mode", value=True, key="fast_mode_simple",
                          help="Faster processing with basic feedback")

    # Evaluation button with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        evaluate_button = st.button(
            "🚀 Evaluate Resume",
            type="primary",
            use_container_width=True
        )

    if evaluate_button:
        if jd_file and resume_file:
            with st.spinner("🔄 Processing documents..."):
                try:
                    # Read the JD content
                    if jd_file.type == "text/plain":
                        jd_text = jd_file.read().decode("utf-8")
                    else:
                        st.error("Please upload a text file for the job description.")
                        st.stop()

                    # Save files for record keeping
                    jd_path = os.path.join('data/jds', jd_file.name)
                    resume_path = os.path.join('data/resumes', resume_file.name)

                    # Ensure directories exist
                    os.makedirs('data/jds', exist_ok=True)
                    os.makedirs('data/resumes', exist_ok=True)

                    # Save JD file
                    with open(jd_path, 'w', encoding='utf-8') as f:
                        f.write(jd_text)

                    # Save resume file
                    with open(resume_path, 'wb') as f:
                        f.write(resume_file.getvalue())

                    # Call optimized pipeline to evaluate
                    with st.spinner("🚀 Processing..."):
                        try:
                            if fast_mode:
                                result = evaluate_resume_fast(resume_file, jd_text, skip_feedback=True)
                            else:
                                result = evaluate_resume(resume_file, jd_text)

                            # Ensure we have a valid result
                            if not result:
                                st.error("❌ Processing failed - no result returned")
                                st.stop()

                        except Exception as e:
                            st.error(f"❌ Processing error: {str(e)}")
                            st.stop()

                    # Extract results with correct keys
                    score = result.get('Total Score', 0)
                    verdict = result.get('Verdict', 'N/A')
                    feedback = result.get('Feedback', '')
                    missing = ', '.join(result.get('Missing Skills', []))

                    # Save result to database
                    save_result(resume_file.name, jd_file.name, score, verdict, feedback, missing)

                    # Display results with enhanced styling
                    st.markdown("---")
                    st.markdown("## 🎉 Evaluation Complete!")

                    # Success message with score
                    if score >= 70:
                        st.success(f'🟢 Excellent Match! Score: {score}/100')
                    elif score >= 50:
                        st.warning(f'🟡 Good Match! Score: {score}/100')
                    else:
                        st.error(f'🔴 Needs Improvement! Score: {score}/100')

                    # Create enhanced result display
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown("""
                        <div class="metric-container">
                            <h3>📊 Total Score</h3>
                            <h2 style="color: #4facfe;">{}/100</h2>
                        </div>
                        """.format(score), unsafe_allow_html=True)

                    with col2:
                        verdict_color = "#4CAF50" if verdict == "High" else "#FF9800" if verdict == "Medium" else "#F44336"
                        st.markdown("""
                        <div class="metric-container">
                            <h3>🎯 Verdict</h3>
                            <h2 style="color: {};">{}</h2>
                        </div>
                        """.format(verdict_color, verdict), unsafe_allow_html=True)

                    with col3:
                        missing_count = len(result.get('Missing Skills', []))
                        st.markdown("""
                        <div class="metric-container">
                            <h3>⚠️ Missing Skills</h3>
                            <h2 style="color: #FF6B6B;">{}</h2>
                        </div>
                        """.format(missing_count), unsafe_allow_html=True)

                    # Detailed feedback section
                    st.markdown("### 💡 Detailed Feedback")
                    st.markdown(f"""
                    <div class="result-card">
                        {feedback}
                    </div>
                    """, unsafe_allow_html=True)

                    # Missing skills breakdown
                    if missing:
                        st.markdown("### 🎯 Skills to Improve")
                        missing_skills = result.get('Missing Skills', [])
                        for i, skill in enumerate(missing_skills[:5]):  # Show first 5
                            st.markdown(f"• **{skill}**")
                        if len(missing_skills) > 5:
                            st.markdown(f"*... and {len(missing_skills) - 5} more skills*")

                except Exception as e:
                    st.error(f"❌ Error during evaluation: {str(e)}")
                    st.write("Please check your files and try again.")
        else:
            st.warning('⚠️ Please upload both Job Description and Resume to proceed.')

with tab2:
    st.markdown("""
    <div class="search-container">
        <h2>🔍 Search & Filter Results</h2>
        <p>Find and analyze previous evaluations</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        jd_filter = st.text_input('🔍 Filter by JD name', placeholder="Enter job description name...")

    with col2:
        verdict_filter = st.selectbox('📊 Filter by Verdict', options=['All', 'High', 'Medium', 'Low'])

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        search_button = st.button('🔍 Search Results', type="primary")

    if search_button or st.session_state.get('auto_search', False):
        verdict_param = verdict_filter if verdict_filter != 'All' else None
        results = search_results(jd_filter if jd_filter else None, verdict_param)

        if results:
            st.markdown(f"### 📋 Found {len(results)} result(s)")

            # Display results in cards
            for i, row in enumerate(results):
                score = row[3]
                verdict = row[4]

                # Determine card styling based on verdict
                if verdict == "High":
                    border_color = "#4CAF50"
                    emoji = "🟢"
                elif verdict == "Medium":
                    border_color = "#FF9800"
                    emoji = "🟡"
                else:
                    border_color = "#F44336"
                    emoji = "🔴"

                st.markdown(f"""
                <div style="border-left: 5px solid {border_color}; padding: 1rem; margin: 1rem 0; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4>{emoji} {row[1]}</h4>
                        <span style="background: {border_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                            {score}/100
                        </span>
                    </div>
                    <p><strong>Job Description:</strong> {row[2]}</p>
                    <p><strong>Verdict:</strong> {verdict}</p>
                    <p><strong>Missing Skills:</strong> {row[6] if row[6] else 'None'}</p>
                </div>
                """, unsafe_allow_html=True)

                # Expandable feedback section
                with st.expander(f"💡 View Feedback for {row[1]}"):
                    st.write(row[5])
        else:
            st.info("No results found. Try adjusting your search criteria.")

with tab3:
    st.markdown("### 📊 Analytics Dashboard")

    # Get all results for analytics
    all_results = search_results()

    if all_results:
        # Convert to DataFrame for analysis
        df = pd.DataFrame(all_results, columns=['ID', 'Resume', 'JD', 'Score', 'Verdict', 'Feedback', 'Missing'])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📈 Score Statistics")
            avg_score = df['Score'].mean()
            max_score = df['Score'].max()
            min_score = df['Score'].min()

            st.metric("Average Score", f"{avg_score:.1f}")
            st.metric("Highest Score", f"{max_score}")
            st.metric("Lowest Score", f"{min_score}")

        with col2:
            st.markdown("#### 🎯 Verdict Distribution")
            verdict_counts = df['Verdict'].value_counts()
            for verdict, count in verdict_counts.items():
                percentage = (count / len(df)) * 100
                st.write(f"**{verdict}:** {count} ({percentage:.1f}%)")

        # Recent evaluations
        st.markdown("#### 🕒 Recent Evaluations")
        recent_results = df.tail(5)  # Last 5 results
        st.dataframe(recent_results[['Resume', 'JD', 'Score', 'Verdict']], use_container_width=True)

    else:
        st.info("No evaluation data available yet. Complete some evaluations to see analytics.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h4>🎯 Resume Evaluator Pro</h4>
    <p>Powered by AI and Natural Language Processing</p>
    <p><small>Built with Streamlit • Advanced Resume Screening Technology</small></p>
</div>
""", unsafe_allow_html=True)
