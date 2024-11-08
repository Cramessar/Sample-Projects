import os

def get_openai_api_key():
    """Retrieve the OpenAI API key from an environment variable."""
    return os.getenv("OPENAI_API_KEY")
