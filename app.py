import streamlit as st
import os
import tempfile
from contract_analyzer import analyze_contract
from legal_qa import ask_legal_question

# Set Streamlit page configuration
st.set_page_config(
    page_title="Legal Assistant Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        margin-bottom: 1rem;
    }
    .card {
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 10px;
        background-color: #F3F4F6;
    }
    .risk-high {
        color: #DC2626;
        font-weight: bold;
    }
    .risk-medium {
        color: #F59E0B;
        font-weight: bold;
    }
    .risk-low {
        color: #10B981;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Get API Key from environment variable if available, otherwise from user input
    default_api_key = os.environ.get("BIGMODEL_API_KEY", "")
    
    # Sidebar - API Configuration
    with st.sidebar:
        st.markdown("### API Configuration")
        api_key = st.text_input("BigModel API Key", value=default_api_key, type="password")
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **Legal Assistant Pro** helps legal professionals:
        - Analyze contracts for potential risks
        - Get answers to legal questions using AI
        
        This tool is for informational purposes only and does not constitute legal advice.
        """)
    
    # Main Page Header
    st.markdown("<h1 class='main-header'>Legal Assistant Pro</h1>", unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["📄 Contract Analyzer", "💬 Legal Q&A Chatbot"])
    
    # Contract Analyzer Tab
    with tab1:
        st.markdown("<h2 class='sub-header'>Contract Analyzer</h2>", unsafe_allow_html=True)
        st.markdown("""
        Upload a contract document (PDF) to analyze it for potential legal risks, 
        obligations, and important clauses.
        """)
        
        uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])
        
        if uploaded_file is not None:
            with st.spinner('Analyzing contract...'):
                # Save the uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_file_path = tmp_file.name
                
                try:
                    # Analyze the contract
                    analysis_results = analyze_contract(temp_file_path, api_key)
                    
                    # Display the results
                    st.markdown("### Analysis Results")
                    
                    # Contract Summary
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("#### 📝 Contract Summary")
                    st.markdown(analysis_results["summary"])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Key Provisions
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("#### 📋 Key Provisions")
                    for provision in analysis_results["key_provisions"]:
                        st.markdown(f"- **{provision['title']}**: {provision['description']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Risk Assessment
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("#### ⚠️ Risk Assessment")
                    for risk in analysis_results["risks"]:
                        risk_class = f"risk-{risk['level'].lower()}"
                        st.markdown(f"- <span class='{risk_class}'>{risk['level'].upper()}</span>: {risk['description']}", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Recommendations
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("#### 💡 Recommendations")
                    for rec in analysis_results["recommendations"]:
                        st.markdown(f"- {rec}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                finally:
                    # Clean up the temporary file
                    os.unlink(temp_file_path)
    
    # Legal Q&A Chatbot Tab
    with tab2:
        st.markdown("<h2 class='sub-header'>Legal Q&A Chatbot</h2>", unsafe_allow_html=True)
        st.markdown("""
        Ask legal questions about laws, regulations, or legal principles across different jurisdictions.
        The AI will provide informational responses based on its training data.
        """)
        
        # Initialize chat history if not already done
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Jurisdiction selection
        jurisdiction = st.selectbox(
            "Select Jurisdiction",
            ["United States (Federal)", "California", "New York", "Texas", "United Kingdom", "European Union", "International Law", "Other"]
        )
        
        # Legal area selection
        legal_area = st.selectbox(
            "Select Legal Area",
            ["Contract Law", "Corporate Law", "Intellectual Property", "Employment Law", "Tax Law", "Real Estate", "Data Privacy", "General"]
        )
        
        # Question input
        user_question = st.text_area("Enter your legal question:", height=100)
        
        if st.button("Submit Question"):
            if not user_question:
                st.error("Please enter a question.")
            elif not api_key:
                st.error("Please enter your BigModel API key in the sidebar.")
            else:
                with st.spinner('Getting answer...'):
                    response = ask_legal_question(user_question, jurisdiction, legal_area, api_key)
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_question, response["answer"]))
                    
                    # Display response
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("### Response:")
                    st.markdown(response["answer"])
                    
                    # Display disclaimer
                    st.markdown("---")
                    st.markdown("""
                    **Disclaimer**: This information is provided for educational purposes only and does not 
                    constitute legal advice. Consult with a qualified attorney for specific legal guidance.
                    """)
                    st.markdown("</div>", unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### Previous Questions")
            for i, (q, a) in enumerate(st.session_state.chat_history):
                st.markdown(f"**Question {i+1}**: {q}")
                st.markdown(f"**Answer**: {a}")
                st.markdown("---")

if __name__ == "__main__":
    main()