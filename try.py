import google.generativeai as genai

def list_available_models(api_key):
    genai.configure(api_key=api_key)
    try:
        models = genai.list_models()  # Get the list of available models
        print("Available Models:")
        for model in models:
            print(model)  # Print the entire model object to inspect its structure
    except Exception as e:
        print(f"Error fetching models: {str(e)}")

# Example usage
list_available_models('AIzaSyC17k9wzhBECj7xunWMU3KrqNbU_LMm4tg')
