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

MODE = 1
MODELS = [
    "gpt-4o-mini", # MODE 0
    "davinci-002"  # MODE 1      
          ]

MODEL = MODELS[MODE]
LOGGING = False
SELLER_BUYER_FILE = f"seller_buyer_conversations-{MODEL}.json"
CHITCHAT_FILE = f"chitchat_conversations-{MODEL}.json"
THERAPIST_PATIENT_FILE = f"therapist_patient_conversations-{MODEL}.json"
MAX_COMPLETION_TOKENS = 500
NUM_ROUNDS = 10 # Number of rounds for each task
NUM_EXCHANGES = 15 # Number of back and forth exchanges between LLMs

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def simulate_conversation(system_prompt_1, system_prompt_2, mode):
    """
    Simulate a conversation between two LLMs.

    Args:
        system_prompt_1 (str): The system prompt for the first participant.
        system_prompt_2 (str): The system prompt for the second participant.
        mode (int): 0 for gpt-4o-mini, 1 for text-davinci-003.

    Returns:
        list: The conversation history.
    """
    if mode == 0:
        # For gpt-4o-mini (chat-based)
        llm1_memory = [{"role": "user", "content": system_prompt_1}]
        llm2_memory = [{"role": "user", "content": system_prompt_2}]
    else:
        # For text-davinci-003 (completion-based)
        conversation = []
        history = f"Scenario:\n{system_prompt_1}\n{system_prompt_2}\n\nConversation:\n"

    choice = random.choice([0, 1])  # Randomly decide who starts the conversation

    for _ in range(NUM_EXCHANGES):
        if choice == 1:
            # LLM1 (Seller or First Participant) goes first
            if mode == 0:
                gpt_turn(llm1_memory, llm2_memory)
            if mode == 1:
                davinci_turn(conversation, history, "LLM1")

            # LLM2 (Buyer or Second Participant) responds
            if mode == 0:
                gpt_turn(llm2_memory, llm1_memory)
            if mode == 1:
                davinci_turn(conversation, history, "LLM2")
        else:
            # LLM2 (Buyer or Second Participant) goes first
            if mode == 0:
                gpt_turn(llm2_memory, llm1_memory)
            if mode == 1:
                davinci_turn(conversation, history, "LLM2")

            # LLM1 (Seller or First Participant) responds
            if mode == 0:
                gpt_turn(llm1_memory, llm2_memory)
            if mode == 1:
                davinci_turn(conversation, history, "LLM1")

    if mode == 0:
        return llm1_memory
    if mode == 1:
        return conversation

def gpt_turn(llm1_memory, llm2_memory):
    response = client.chat.completions.create(
        model=MODEL,
        messages=llm1_memory,
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    answer = response.choices[0].message.content.strip()
    llm1_memory.append({"role": "assistant", "content": answer})
    llm2_memory.append({"role": "user", "content": answer})

def davinci_turn(conversation, history, LLM_name):
    response = client.completions.create(
        model=MODEL,
        prompt=f"{history}{LLM_name}: ",
        max_tokens=MAX_COMPLETION_TOKENS,
        stop=["\n"]
    )
    answer = response.choices[0].text.strip()
    conversation.append({"speaker": LLM_name, "message": answer})
    history += f"{LLM_name}: {answer}\n"

def run_just_task_convos():
    """
    Run the conversations for the three tasks: seller-buyer, chitchat, and therapist-patient.
    """
    data_dir = f"{pathlib.Path(__file__).parent}/{TASK_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    logging.info("Running seller buyer conversations...")
    seller_buyer_conversations = [simulate_conversation(GENERIC_SELLER_PROMPT, GENERIC_BUYER_PROMPT, MODE) for _ in tqdm(range(NUM_ROUNDS))]
    with open(f"{data_dir}/{SELLER_BUYER_FILE}", "w") as f:
        json.dump(seller_buyer_conversations, f, indent=4)

    logging.info("Running chitchat conversations...")
    chitchat_conversations = [simulate_conversation(GENERIC_CHITCHAT_PROMPT1, GENERIC_CHITCHAT_PROMPT2, MODE) for _ in tqdm(range(NUM_ROUNDS))]
    with open(f"{data_dir}/{CHITCHAT_FILE}", "w") as f:
        json.dump(chitchat_conversations, f, indent=4)

    logging.info("Running therapist patient conversations...")
    therapist_patient_conversations = [simulate_conversation(GENERIC_THERAPIST_PROMPT, GENERIC_PATIENT_PROMPT, MODE) for _ in tqdm(range(NUM_ROUNDS))]
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