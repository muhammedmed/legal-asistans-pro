import requests
import json
import time

def ask_legal_question(question, jurisdiction, legal_area, api_key):
    """
    Ask a legal question using BigModel API
    
    Args:
        question: The legal question to ask
        jurisdiction: The relevant legal jurisdiction
        legal_area: The area of law
        api_key: BigModel API key
    
    Returns:
        Dictionary containing the answer
    """
    # Prepare the prompt for the API
    prompt = f"""Please provide an informational answer to the following legal question. 
The question pertains to the jurisdiction of {jurisdiction} and the legal area of {legal_area}.

QUESTION: {question}

Please provide a clear, accurate, and informative response based on your training data. 
Include relevant legal principles, statutes, or case law if appropriate.
End your response with a brief disclaimer noting that this is not legal advice.

Format your response in markdown for readability."""

    # Call BigModel API
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "glm-4", # Using GLM-4 model from BigModel
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        
        response = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            return {"answer": answer}
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return generate_error_response(response.text)
    
    except Exception as e:
        print(f"Exception during API call: {e}")
        return generate_error_response(str(e))

def generate_error_response(error_text):
    """Generate an error response when API call fails"""
    return {
        "answer": f"""
## Unable to Process Your Question

I apologize, but I couldn't process your question due to a technical issue:

```
{error_text[:100]}...
```

Please check your API key and internet connection, then try again. If the issue persists, the service might be temporarily unavailable.

**Disclaimer**: This system provides informational responses only, not legal advice.
"""
    }