import requests
import json
import PyPDF2
import base64
import time

def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        text = ""
    
    return text

def analyze_contract(pdf_path, api_key):
    """
    Analyze contract using BigModel API
    
    Args:
        pdf_path: Path to the contract PDF file
        api_key: BigModel API key
    
    Returns:
        Dictionary containing analysis results
    """
    # Extract text from PDF
    contract_text = extract_text_from_pdf(pdf_path)
    
    if not contract_text.strip():
        return {
            "summary": "Error: Could not extract text from the PDF file.",
            "key_provisions": [],
            "risks": [],
            "recommendations": ["Please upload a valid PDF file with extractable text."]
        }
    
    # Prepare the prompt for the API
    prompt = f"""Please analyze the following contract. Provide:
1. A concise summary of the contract (1-2 paragraphs)
2. Key provisions (identify 3-5 most important clauses)
3. Risk assessment (identify high, medium, and low risks)
4. Recommendations for addressing potential issues

Contract Text:
{contract_text[:5000]}...  # Truncating to first 5000 chars for API limits

Format your response in JSON with the following structure:
{{
  "summary": "Contract summary here",
  "key_provisions": [
    {{"title": "Provision title", "description": "Description"}},
    ...
  ],
  "risks": [
    {{"level": "high/medium/low", "description": "Risk description"}},
    ...
  ],
  "recommendations": [
    "Recommendation 1",
    ...
  ]
}}
"""

    # Call BigModel API
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "glm-4",  # Using GLM-4 model from BigModel
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis_text = result['choices'][0]['message']['content']
            
            # Parse the JSON response
            try:
                analysis_data = json.loads(analysis_text)
                return analysis_data
            except json.JSONDecodeError:
                # In case the API doesn't return valid JSON
                return fallback_analysis(analysis_text)
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return generate_error_analysis(response.text)
    
    except Exception as e:
        print(f"Exception during API call: {e}")
        return generate_error_analysis(str(e))

def fallback_analysis(text):
    """Generate a structured analysis from unstructured text"""
    return {
        "summary": "The contract analysis could not be properly formatted. Raw analysis is provided below.",
        "key_provisions": [{"title": "Raw Analysis", "description": text[:1000] + "..."}],
        "risks": [{"level": "medium", "description": "Analysis format error - please try again or review manually"}],
        "recommendations": ["Review the contract manually", "Try uploading a cleaner PDF version"]
    }

def generate_error_analysis(error_text):
    """Generate an error response when API call fails"""
    return {
        "summary": "An error occurred during contract analysis.",
        "key_provisions": [],
        "risks": [{"level": "high", "description": "Analysis couldn't be completed due to technical issues"}],
        "recommendations": [
            "Check your API key",
            "Ensure the PDF contains extractable text",
            "Try again later or contact support"
        ]
    }