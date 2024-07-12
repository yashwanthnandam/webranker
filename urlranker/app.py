from .controllers import HTMLProcessingController
from dotenv import load_dotenv
from .use_cases import GPTService
import os

def create_app():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    print("printing api key ---------------------------->")
    print(api_key)
    if not api_key:
        print("Error: OPENAI_API_KEY not found in the environment variables.")
        return None 
    model_name = "gpt-3.5-turbo"
    gpt_service = GPTService(api_key,model_name)
    controller = HTMLProcessingController(gpt_service)
    return controller
