"""
The purpose of this script is to generate background questions for the persona retention task given a persona.
"""
from openai import OpenAI
import os
import pathlib
import json

MODEL = "gpt-4o-mini"
NUM_QUESTIONS = 10
NUM_MULTIPLE_CHOICE = 4
MAX_COMPLETION_TOKENS = 500
BACKSTORIES_FILE = "background_stories.json"
SAVE_FILE = "qa_pairs.json"

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

prompt = f"Please carefully read the backstory of this person. \
    Create {NUM_QUESTIONS} straight-forward questions and answers about this person where \
    the answers are directly found in the backstory. \
    The questions should be multiple choice with {NUM_MULTIPLE_CHOICE} options. \
    The questions should be in second person and the answers should be in first person. \
    Return just the questions and answers. Each question should be fully contained in one line including the multiple choice options. \
    Each question and answer pair should be separated by a new line. Each answer should be a new line after the question. An example looks like: \
    What is your name? A) John B) Mike C) Jessica D) Stacy\n\
    A) John \n \
    How many kids do you have? A) 1 B) 2 C) 3 D) 4\n \
    C) 3"

def generate_questions_and_answers(background_story):
    """
    Generate background questions and answers for the persona retention task.

    Args:
        background_story (str): The background story to generate questions for.
        num_multiple_choice (int): The number of multiple choice answers to generate for each question.
        num_questions (int): The number of questions to generate.

    Returns:
        questions (list): A list of questions and answers.
    """
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
    background_stories = []
    with open(f"{pathlib.Path(__file__).parent}/data/{BACKSTORIES_FILE}", "r") as f:
        background_stories = json.load(f)

    # Generate questions and answers for each background story
    new_data = []
    for story in background_stories:
        qa_pairs = generate_questions_and_answers(story["story"])
        new_data.append({
            "story": story["story"],
            "qa": qa_pairs
        })

    with open(f"{pathlib.Path(__file__).parent}/data/{SAVE_FILE}", "w") as f:
        json.dump(new_data, f, indent=4)

if __name__ == "__main__":
    main()