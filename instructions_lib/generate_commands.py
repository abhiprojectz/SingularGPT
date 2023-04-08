import requests
import json
from dotenv import load_dotenv
import os
from instructions_lib.fetch_commands import load_prompt 
from instructions_lib.process_instructions import generate_script, execute_commands 


load_dotenv()


class OpenAI_API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.openai.com/v1/'

    def request(self, path, params=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'OpenAI API Client'
        }
        url = self.endpoint + path

        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f'Error: {err}')
        
        return response.json()

    def completions(self, prompt, model, temperature=0.5, max_tokens=50):
        path = 'completions'
        params = {
            'model': model,
            'prompt': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        return self.request(path, params)


def generate(prompt):
    if prompt:
        prompt = load_prompt()
    api_key = os.getenv('OPENAI_API') 
    openai = OpenAI_API(api_key)
    response = openai.completions(prompt, 'text-davinci-002', temperature=0.7, max_tokens=100)
    print(response)
    return response




