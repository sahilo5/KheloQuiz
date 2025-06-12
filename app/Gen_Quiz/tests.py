from django.test import TestCase

import requests
import json

def get_api_response():

    prompt = "Generate a JSON object containing 5 multiple-choice questions on the topic: Java."
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": [
        {
            "role": "user",
            "content": prompt
        }
        ],   
    })
    ) 

    try:
        return response.json()
    except json.JSONDecodeError:
        print("❌ Error decoding JSON response.")
        return {}  
    

def main():
    api_response = get_api_response()
    print("Full API Response:\n", json.dumps(api_response, indent=4))

    if "choices" in api_response:
        print("\nAI Response:\n", api_response["choices"][0]["message"]["content"])
    else:
        print("\n❌ 'choices' key not found. Response might be an error or invalid.")
    


if __name__ =="__main__":
    main()
