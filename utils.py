import os
import json
from datetime import datetime, timedelta
import google.generativeai as genai
from google.generativeai import types

def initialize_gemini():
    """Initialize and return the Gemini API client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    genai.configure(api_key=api_key)
    return genai

def create_prompt(user_input):
    """Create the prompt for Gemini API based on user input."""
    # Calculate number of days
    start_date = datetime.strptime(user_input["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(user_input["end_date"], "%Y-%m-%d")
    num_days = (end_date - start_date).days + 1
    
    # Few-shot examples to guide the model
    few_shot_examples = []
    
    # Luxury example
    if user_input["budget"] == "luxury":
        few_shot_examples.append(
            {
                "style": "luxury",
                "output": """
                {
                  "day": 1,
                  "summary": "Arrival and indulgence in local gourmet",
                  "morning": "Check into a 5-star ryokan in Gion.",
                  "afternoon": "Explore Nishiki Market with a private food guide.",
                  "evening": "Dinner at Michelin-starred Kikunoi."
                }
                """
            }
        )
    
    # Budget example
    elif user_input["budget"] == "budget":
        few_shot_examples.append(
            {
                "style": "budget",
                "output": """
                {
                  "day": 1,
                  "summary": "Arrival and local exploration",
                  "morning": "Check into a budget-friendly hostel near the train station.",
                  "afternoon": "Free walking tour of the historical district.",
                  "evening": "Dinner at a popular local street food market."
                }
                """
            }
        )
    
    # Moderate example
    else:
        few_shot_examples.append(
            {
                "style": "moderate",
                "output": """
                {
                  "day": 1,
                  "summary": "Arrival and cultural immersion",
                  "morning": "Check into a comfortable mid-range hotel.",
                  "afternoon": "Visit main cultural attractions with audio guide.",
                  "evening": "Dinner at a well-reviewed local restaurant."
                }
                """
            }
        )
    
    # Build the prompt
    examples_text = "\n".join([f"Style: {ex['style']}\nOutput: {ex['output']}" for ex in few_shot_examples])
    interests_text = ", ".join(user_input["interests"])
    
    prompt = f"""
    You are a professional travel planner specializing in {user_input["budget"]} travel experiences.
    
    Create a detailed {num_days}-day travel itinerary for {user_input["destination"]} from {user_input["start_date"]} to {user_input["end_date"]}.
    
    The traveler is particularly interested in: {interests_text}
    Budget level: {user_input["budget"]}
    
    For each day, generate a JSON object with the following structure:
    {{
      "day": [day number],
      "summary": [brief summary of the day],
      "morning": [detailed morning activity],
      "afternoon": [detailed afternoon activity],
      "evening": [detailed evening activity]
    }}
    
    Here are examples of how to structure each day based on the selected budget level:
    
    {examples_text}
    
    For this traveler, create a complete itinerary with all {num_days} days following this style and structure.
    Return the results as a JSON array of day objects, with one object per day.
    Make sure all JSON is properly formatted and can be parsed.
    """
    
    return prompt

def generate_itinerary(client, user_input):
    """Generate a travel itinerary using the Gemini API."""
    # Create the prompt
    prompt = create_prompt(user_input)
    
    # Configure the model
    model = client.GenerativeModel('gemini-1.5-pro')
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    # Generate the response
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )
    
    # Extract and parse the JSON itinerary from the response
    try:
        response_text = response.text
        
        # Look for JSON array in the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_text = response_text[start_idx:end_idx]
            itinerary = json.loads(json_text)
            return itinerary
        else:
            # Try to find individual JSON objects if array not found
            itinerary = []
            lines = response_text.split('\n')
            current_json = ""
            capture = False
            
            for line in lines:
                if line.strip().startswith('{'):
                    capture = True
                    current_json = line
                elif line.strip().endswith('}') and capture:
                    current_json += line
                    try:
                        day_data = json.loads(current_json)
                        itinerary.append(day_data)
                        current_json = ""
                        capture = False
                    except:
                        current_json += line
                elif capture:
                    current_json += line
            
            if itinerary:
                return itinerary
            else:
                # Last resort: try to parse the whole text as JSON
                try:
                    return json.loads(response_text)
                except:
                    raise ValueError("Could not parse the API response as JSON")
    except Exception as e:
        raise ValueError(f"Error parsing itinerary: {str(e)}")

    return None
