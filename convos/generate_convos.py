"""
How consistent are prompted models for tasks?
Generate conversations between two LLMs for three different tasks: buyer-seller, chitchat, and therapist-patient.
"""
from openai import OpenAI
import os
import random
import json
import logging
from tqdm import tqdm
import pathlib
from convo_prompts import *

logging.basicConfig(
    level=logging.INFO,  # Default level
    format='%(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()         # Log to the console
    ]
)

TASK_DIR = "task_data"
# TASK_STRATEGY_DIR = "task_strategy_data"
# TASK_STRATEGY_PERSONA_DIR = "task_strategy_persona_data"

LOGGING = False
SELLER_BUYER_FILE = "seller_buyer_conversations.json"
CHITCHAT_FILE = "chitchat_conversations.json"
THERAPIST_PATIENT_FILE = "therapist_patient_conversations.json"
MAX_COMPLETION_TOKENS = 500
NUM_ROUNDS = 10 # Number of rounds for each task
NUM_EXCHANGES = 15 # Number of back and forth exchanges between LLMs
MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def sim_gpt_convo(system_prompt_1, system_prompt_2):
    """
    Simulate a conversation between two LLMs with the given background text and questions.
    """
    llm1_memory = [
        {"role": "user", "content": system_prompt_1}
    ]
    llm2_memory = [
        {"role": "user", "content": system_prompt_2}
    ]

    # 1: seller goes first, else buyer goes first
    choice = random.choice([0, 1])

    for turn in range(NUM_EXCHANGES):
        if choice == 1:
            # seller goes first
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm1_memory,
                max_completion_tokens=MAX_COMPLETION_TOKENS
            )

            answer = response.choices[0].message.content
            logging.info(f"\n{answer}")

            # add the response to LLM 1's memory
            llm1_memory.append({"role": "user", "content": answer})

            # add the response to LLM 2's memory
            llm2_memory.append({"role": "user", "content": answer})

            # buyer responds to the seller
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm2_memory,
                max_completion_tokens=MAX_COMPLETION_TOKENS
            )

            answer = response.choices[0].message.content
            logging.info(f"\n{answer}")

            # add the response to LLM 2's memory
            llm2_memory.append({"role": "user", "content": answer})

            # add the response to LLM 1's memory
            llm1_memory.append({"role": "user", "content": answer})
        else:
            # buyer goes first
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm2_memory,
                max_completion_tokens=MAX_COMPLETION_TOKENS
            )

            answer = response.choices[0].message.content
            logging.info(f"\n{answer}")

            # add the response to LLM 2's memory
            llm2_memory.append({"role": "user", "content": answer})

            # add the response to LLM 1's memory
            llm1_memory.append({"role": "user", "content": answer})

            # seller responds to the buyer
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm1_memory,
                max_completion_tokens=MAX_COMPLETION_TOKENS
            )

            answer = response.choices[0].message.content
            logging.info(f"\n{answer}")

            # add the response to LLM 1's memory
            llm1_memory.append({"role": "user", "content": answer})

            # add the response to LLM 2's memory
            llm2_memory.append({"role": "user", "content": answer})

    return llm1_memory, llm2_memory


def run_just_task_convos():
    data_dir = f"{pathlib.Path(__file__).parent}/{TASK_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    logging.info("Running seller buyer conversations...")
    seller_buyer_conversations = [sim_gpt_convo(GENERIC_SELLER_PROMPT, GENERIC_BUYER_PROMPT) for _ in tqdm(range(NUM_ROUNDS))]
    with open(f"{data_dir}/{SELLER_BUYER_FILE}", "w") as f:
        json.dump(seller_buyer_conversations, f, indent=4)

    logging.info("Running chitchat conversations...")
    chitchat_conversations = [sim_gpt_convo(GENERIC_CHITCHAT_PROMPT1, GENERIC_CHITCHAT_PROMPT2) for _ in tqdm(range(NUM_ROUNDS))]
    with open(f"{data_dir}/{CHITCHAT_FILE}", "w") as f:
        json.dump(chitchat_conversations, f, indent=4)

    logging.info("Running therapist patient conversations...")
    therapist_patient_conversations = [sim_gpt_convo(GENERIC_THERAPIST_PROMPT, GENERIC_PATIENT_PROMPT) for _ in tqdm(range(NUM_ROUNDS))]
    with open(f"{data_dir}/{THERAPIST_PATIENT_FILE}", "w") as f:
        json.dump(therapist_patient_conversations, f, indent=4)

def main():
    """
    Simulate a conversation between two LLMs.
    """
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    if LOGGING:
        logging.disable(logging.NOTSET)
    else:
        logging.disable(logging.CRITICAL)

    # just task
    run_just_task_convos()

if __name__ == "__main__":
    main()