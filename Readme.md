# Legal Assistant Pro

A Streamlit application that combines contract analysis and legal Q&A functionality using the BigModel API.

## Features

1. **Contract Analyzer**: Upload and analyze contracts (PDF format) to identify:
   - Contract summary
   - Key provisions
   - Risk assessment
   - Recommendations

2. **Legal Q&A Chatbot**: Ask legal questions about different legal areas across various jurisdictions

## Setup Instructions

### Prerequisites

- Python 3.7+
- BigModel API key (from https://open.bigmodel.cn/)

### Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the App

1. Navigate to the project directory in your terminal
2. Launch the Streamlit app:

```bash
streamlit run app.py
```

3. The app will open in your web browser (typically at http://localhost:8501)
4. Enter your BigModel API key in the sidebar
5. Use the tabs to navigate between Contract Analyzer and Legal Q&A functionality

## Usage

### Contract Analyzer

1. Select the "Contract Analyzer" tab
2. Upload a contract document (PDF format)
3. Wait for the analysis to complete
4. Review the summary, key provisions, risk assessment, and recommendations

### Legal Q&A Chatbot

1. Select the "Legal Q&A Chatbot" tab
2. Choose the relevant jurisdiction and legal area
3. Enter your legal question in the text area
4. Click "Submit Question"
5. Review the answer provided by the AI

## Important Notes

- This application is for informational purposes only and does not constitute legal advice
- The quality of analysis depends on the clarity of the PDF text and the capabilities of the BigModel API
- Your API key is required for both functionalities but is not stored permanently

## Customization

You can modify the code to:
- Add more jurisdictions or legal areas
- Customize the styling and layout
- Implement additional features like saving analysis results or chat history

## Troubleshooting

- If you get an error, make sure your API key is correctly entered
- Ensure your PDF document contains extractable text
- Check your internet connection