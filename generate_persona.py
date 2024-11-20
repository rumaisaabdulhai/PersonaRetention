"""
The purpose of this script is to generate a new persona.
"""
from openai import OpenAI
import os
import pathlib
import json
from classes import Persona
from prompts import generate_persona_prompt, extract_persona_prompt

MODEL = "gpt-4o-mini" # davinci-002
MAX_COMPLETION_TOKENS = 500
PERSONAS_FILE = "personas.json"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_biography():
    """
    Generate a detailed biography for the persona.

    Returns:
        str: The generated biography as a natural language paragraph.
    """
    memory = [{"role": "user", "content": generate_persona_prompt}]
    response = client.chat.completions.create(
        model=MODEL,
        messages=memory,
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    answer = response.choices[0].message.content.strip()
    return answer

def load_existing_personas(file_path):
    """
    Load existing personas from the JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: List of existing personas or an empty list if the file doesn't exist or is empty.
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []
            
def save_personas(file_path, personas):
    """
    Save the list of personas to the JSON file.

    Args:
        file_path (str): Path to the JSON file.
        personas (list): List of personas to save.
    """
    with open(file_path, "w") as file:
        json.dump(personas, file, indent=4)

def append_persona_to_file(file_path, new_persona):
    """
    Append a new persona to the JSON file.

    Args:
        file_path (str): Path to the JSON file.
        new_persona (dict): The new persona to append.
    """
    personas = load_existing_personas(file_path)
    personas.append(new_persona)
    save_personas(file_path, personas)

def extract_features(persona):
    """
    Extract one-sentence summaries from a biography.

    Args:
        biography (str): The detailed biography.

    Returns:
        dict: A dictionary of extracted features and their summaries.
    """
    prompt = extract_persona_prompt.replace("<biography>", persona.biography)
    memory = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model = MODEL,
        messages = memory,
        max_tokens = MAX_COMPLETION_TOKENS
    )
    summaries = response.choices[0].message.content.strip()

    for line in summaries.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip().strip('"')

            if hasattr(persona, key):
                setattr(persona, key, value)
    return persona

def main():
    persona = Persona()
    persona.biography = generate_biography()
    updated_persona = extract_features(persona)

    persona_dict = {attr: getattr(updated_persona, attr) for attr in vars(updated_persona)}
    print("\nNew Persona:")
    print(json.dumps(persona_dict, indent=4))

    append_persona_to_file(PERSONAS_FILE, persona_dict)

if __name__ == "__main__":
    main()