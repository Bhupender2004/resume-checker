import streamlit as st

# Page configuration
st.set_page_config(
    page_title="UI Test",
    page_icon="🧪",
    layout="wide"
)

# Test the basic UI components
st.title("🧪 UI Test - Resume Screening Dashboard")

# Test tabs
tab1, tab2, tab3 = st.tabs(["📝 Test Tab 1", "🔍 Test Tab 2", "📊 Test Tab 3"])

with tab1:
    st.markdown("## Tab 1 Content")
    st.write("This is tab 1 content")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Column 1")
        st.write("Content in column 1")
    
    with col2:
        st.markdown("### Column 2")
        st.write("Content in column 2")

with tab2:
    st.markdown("## Tab 2 Content")
    st.write("This is tab 2 content")

with tab3:
    st.markdown("## Tab 3 Content")
    st.write("This is tab 3 content")

# Test file uploader
st.markdown("---")
st.markdown("## File Upload Test")
uploaded_file = st.file_uploader("Test file upload", type=["txt", "pdf"])

if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

# Test buttons
st.markdown("---")
st.markdown("## Button Test")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Primary Button", type="primary"):
        st.success("Primary button clicked!")

with col2:
    if st.button("Secondary Button"):
        st.info("Secondary button clicked!")

with col3:
    if st.button("Warning Button"):
        st.warning("Warning button clicked!")

# Test metrics
st.markdown("---")
st.markdown("## Metrics Test")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Test Metric 1", "100", "10")

with col2:
    st.metric("Test Metric 2", "85%", "-5%")

with col3:
    st.metric("Test Metric 3", "42", "2")

st.markdown("---")
st.success("✅ UI Test Complete - All components working!")
