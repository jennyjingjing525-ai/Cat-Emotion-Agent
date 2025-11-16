# emotion_logic.py (Revised for KEY.env)
import os 
from dotenv import load_dotenv # Import the dotenv loader!

import sys
import google.adk
print(f"--- Environment Check ---")
print(f"Python Executable: {sys.executable}")
print(f"ADK Version: {google.adk.__version__}")
print(f"--- Check Complete ---")

def run_adk_check():
    print(f"\n--- SERVER-SIDE ADK CHECK ---")
    print(f"Python Executable: {sys.executable}")
    print(f"ADK Version: {google.adk.__version__}")

    # Test an Agent object directly
    from google.adk.agents import Agent
    from google.adk.models.google_llm import Gemini
    try:
        test_agent = Agent(name="Test", model=Gemini(model="gemini-2.5-flash"))
        # If this line runs, the ADK is correctly configured:
        print(f"Agent object created successfully.")
        # Verify the run attribute exists
        if hasattr(test_agent, 'run'):
             print(".run() attribute found on agent object.")
        else:
             print("!!! CRITICAL: .run() attribute is MISSING on agent object.")
    except Exception as e:
        print(f"Agent creation failed: {e}")
    print(f"--- CHECK END ---\n")

# Call this function when the server starts
run_adk_check()

# --- Load Environment Variables ---
# Use the filename 'KEY.env' to load your secret API key
load_dotenv(dotenv_path='KEY.env') 

from google.adk.agents import Agent as ADKAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool, google_search 
from google.genai import types

print("✅ ADK components imported successfully.")

# --- 1. Define the Custom Tool Function (New Ability) ---
def get_cat_breed_info(breed: str) -> str:
    """
    Looks up descriptive information about a specific cat breed.
    The Agent can use this tool if it decides the cat's breed is relevant
    to the emotion analysis. (Simulated tool response)
    """
    if "siamese" in breed.lower():
        return "Siamese cats are known for being very vocal and often display an intense, 'sassy' expression which can be mistaken for anger or demand. They are highly social."
    elif "ragdoll" in breed.lower():
        return "Ragdolls are known for their relaxed and floppy posture, often appearing more docile or 'relaxed' than other breeds when handled."
    else:
        return f"Information for breed '{breed}' not found. No specific breed traits to consider."

# --- 2. Initialize the ADK Components ---

# 2a. Define Retry Options (for robustness)
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# 2b. Define the Agent's specific instruction
SYSTEM_INSTRUCTION = (
    "You are the Cat Emotion Analysis Agent. Your primary goal is to analyze "
    "the provided image of a cat. You must identify the cat's dominant emotion "
    "(e.g., Happy, Angry, Fearful, Curious, Relaxed) and provide a concise, "
    "detailed explanation (2-3 sentences) based on observable visual cues. "
    "You can use the provided tools if they help you perform a better analysis."
)

# 2c. Create the Agent
# The ADK automatically reads the GEMINI_API_KEY from os.environ
cat_emotion_agent = ADKAgent(
    # ADD A UNIQUE NAME HERE (REQUIRED)
    name="CatEmotionAnalyzer",
    model=Gemini(
        model="gemini-2.5-flash", # Use a stable model name
        system_instruction=SYSTEM_INSTRUCTION,
    ),
    # Register the tools the agent can use
    tools=[
        FunctionTool(get_cat_breed_info),
        google_search # Adding a general tool for context
    ]
)

# --- 3. The new core analysis function ---
def analyze_emotion_with_adk(base64_image: str, mime_type: str, prompt: str) -> str:
    """
    Uses the pre-defined ADK Agent to process the multimodal request.
    """
    
    # Construct the multimodal content parts for the Agent
    contents = [
        {"text": prompt},
        {
            "inlineData": {
                "mimeType": mime_type,
                "data": base64_image
            }
        }
    ]
    
    # Run the agent
    # The ADK Agent automatically decides if it needs to use get_cat_breed_info or google_search
    # before generating the final response.
    try:
        response = cat_emotion_agent(contents=contents)
        return response.text
    except Exception as e:
        return f"Error: ADK Agent failed to run. Details: {e}"
    