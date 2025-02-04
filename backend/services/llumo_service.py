# services/llumo_service.py

import os
import json
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

def evaluate_with_llumo(prompt, context, output):
    LLUMO_API_KEY = os.getenv("LLUMO_API_KEY")
    
    LLUMO_ENDPOINT = "https://app.llumo.ai/api/create-eval-analytics"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLUMO_API_KEY}",
    }

    payload = {
        "prompt": prompt,
        "input": {
            "context": context,
            "evaluation_criteria": "CLARITY: Response must be well-structured, use precise language, have clear sections, and present information logically. CONFIDENCE: Response should use assertive language and be well-supported by context. CONTEXT: Response must align with and use information from the provided context appropriately."
        },
        "output": output,
        "analytics": ["Clarity", "Confidence", "Context"],
        "scoring_guide": """
        Clarity scoring criteria:
        - Well-structured sections
        - Simple language.
        
        Confidence scoring criteria:
        - Use of direct statements
        - Support from context
        - Consistent tone
        
        Context scoring criteria:
        - Information accuracy
        - Relevant details
        - Proper context use
        """
    }

    try:
        logging.info(f"Sending payload to LLUMO: {json.dumps(payload, indent=2)}")
        response = requests.post(LLUMO_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        logging.info(f"LLUMO raw response: {json.dumps(result, indent=2)}")
        
        if "data" in result:
            try:
                data = json.loads(result["data"]["data"])
                return data, True
            except json.JSONDecodeError:
                return result["data"], True
        return {}, False

    except Exception as error:
        logging.error(f"Error in LLUMO evaluation: {str(error)}")
        return {}, False