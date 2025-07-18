import streamlit as st
import pandas as pd
import io
import json
from utils.data_cleaner import clean_data, detect_column_types, validate_file
from utils.chart_generator import generate_smart_charts
from utils.kpi_cards import display_kpis
from utils.gemini_summary import get_data_analysis, get_insights, get_financial_analysis
from utils.simplified_bi_agent import SimplifiedBIAgent

# Page Configuration
st.set_page_config(
    layout="wide", 
    page_title="Business Intelligence Agent",
    page_icon="📊"
)

# Custom CSS for clean UI
st.markdown("""
<style>
    .main-header {
        font-size: 24px;
        font-weight: 600;
        color: #1f1f1f;
        margin-bottom: 10px;
    }
    .step-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #007acc;
    }
    .step-title {
        font-size: 18px;
        font-weight: 600;
        color: #007acc;
        margin-bottom: 10px;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Business Intelligence Agent</h1>', unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = None
if 'analysis_goals' not in st.session_state:
    st.session_state.analysis_goals = []

# API Key - Using your provided key
GEMINI_API_KEY = "AIzaSyDzTSzogzG7ntlLHBOoHISaKC12g4ljW-s"

# Initialize BI Agent
bi_agent = SimplifiedBIAgent(GEMINI_API_KEY)

# Step 1: Data Input
st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown('<div class="step-title">Step 1: Request Data Input</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📁 Upload your data file (Excel, CSV, PDF, or Text)", 
    type=["csv", "xlsx", "pdf", "txt"],
    help="Upload business data like financial reports, sales data, etc."
)

if uploaded_file:
    # Validate file
    is_valid, message = validate_file(uploaded_file)
    if is_valid:
        st.success(f"✅ File validated successfully: {message}")
        
        # Process different file types
        if uploaded_file.name.endswith(('.csv', '.xlsx')):
            try:
                if uploaded_file.name.endswith(".csv"):
                    df_raw = pd.read_csv(uploaded_file)
                else:
                    df_raw = pd.read_excel(uploaded_file)
                
                st.session_state.data = df_raw
                st.session_state.step = 2
                
                st.write("**Data Preview:**")
                st.dataframe(df_raw, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        elif uploaded_file.name.endswith('.pdf') or uploaded_file.name.endswith('.txt'):
            # Handle PDF/Text files with AI extraction
            content = uploaded_file.read()
            if uploaded_file.name.endswith('.txt'):
                content = content.decode('utf-8')
            
            extracted_data = bi_agent.extract_data_from_document(content, uploaded_file.name)
            if extracted_data:
                st.success("✅ Data extracted from document successfully!")
                st.text_area("Extracted Content:", extracted_data, height=200)
                st.session_state.data = extracted_data
                st.session_state.step = 2
            else:
                st.error("❌ Could not extract usable data from the document.")
                
    else:
        st.error(f"❌ File validation failed: {message}")

st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Analyze and Preprocess Data
if st.session_state.step >= 2 and st.session_state.data is not None:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 2: Analyze and Preprocess the Data</div>', unsafe_allow_html=True)
    
    if isinstance(st.session_state.data, pd.DataFrame):
        df = st.session_state.data
        
        # Clean and analyze data
        df_clean = clean_data(df)
        types = detect_column_types(df_clean)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Data Quality Summary:**")
            st.write(f"- Rows: {len(df)}")
            st.write(f"- Columns: {len(df.columns)}")
            st.write(f"- Missing values: {df.isnull().sum().sum()}")
            st.write(f"- Duplicates: {df.duplicated().sum()}")
        
        with col2:
            st.write("**Column Types Detected:**")
            for col, dtype in types.items():
                st.write(f"- {col}: {dtype}")
        
        st.write("**Cleaned Data Preview:**")
        st.dataframe(df_clean, use_container_width=True)
        
        # Statistical Summary
        if len(df_clean.select_dtypes(include=['number']).columns) > 0:
            st.write("**Statistical Summary:**")
            st.dataframe(df_clean.describe(), use_container_width=True)
        
        st.session_state.cleaned_data = df_clean
        st.session_state.data_types = types
        st.session_state.step = 3
        
    st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Define Analysis Goals
if st.session_state.step >= 3:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 3: Define Analysis Goals</div>', unsafe_allow_html=True)
    
    st.write("**What insights are you looking for?**")
    
    # Predefined analysis templates
    analysis_templates = [
        "Show me revenue trends over time",
        "Identify top-performing products/categories", 
        "Analyze profit margins and expenses",
        "Calculate financial ratios (ROE, ROA, etc.)",
        "Year-over-year growth analysis",
        "Customer segmentation analysis",
        "Seasonal patterns and forecasting",
        "Custom analysis"
    ]
    
    selected_goals = st.multiselect(
        "Select analysis objectives:",
        analysis_templates,
        default=st.session_state.analysis_goals
    )
    
    # Custom analysis input
    custom_analysis = st.text_area(
        "Or describe your specific analysis requirements:",
        placeholder="e.g., What is the YoY growth in revenue, profit margins by region, etc.",
        height=100
    )
    
    if custom_analysis:
        selected_goals.append(custom_analysis)
    
    st.session_state.analysis_goals = selected_goals
    
    if selected_goals:
        if st.button("🚀 Start Analysis", type="primary"):
            st.session_state.step = 4
    
    st.markdown('</div>', unsafe_allow_html=True)

# Step 4: Present Results
if st.session_state.step >= 4 and hasattr(st.session_state, 'cleaned_data'):
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 4: Present Results</div>', unsafe_allow_html=True)
    
    df_clean = st.session_state.cleaned_data
    types = st.session_state.data_types
    goals = st.session_state.analysis_goals
    
    # KPI Dashboard
    st.subheader("📊 Key Performance Indicators")
    display_kpis(df_clean, types)
    
    # Visualizations
    st.subheader("📈 Data Visualizations")
    generate_smart_charts(df_clean, types, GEMINI_API_KEY)
    
    # AI-Powered Analysis
    st.subheader("🤖 AI-Powered Insights")
    
    with st.spinner("Generating AI insights..."):
        insights = bi_agent.generate_comprehensive_analysis(df_clean, goals)
        if insights:
            st.markdown(insights)
    
    st.session_state.step = 5
    st.markdown('</div>', unsafe_allow_html=True)

# Step 5: Financial Analysis & Q&A
if st.session_state.step >= 5 and hasattr(st.session_state, 'cleaned_data'):
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 5: Interactive Analysis & Q&A</div>', unsafe_allow_html=True)
    
    st.write("**Ask specific questions about your data:**")
    
    # Common financial questions
    common_questions = [
        "What is the YoY growth in revenue?",
        "What is the return on capital employed?",
        "Calculate debt-to-equity ratio",
        "Show profit margin trends",
        "Identify expense categories with highest growth",
        "What are the key risk factors?",
        "Compare quarterly performance"
    ]
    
    selected_question = st.selectbox("Select a common question:", ["Custom question"] + common_questions)
    
    if selected_question == "Custom question":
        user_question = st.text_input("Enter your question:", placeholder="e.g., What drove the increase in operating expenses?")
    else:
        user_question = selected_question
    
    if user_question and st.button("🔍 Get Answer"):
        with st.spinner("Analyzing..."):
            answer = bi_agent.answer_question(st.session_state.cleaned_data, user_question)
            if answer:
                st.write("**Answer:**")
                st.markdown(answer)
    
    st.session_state.step = 6
    st.markdown('</div>', unsafe_allow_html=True)

# Step 6: Feedback and Next Steps
if st.session_state.step >= 6:
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-title">Step 6: Feedback & Next Steps</div>', unsafe_allow_html=True)
    
    # Export options
    st.subheader("📤 Export Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Dashboard as PDF"):
            st.info("PDF export feature coming soon!")
    
    with col2:
        if st.button("📈 Export Charts"):
            st.info("Chart export feature coming soon!")
    
    with col3:
        if hasattr(st.session_state, 'cleaned_data'):
            csv = st.session_state.cleaned_data.to_csv(index=False)
            st.download_button(
                label="💾 Download Cleaned Data",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
    
    # Feedback
    st.subheader("💬 Feedback")
    satisfaction = st.radio(
        "Does this analysis answer your questions?",
        ["Yes, fully satisfied", "Partially satisfied", "Need more analysis"]
    )
    
    if satisfaction == "Need more analysis":
        additional_requests = st.text_area(
            "What additional analysis would you like?",
            placeholder="Describe what you'd like to explore further..."
        )
        
        if additional_requests and st.button("🔄 Request Additional Analysis"):
            st.session_state.analysis_goals.append(additional_requests)
            st.session_state.step = 4  # Go back to analysis
            st.rerun()
    
    # Suggested next steps
    st.subheader("🎯 Suggested Next Steps")
    suggestions = bi_agent.get_next_step_suggestions(st.session_state.analysis_goals)
    if suggestions:
        st.markdown(suggestions)
    
    # Reset option
    if st.button("🔄 Start New Analysis"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
