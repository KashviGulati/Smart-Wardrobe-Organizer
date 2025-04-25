import google.generativeai as genai
from datetime import datetime

# Your API key (change this as needed)
HARDCODED_API_KEY = "AIzaSyC17k9wzhBECj7xunWMU3KrqNbU_LMm4tg"

# The model you want to use
MODEL_NAME = "gemini-1.5-flash-8b-001"  # Specify the model name here

def initialize_gemini(api_key=None):
    api_key = api_key or HARDCODED_API_KEY
    genai.configure(api_key=api_key)
    return True

def get_fashion_advice(prompt, api_key=None, temperature=0.7):
    try:
        api_key = api_key or HARDCODED_API_KEY
        genai.configure(api_key=api_key)

        # Initialize the specific model
        model = genai.GenerativeModel(MODEL_NAME)
        chat = model.start_chat(history=[])

        enhanced_prompt = f"""
        You are a professional fashion advisor. The user needs advice on fashion choices.
        Provide helpful, specific and friendly fashion advice based on the following query:

        {prompt}

        Current date: {datetime.now().strftime('%B %d, %Y')}
        """

        response = chat.send_message(enhanced_prompt)
        return response.text

    except Exception as e:
        return f"Error getting fashion advice: {str(e)}"

# Example Usage
response = get_fashion_advice("What should I wear for a formal event this weekend?")
print(response)
