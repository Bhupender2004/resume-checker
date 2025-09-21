import sys, os
sys.path.append(os.path.join(os.getcwd(),"script"))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Try to import advanced visualization libraries
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
from datetime import datetime
import time
try:
    from script.pipeline import evaluate_resume, evaluate_resumes_batch, evaluate_resume_fast
except ImportError:
    from pipeline import evaluate_resume, evaluate_resumes_batch, evaluate_resume_fast

# ------------------------
# Page Config & Custom CSS
# ------------------------
st.set_page_config(
    page_title="AI Resume Screening Dashboard",
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

# Custom CSS for white theme - Force override Streamlit defaults
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

    /* Main background - Light theme */
    .main {
        background: white !important;
        color: #2c3e50 !important;
    }

    /* Header styling - Vibrant blue */
    .main-header {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(52, 152, 219, 0.3);
    }

    /* Upload section - Light green theme */
    .upload-section {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
        border: 2px solid #28a745;
    }

    .upload-section h3 {
        color: #155724;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Key Features section - Light purple theme */
    .features-section {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.2);
        border: 2px solid #9c27b0;
    }

    .features-section h3 {
        color: #4a148c;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .features-section p {
        color: #6a1b9a;
        font-weight: 600;
        line-height: 1.6;
    }

    /* Metric cards - Different colors */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        font-weight: 600;
    }

    .metric-card h4 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-weight: 700;
        font-size: 1.2rem;
    }

    .metric-card p {
        color: #34495e;
        margin-bottom: 0;
        line-height: 1.6;
        font-weight: 500;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .metric-card-blue {
        border-left: 5px solid #3498db;
        background: linear-gradient(135deg, #ebf3fd 0%, #d6eaff 100%);
    }

    .metric-card-green {
        border-left: 5px solid #27ae60;
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
    }

    .metric-card-orange {
        border-left: 5px solid #f39c12;
        background: linear-gradient(135deg, #fef9e7 0%, #fcf3cf 100%);
    }

    /* Candidate cards with better colors */
    .candidate-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid;
        font-weight: 500;
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

    /* Skill tags with better visibility */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
    }

    /* Sidebar styling - Light theme */
    .sidebar-section {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 2px solid #9c27b0;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.2);
    }

    .sidebar-section h3 {
        color: #4a148c;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .sidebar-section p {
        color: #6a1b9a;
        font-weight: 600;
        line-height: 1.6;
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

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🚀 AI-Powered Resume Screening Dashboard</h1>
    <p>Intelligent candidate evaluation with advanced NLP and machine learning</p>
</div>
""", unsafe_allow_html=True)

# ------------------------
# Sidebar: Upload + Filters
# ------------------------
st.sidebar.header("📁 Upload Files & Filters")

# Add instructions
with st.sidebar.expander("ℹ️ Instructions", expanded=False):
    st.write("""
    1. Upload a job description (TXT or PDF)
    2. Upload one or more resumes (PDF format)
    3. Adjust the minimum score filter if needed
    4. View results and download CSV report
    """)

# Key Features moved to sidebar with styling
st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>✨ Key Features</h3>
    <p><strong>🧠 AI-Powered Analysis</strong><br>
    Advanced NLP and machine learning algorithms analyze resumes for skill matching and semantic similarity.</p>

    <p><strong>📊 Interactive Analytics</strong><br>
    Comprehensive dashboards with charts, statistics, and insights to help you make informed decisions.</p>

    <p><strong>⚡ Fast Processing</strong><br>
    Process multiple resumes simultaneously with real-time progress tracking and instant results.</p>
</div>
""", unsafe_allow_html=True)

score_filter = st.sidebar.slider(
    "🎯 Minimum Total Score",
    0, 100, 50,
    help="Only show candidates with scores above this threshold"
)

# File uploads are now in the main content area

# Advanced Settings
with st.sidebar.expander("⚙️ Advanced Settings", expanded=False):
    st.markdown("**Scoring Weights**")
    hard_match_weight = st.slider("Hard Skills Weight", 0.0, 1.0, 0.6, 0.1)
    semantic_weight = st.slider("Semantic Match Weight", 0.0, 1.0, 0.4, 0.1)

    st.markdown("**Display Options**")
    show_detailed_feedback = st.checkbox("Show Detailed Feedback", True)
    show_skill_breakdown = st.checkbox("Show Skill Breakdown", True)
    max_results = st.number_input("Max Results to Display", 1, 100, 20)

# Export Options
with st.sidebar.expander("📊 Export Options", expanded=False):
    export_format = st.selectbox("Export Format", ["CSV", "JSON", "Excel"])
    include_feedback = st.checkbox("Include Feedback in Export", True)
    include_timestamps = st.checkbox("Include Timestamps", False)

# ------------------------
# Process Resumes
# ------------------------
results = []

# Processing logic will be moved to after upload section

# ------------------------
# Display Results
# ------------------------
results = st.session_state.get('results', [])
if results:
    # Summary Statistics
    st.markdown("## 📊 Results Overview")

    # Create summary metrics
    total_candidates = len(results)
    high_candidates = len([r for r in results if r["Verdict"] == "High"])
    medium_candidates = len([r for r in results if r["Verdict"] == "Medium"])
    low_candidates = len([r for r in results if r["Verdict"] == "Low"])
    avg_score = sum([r["Total Score"] for r in results]) / len(results) if results else 0

    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Candidates", total_candidates)
    with col2:
        st.metric("High Match", high_candidates, f"{(high_candidates/total_candidates*100):.1f}%")
    with col3:
        st.metric("Medium Match", medium_candidates, f"{(medium_candidates/total_candidates*100):.1f}%")
    with col4:
        st.metric("Low Match", low_candidates, f"{(low_candidates/total_candidates*100):.1f}%")
    with col5:
        st.metric("Average Score", f"{avg_score:.1f}")

    # Sorting and filtering options
    st.markdown("### 🔍 Filter & Sort Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        sort_by = st.selectbox("Sort by", ["Score (High to Low)", "Score (Low to High)", "Name (A-Z)", "Name (Z-A)"])
    with col2:
        filter_verdict = st.selectbox("Filter by Verdict", ["All", "High", "Medium", "Low"])
    with col3:
        search_term = st.text_input("Search in names/feedback", "")

    # Apply filters and sorting
    filtered_results = results.copy()

    # Filter by verdict
    if filter_verdict != "All":
        filtered_results = [r for r in filtered_results if r["Verdict"] == filter_verdict]

    # Filter by search term
    if search_term:
        filtered_results = [r for r in filtered_results if
                          search_term.lower() in r["Resume"].lower() or
                          search_term.lower() in r["Feedback"].lower()]

    # Sort results
    if sort_by == "Score (High to Low)":
        filtered_results.sort(key=lambda x: x["Total Score"], reverse=True)
    elif sort_by == "Score (Low to High)":
        filtered_results.sort(key=lambda x: x["Total Score"])
    elif sort_by == "Name (A-Z)":
        filtered_results.sort(key=lambda x: x["Resume"])
    elif sort_by == "Name (Z-A)":
        filtered_results.sort(key=lambda x: x["Resume"], reverse=True)

    # Limit results
    filtered_results = filtered_results[:max_results]

    st.markdown(f"### 📋 Candidate Results ({len(filtered_results)} shown)")

    # Display results with enhanced cards
    for i, r in enumerate(filtered_results):
        if r["Verdict"]=="High":
            color = "#4CAF50"
            emoji = "🟢"
            card_class = "high-score"
        elif r["Verdict"]=="Medium":
            color = "#FF9800"
            emoji = "🟡"
            card_class = "medium-score"
        else:
            color = "#F44336"
            emoji = "🔴"
            card_class = "low-score"

        with st.container():
            st.markdown(f"""
            <div class="candidate-card {card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="color: {color}; margin: 0;">{emoji} {r['Resume']}</h3>
                    <div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                        {r['Total Score']:.1f}/100
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Create expandable sections for detailed info
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"**Verdict:** {r['Verdict']}")
                if show_skill_breakdown and r.get('Missing Skills'):
                    st.markdown("**Missing Skills:**")
                    missing_skills = r['Missing Skills'][:5]  # Show first 5
                    for skill in missing_skills:
                        st.markdown(f"<span class='skill-tag'>❌ {skill}</span>", unsafe_allow_html=True)
                    if len(r['Missing Skills']) > 5:
                        st.markdown(f"<small>... and {len(r['Missing Skills']) - 5} more</small>", unsafe_allow_html=True)

            with col2:
                if show_detailed_feedback:
                    with st.expander("💡 Detailed Feedback"):
                        st.write(r['Feedback'])

                # Action buttons
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button(f"📧 Contact", key=f"contact_{i}"):
                        st.info("Contact feature would be implemented here")
                with col_btn2:
                    if st.button(f"📄 View Resume", key=f"view_{i}"):
                        st.info("Resume viewer would be implemented here")
                with col_btn3:
                    if st.button(f"⭐ Shortlist", key=f"shortlist_{i}"):
                        st.success(f"Added {r['Resume']} to shortlist!")

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")

    # ------------------------
    # Enhanced Analytics & Visualizations
    # ------------------------
    st.markdown("## 📈 Analytics Dashboard")

    # Create DataFrame for analysis
    df = pd.DataFrame(results)

    # Visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Score Distribution", "🎯 Skills Analysis", "📋 Export"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Verdict Distribution")
            if PLOTLY_AVAILABLE:
                # Use Plotly for interactive charts
                verdict_counts = df['Verdict'].value_counts()
                fig = px.pie(values=verdict_counts.values, names=verdict_counts.index,
                           color_discrete_map={'High': '#4CAF50', 'Medium': '#FF9800', 'Low': '#F44336'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Fallback to matplotlib
                fig, ax = plt.subplots(figsize=(8, 6))
                verdict_counts = df['Verdict'].value_counts()
                colors = ['#4CAF50' if x=='High' else '#FF9800' if x=='Medium' else '#F44336' for x in verdict_counts.index]
                ax.pie(verdict_counts.values, labels=verdict_counts.index, colors=colors, autopct='%1.1f%%')
                ax.set_title("Verdict Distribution")
                st.pyplot(fig)

        with col2:
            st.markdown("### Score Statistics")
            st.write(f"**Highest Score:** {df['Total Score'].max():.1f}")
            st.write(f"**Lowest Score:** {df['Total Score'].min():.1f}")
            st.write(f"**Average Score:** {df['Total Score'].mean():.1f}")
            st.write(f"**Median Score:** {df['Total Score'].median():.1f}")
            st.write(f"**Standard Deviation:** {df['Total Score'].std():.1f}")

            # Score ranges
            st.markdown("### Score Ranges")
            high_range = len(df[df['Total Score'] >= 70])
            medium_range = len(df[(df['Total Score'] >= 40) & (df['Total Score'] < 70)])
            low_range = len(df[df['Total Score'] < 40])

            st.write(f"**70-100 (Excellent):** {high_range} candidates")
            st.write(f"**40-69 (Good):** {medium_range} candidates")
            st.write(f"**0-39 (Needs Improvement):** {low_range} candidates")

    with tab2:
        st.markdown("### Score Distribution Histogram")
        if PLOTLY_AVAILABLE:
            fig = px.histogram(df, x='Total Score', nbins=20,
                             title="Distribution of Candidate Scores",
                             color_discrete_sequence=['#667eea'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['Total Score'], bins=20, color='#667eea', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Total Score')
            ax.set_ylabel('Number of Candidates')
            ax.set_title('Distribution of Candidate Scores')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        # Box plot for score distribution by verdict
        st.markdown("### Score Distribution by Verdict")
        if PLOTLY_AVAILABLE:
            fig = px.box(df, x='Verdict', y='Total Score',
                        color='Verdict',
                        color_discrete_map={'High': '#4CAF50', 'Medium': '#FF9800', 'Low': '#F44336'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            verdict_groups = [df[df['Verdict'] == v]['Total Score'].values for v in ['High', 'Medium', 'Low']]
            ax.boxplot(verdict_groups, labels=['High', 'Medium', 'Low'])
            ax.set_ylabel('Total Score')
            ax.set_title('Score Distribution by Verdict')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

    with tab3:
        st.markdown("### Skills Gap Analysis")

        # Analyze missing skills
        all_missing_skills = []
        for r in results:
            all_missing_skills.extend(r.get('Missing Skills', []))

        if all_missing_skills:
            from collections import Counter
            skill_counts = Counter(all_missing_skills)
            top_missing_skills = skill_counts.most_common(10)

            st.markdown("#### Top 10 Most Missing Skills")
            skills_df = pd.DataFrame(top_missing_skills, columns=['Skill', 'Count'])

            if PLOTLY_AVAILABLE:
                fig = px.bar(skills_df, x='Count', y='Skill', orientation='h',
                           title="Most Frequently Missing Skills")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(skills_df['Skill'], skills_df['Count'], color='#FF6B6B')
                ax.set_xlabel('Number of Candidates Missing This Skill')
                ax.set_title('Most Frequently Missing Skills')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

            # Skills gap table
            st.markdown("#### Detailed Skills Gap")
            st.dataframe(skills_df, use_container_width=True)
        else:
            st.info("No missing skills data available for analysis.")

    with tab4:
        st.markdown("### Export Results")

        # Prepare export data
        export_df = df.copy()
        if not include_feedback:
            export_df = export_df.drop('Feedback', axis=1, errors='ignore')

        if include_timestamps:
            export_df['Processed_At'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Export buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if export_format == "CSV":
                csv_data = export_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download CSV",
                    data=csv_data,
                    file_name=f"resume_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

        with col2:
            if export_format == "JSON":
                json_data = export_df.to_json(orient='records', indent=2).encode('utf-8')
                st.download_button(
                    "📥 Download JSON",
                    data=json_data,
                    file_name=f"resume_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        with col3:
            st.info("Excel export requires additional setup")

        # Preview export data
        st.markdown("#### Export Preview")
        st.dataframe(export_df.head(), use_container_width=True)

else:
    # Welcome screen with instructions
    st.markdown("## 👋 Welcome to AI Resume Screening Dashboard")



    # Upload section moved to main content
    st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload Documents</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="upload-section">
            <h3>📄 Upload Job Description</h3>
        </div>
        """, unsafe_allow_html=True)
        jd_file_main = st.file_uploader(
            "Drag and drop file here",
            type=["txt","pdf"],
            help="Limit 200MB per file • TXT, PDF",
            key="jd_main"
        )
        if jd_file_main:
            st.success(f"✅ Loaded: {jd_file_main.name}")

    with col2:
        st.markdown("""
        <div class="upload-section">
            <h3>📋 Upload Resumes</h3>
        </div>
        """, unsafe_allow_html=True)
        resumes_main = st.file_uploader(
            "Drag and drop files here",
            type=["pdf"],
            accept_multiple_files=True,
            help="Limit 200MB per file • PDF",
            key="resumes_main"
        )
        if resumes_main:
            st.success(f"✅ {len(resumes_main)} resume(s) loaded")

    # Processing section
    if jd_file_main and resumes_main:
        st.markdown("---")

        # Add process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process Resumes", type="primary", use_container_width=True):
                # Show processing status
                with st.spinner("Processing job description..."):
                    # Read JD
                    if jd_file_main.type=="text/plain":
                        jd_text = jd_file_main.read().decode("utf-8")
                    else:
                        # PDF JD
                        try:
                            import pdfplumber
                            jd_text = ""
                            with pdfplumber.open(jd_file_main) as pdf:
                                for page in pdf.pages:
                                    jd_text += page.extract_text() + "\n"
                        except ImportError:
                            st.error("pdfplumber not available. Please use TXT format for job descriptions.")
                            st.stop()

                # Process resumes with optimized batch processing
                st.subheader(f"⚡ Fast Processing {len(resumes_main)} resume(s)...")

                # Add processing mode selection
                col1, col2 = st.columns(2)
                with col1:
                    fast_mode = st.checkbox("🚀 Fast Mode (Skip detailed feedback)", value=True,
                                          help="Faster processing by skipping AI feedback generation")
                with col2:
                    batch_mode = st.checkbox("📦 Batch Mode (Parallel processing)", value=True,
                                           help="Process multiple resumes simultaneously")

                progress_bar = st.progress(0)
                status_text = st.empty()
                start_time = time.time()

                results = []

                if batch_mode and len(resumes_main) > 1:
                    # Use optimized batch processing
                    status_text.text("🚀 Processing all resumes in parallel...")
                    try:
                        all_results = evaluate_resumes_batch(resumes_main, jd_text,
                                                           max_workers=3, skip_feedback=fast_mode)
                        # Filter by score
                        results = [res for res in all_results if res["Total Score"] >= score_filter]
                        progress_bar.progress(1.0)
                    except Exception as e:
                        st.error(f"Batch processing error: {str(e)}")
                        # Fallback to sequential processing
                        for i, resume in enumerate(resumes_main):
                            status_text.text(f"Processing {resume.name}... ({i+1}/{len(resumes_main)})")
                            try:
                                res = evaluate_resume_fast(resume, jd_text, skip_feedback=fast_mode)
                                if res["Total Score"] >= score_filter:
                                    results.append(res)
                            except Exception as e:
                                st.error(f"Error processing {resume.name}: {str(e)}")
                            progress_bar.progress((i+1)/len(resumes_main))
                else:
                    # Sequential processing with fast mode
                    for i, resume in enumerate(resumes_main):
                        status_text.text(f"Processing {resume.name}... ({i+1}/{len(resumes_main)})")
                        try:
                            if fast_mode:
                                res = evaluate_resume_fast(resume, jd_text, skip_feedback=True)
                            else:
                                res = evaluate_resume(resume, jd_text)

                            if res["Total Score"] >= score_filter:
                                results.append(res)
                        except Exception as e:
                            st.error(f"Error processing {resume.name}: {str(e)}")
                        progress_bar.progress((i+1)/len(resumes_main))

                # Show processing time
                processing_time = time.time() - start_time
                status_text.text(f"✅ Completed in {processing_time:.2f} seconds!")

                # Clear progress after 2 seconds
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()

                # Store results in session state
                st.session_state['results'] = results

                # Display results immediately after processing
                if results:
                    st.markdown("---")
                    st.markdown("## 🎉 **Processing Complete!**")
                    st.markdown(f"### 📊 **Results for {len(results)} Resume(s)**")

                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("📋 Total Processed", len(results))

                    with col2:
                        high_count = len([r for r in results if r["Verdict"] == "High"])
                        st.metric("🟢 High Match", high_count)

                    with col3:
                        medium_count = len([r for r in results if r["Verdict"] == "Medium"])
                        st.metric("🟡 Medium Match", medium_count)

                    with col4:
                        low_count = len([r for r in results if r["Verdict"] == "Low"])
                        st.metric("🔴 Low Match", low_count)

                    # Display individual results
                    st.markdown("### 📄 **Individual Results**")

                    for i, result in enumerate(results):
                        with st.expander(f"📄 {result['Resume']} - Score: {result['Total Score']} ({result['Verdict']})", expanded=True):

                            # Create columns for better layout
                            col1, col2 = st.columns([2, 1])

                            with col1:
                                st.markdown(f"**📊 Total Score:** {result['Total Score']}")
                                st.markdown(f"**🎯 Verdict:** {result['Verdict']}")

                                if result.get('Missing Skills'):
                                    st.markdown(f"**❌ Missing Skills:** {', '.join(result['Missing Skills'])}")
                                else:
                                    st.markdown("**✅ All required skills found!**")

                                if result.get('Feedback'):
                                    st.markdown(f"**💡 Feedback:** {result['Feedback']}")

                                if result.get('Processing Time'):
                                    st.markdown(f"**⏱️ Processing Time:** {result['Processing Time']} seconds")

                            with col2:
                                # Verdict color coding
                                if result['Verdict'] == 'High':
                                    st.success("🟢 High Match")
                                elif result['Verdict'] == 'Medium':
                                    st.warning("🟡 Medium Match")
                                else:
                                    st.error("🔴 Low Match")

                    st.markdown("---")
                    st.success("✅ **Processing completed successfully!**")

                else:
                    st.warning("⚠️ No resumes met the minimum score criteria. Try adjusting the score filter.")

    # Sample data section
    st.markdown("### 📋 How It Works")

    with st.expander("🔍 See Sample Analysis", expanded=False):
        st.markdown("""
        **1. Upload Job Description**
        - Supports TXT and PDF formats
        - Automatically extracts required skills and qualifications

        **2. Upload Candidate Resumes**
        - Batch upload multiple PDF resumes
        - Real-time processing with progress indicators

        **3. Get Intelligent Results**
        - Comprehensive scoring based on skill matching
        - Semantic analysis for contextual understanding
        - Detailed feedback and recommendations

        **4. Analyze & Export**
        - Interactive charts and analytics
        - Export results in multiple formats
        - Advanced filtering and sorting options
        """)

    # Tips section
    st.markdown("### 💡 Tips for Best Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Job Description Tips:**
        - Include specific technical skills
        - Mention required experience levels
        - Add preferred qualifications
        - Use clear, structured language
        """)

    with col2:
        st.markdown("""
        **Resume Tips:**
        - Ensure PDFs are text-readable
        - Use standard resume formats
        - Include relevant keywords
        - Keep file sizes reasonable
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 AI Resume Screening Dashboard | Built with Streamlit & Advanced NLP</p>
    <p><small>For support or feedback, contact your system administrator</small></p>
</div>
""", unsafe_allow_html=True)
