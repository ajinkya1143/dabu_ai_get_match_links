from prompts import GENERATE_SEARCH_QUERY_PROMPT
import requests

def generate_payload(prompt, images=None):
    if images:
        content = [
            {"type": "text", "text": prompt},
            # Assuming the first image is the main image
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{images[0]}", "detail": "low", "role": "main"}},
            # Add each frame as an image URL
            *[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img}",
                        "detail": "low",
                        "role": "frame"  # Specify that these are frames
                    }
                }
                for img in images[1:]  # Skip the first one since it's already added
            ]
        ]
        messages = [{"role": "user", "content": content}]
        payload = {
            "model": "gpt-4o-2024-08-06",
            "messages": messages,
            "max_tokens": 1000,
        }
    else:
        content = prompt
        messages = [{"role": "user", "content": content}]

        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "max_tokens": 200,
        }
    return payload


def generate_content(messages, images=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer *******",   #Add Open AI key Here
    }

    payload = generate_payload(messages, images)
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload,
                                 timeout=30)
        response_data = response.json()
        if 'choices' not in response_data or not response_data['choices']:
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            print(f"OpenAI API error: {error_message}")
        else:
            return response_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)

    return response


def get_search_query(title, description):
    messages = GENERATE_SEARCH_QUERY_PROMPT.format(title=title, description=description)
    return generate_content(messages)



def get_embedding(text):
    headers = {
        "Authorization": "Bearer ********",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    response = requests.post('https://api.openai.com/v1/embeddings', headers=headers, json=data, timeout=30)
    response_data = response.json()
    # print(f"OpenAI Embedding API response: {json.dumps(response_data, indent=2)}")
    if 'data' not in response_data or not response_data['data']:
        error_message = response_data.get('error', {}).get('message', 'Unknown error')
        print(f"OpenAI Embedding API error: {error_message}")
        raise ValueError(f"OpenAI Embedding API error: {error_message}")
    return response_data['data'][0]['embedding']

def get_text_embedding(text: str):
    try:
        return get_embedding(text)
    except Exception as e:
        print(f"Error in get_text_embedding: {str(e)}")
