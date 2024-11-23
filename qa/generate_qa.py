"""
The purpose of this script is to generate background questions for the persona retention task given a persona.
"""
from openai import OpenAI
import os
import pathlib
import json
from qa_prompts import generate_qa_together_prompt, generate_qa_separately_prompt

MODEL = "gpt-4o-mini"
NUM_QUESTIONS = 10
NUM_MULTIPLE_CHOICE = 4
MAX_COMPLETION_TOKENS = 500
BACKSTORIES_FILE = "tiny_anthology_personas.json"
SAVE_FILE = "qa_pairs_tiny_anthology.json"

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_qa_separately(persona_dict):
    """
    Generate background questions and answers for the persona retention task.
    """
    qa_pairs = []
    for key, value in persona_dict.items():
        if key == "biography":
            continue

        # check if no information is provided
        if value == "":
            print("skipping b/c empty string")
            continue

        # check if it mentions that there is no information
        memory = [{"role": "user", "content": f"Does the following sentence say something like there is no information provided, \
                   no specific details mentioned, or not specified in the biography? Please say only Yes for 1 or No for 0: {value}"}]
        response = client.chat.completions.create(
            model=MODEL,
            messages=memory,
            max_tokens=MAX_COMPLETION_TOKENS
        )
        answer = response.choices[0].message.content
        if answer == "1":
            print(f"skipping b/c no information: {value}")
            continue

        prompt = generate_qa_separately_prompt.replace("<info>", value).replace("<num_multiple_choice>", str(NUM_MULTIPLE_CHOICE))
        memory = [{"role": "user", "content": f"{prompt}"}]
        response = client.chat.completions.create(
            model=MODEL,
            messages=memory,
            max_tokens=MAX_COMPLETION_TOKENS
        )
        answer = response.choices[0].message.content
        memory.append({"role": "assistant", "content": answer})
        memory.append({"role": "user", "content": "Please make sure the question is in second-person. \
                       The answer must be as brief and short as possible. \
                    If it is not correct, please revise it and send the same response as before but with the corrections. An example looks like: \
                    What is your name? A) John B) Mike C) Jessica D) Stacy\n\
                    A) John"})
        response = client.chat.completions.create(
            model=MODEL,
            messages=memory,
            max_tokens=MAX_COMPLETION_TOKENS
        )
        answer = response.choices[0].message.content
        qa_pairs.append(answer)
    return [(qa.split("\n")[0].strip(), qa.split("\n")[1].strip()) for qa in qa_pairs]


def generate_qa_together(background_story):
    """
    Generate background questions and answers for the persona retention task.

    Args:
        background_story (str): The background story to generate questions for.
        num_multiple_choice (int): The number of multiple choice answers to generate for each question.
        num_questions (int): The number of questions to generate.

    Returns:
        questions (list): A list of questions and answers.
    """
    prompt = generate_qa_together_prompt.replace("<num_question>", str(NUM_QUESTIONS)).replace("<num_multiple_choice>", str(NUM_MULTIPLE_CHOICE))
    memory = [{"role": "user", "content": f"{background_story}\n{prompt}"}]
    response = client.chat.completions.create(
        model=MODEL,
        messages=memory,
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    answer = response.choices[0].message.content
    memory.append({"role": "assistant", "content": answer})
    memory.append({"role": "user", "content": "Please make sure the questions are in second-person and the answers are in first-person. \
                   If any are not correct, please revise them and send the same response as before but with the corrections."})
    response = client.chat.completions.create(
        model=MODEL,
        messages=memory,
        max_tokens=MAX_COMPLETION_TOKENS
    )
    answer = response.choices[0].message.content
    qa_pairs = answer.split("\n\n")
    return [(qa.split("\n")[0].strip(), qa.split("\n")[1].strip()) for qa in qa_pairs]

def main():
    """
    Generates questions and answers for each background story and saves them to a json file.
    """
    # Read in the background stories
    output_with_qa = []
    personas = []
    with open(f"{pathlib.Path(__file__).parent.parent}/personas/data/{BACKSTORIES_FILE}", "r") as f:
        personas = json.load(f)

    i = 0
    for persona in personas:
        qa_pairs = generate_qa_separately(persona)
        output_with_qa.append({
            "story": persona["biography"],
            "qa": qa_pairs
        })
        i += 1
        print(f"{i}/{len(personas)}")

    with open(f"{pathlib.Path(__file__).parent}/data/{SAVE_FILE}", "w") as f:
        json.dump(output_with_qa, f, indent=4)

def main2():
    """
    Generates questions and answers for each background story and saves them to a json file.
    """
    # Read in the background stories
    background_stories = []
    with open(f"{pathlib.Path(__file__).parent.parent}/personas/data/{BACKSTORIES_FILE}", "r") as f:
        background_stories = json.load(f)

    # Generate questions and answers for each background story
    new_data = []
    i = 0
    for story in background_stories:
        qa_pairs = generate_qa_together(story)
        new_data.append({
            "story": story,
            "qa": qa_pairs
        })
        i += 1
        print(f"{i}/{len(background_stories)}")

    with open(f"{pathlib.Path(__file__).parent}/data/{SAVE_FILE}", "w") as f:
        json.dump(new_data, f, indent=4)

if __name__ == "__main__":
    main2()