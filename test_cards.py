import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Card Test",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        color: #333333;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    .metric-card h4 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-card p {
        color: #555555;
        margin-bottom: 0;
        line-height: 1.5;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .test-card-dark {
        background: #2c3e50;
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    
    .test-card-light {
        background: #f8f9fa;
        color: #333333;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Card Contrast Test")

st.markdown("## Testing Different Card Styles")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Fixed Metric Cards")
    st.markdown("""
    <div class="metric-card">
        <h4>🧠 AI-Powered Analysis</h4>
        <p>This card should now have proper contrast with dark text on white background.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Dark Theme Card")
    st.markdown("""
    <div class="test-card-dark">
        <h4>📊 Dark Card</h4>
        <p>This is a dark card with white text for comparison.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("### Light Theme Card")
    st.markdown("""
    <div class="test-card-light">
        <h4>⚡ Light Card</h4>
        <p>This is a light card with dark text for comparison.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Key Features Test")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>🧠 AI-Powered Analysis</h4>
        <p>Advanced NLP and machine learning algorithms analyze resumes for skill matching and semantic similarity.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>📊 Interactive Analytics</h4>
        <p>Comprehensive dashboards with charts, statistics, and insights to help you make informed decisions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>⚡ Fast Processing</h4>
        <p>Process multiple resumes simultaneously with real-time progress tracking and instant results.</p>
    </div>
    """, unsafe_allow_html=True)

st.success("✅ All cards should now have proper contrast and be easily readable!")
