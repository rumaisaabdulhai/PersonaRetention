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

USE_PERSONAS = True
NUM_PERSONAS = 10
TASK_DIR = "task_data"
TASK_STRATEGY_DIR = "task_strategy_persona_data" if USE_PERSONAS else "task_strategy_data"

MODE = 0
MODELS = [
    "gpt-4o-mini", # MODE 0
    "davinci-002",  # MODE 1      
    "gpt-4o", # MODE 2
    "o1-mini", # MODE 3
    "gpt-3.5-turbo-0125" # MODE 4
    ]

SELLER_STRATEGY = 1 # 0:None, 1:Anchoring, 2:Reciprocity, 3:Bundling
BUYER_SELLER_ACTIVE = True
CHITCHAT_ACTIVE = False
THERAPIST_PATIENT_ACTIVE = False


MODEL = MODELS[MODE]
LOGGING = False
SELLER_BUYER_FILE = f"buyer_seller_conversations-{MODEL}{SELLER_STRATEGIES[SELLER_STRATEGY][0]}.json"
CHITCHAT_FILE = f"chitchat_conversations-{MODEL}.json"
THERAPIST_PATIENT_FILE = f"therapist_patient_conversations-{MODEL}.json"
MAX_COMPLETION_TOKENS = 500
NUM_ROUNDS = 1 # Number of rounds for each task
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
    if mode == 0 or mode == 2 or mode == 3 or mode == 4:
        # For gpt-4o-mini (chat-based)
        llm1_memory = [{"role": "user", "content": system_prompt_1}]
        llm2_memory = [{"role": "user", "content": system_prompt_2}]
    if mode == 1:
        # For text-davinci-003 (completion-based)
        conversation = []
        history = f"Scenario:\n{system_prompt_1}\nConversation:\n"
        

    choice = random.choice([0, 1])  # Randomly decide who starts the conversation

    for _ in range(NUM_EXCHANGES):

        if choice == 1:
            # LLM1 (Seller or First Participant) goes first
            if mode == 0 or mode == 2 or mode == 3 or mode == 4:
                gpt_turn(llm1_memory, llm2_memory)
            if mode == 1:
                history = davinci_turn(conversation, history, "LLM1")

            # LLM2 (Buyer or Second Participant) responds
            if mode == 0 or mode == 2 or mode == 3 or mode == 4:
                gpt_turn(llm2_memory, llm1_memory)
            if mode == 1:
                history = davinci_turn(conversation, history, "LLM2")
        else:
            # LLM2 (Buyer or Second Participant) goes first
            if mode == 0 or mode == 2 or mode == 3 or mode == 4:
                gpt_turn(llm2_memory, llm1_memory)
            if mode == 1:
                history = davinci_turn(conversation, history, "LLM2")

            # LLM1 (Seller or First Participant) responds
            if mode == 0 or mode == 2 or mode == 3 or mode == 4:
                gpt_turn(llm1_memory, llm2_memory)
            if mode == 1:
                history = davinci_turn(conversation, history, "LLM1")
        if END_CONDITION.upper() in llm1_memory[-1]['content'].upper():
            break


    if mode == 0 or mode == 2 or mode == 3 or mode == 4:
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
    llm1_memory.append({"role": "user", "content": answer})
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
    return history

def run_buyer_seller_strategy_convos():
    """
    Run the conversations for the three tasks: seller-buyer, chitchat, and therapist-patient.
    """
    data_dir = f"{pathlib.Path(__file__).parent}/{TASK_STRATEGY_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    logging.info("Running seller buyer conversations...")

    # seller-buyer
    with open("buyer_strategies.json") as f:
        buyer_strategies = json.load(f)

    # fix buyer stategy, iterate over seller strategies, run each scenario for NUM_ROUNDS
    for i, buyer_strategy in tqdm(enumerate(buyer_strategies)):
        buyer_prompt = BUYER_STRAT_PROMPT.replace("<BUYER_STRATEGY>", buyer_strategy)
        for j, seller_strategy in enumerate(SELLER_STRATEGIES):
            seller_prompt = SELLER_STRAT_PROMPT.replace("<SELLER_STRATEGY>", seller_strategy)
            seller_buyer_conversations = [simulate_conversation(seller_prompt, buyer_prompt, MODE) for _ in range(NUM_ROUNDS)]
            with open(f"{data_dir}/buyer_{i}_seller_{j}.json", "w") as f:
                json.dump(seller_buyer_conversations, f, indent=4)

def run_therapist_patient_strategy_convos(usePersonas = False):
    """
    Run the conversations for the three tasks: seller-buyer, chitchat, and therapist-patient.
    """
    data_dir = f"{pathlib.Path(__file__).parent}/{TASK_STRATEGY_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    logging.info("Running therapist patient conversations...")

    if usePersonas:
        personas_path = pathlib.Path(__file__).parent.parent / "personas/data/therapist_personas.json"
        with open(personas_path, 'r') as f:
            therapist_personas = json.load(f)

    # fix buyer stategy, iterate over seller strategies, run each scenario for NUM_ROUNDS
    for i, patient_strategy in enumerate(PATIENT_STRATEGIES):
        patient_prompt = THERAPIST_STRAT_PROMPT.replace("<PATIENT_STRATEGY>", patient_strategy)
        for j, therapist_strategy in enumerate(THERAPIST_STRATEGIES):
            if usePersonas:
                for k, persona in enumerate(therapist_personas):
                    if k == NUM_PERSONAS:
                        break
                    therapist_prompt = PATIENT_STRAT_PROMPT.replace("<THERAPIST_STRATEGY>", therapist_strategy) + f"""You have the following biography: "{persona['biography']}" """
                    therapist_patient_conversations = [simulate_conversation(therapist_prompt, patient_prompt, MODE) for _ in range(NUM_ROUNDS)]
                    with open(f"{data_dir}/therapist_{i}_patient_{j}_persona_{k}.json", "w") as f:
                        json.dump(therapist_patient_conversations, f, indent=4)
            else:
                therapist_prompt = PATIENT_STRAT_PROMPT.replace("<THERAPIST_STRATEGY>", therapist_strategy)
                therapist_patient_conversations = [simulate_conversation(therapist_prompt, patient_prompt, MODE) for _ in range(NUM_ROUNDS)]
                with open(f"{data_dir}/therapist_{i}_patient_{j}.json", "w") as f:
                    json.dump(therapist_patient_conversations, f, indent=4)


def run_just_task_convos():
    """
    Run the conversations for the three tasks: seller-buyer, chitchat, and therapist-patient.
    """
    data_dir = f"{pathlib.Path(__file__).parent}/{TASK_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    if BUYER_SELLER_ACTIVE:
        logging.info("Running seller buyer conversations...")
        if (MODE == 0 or MODE == 2 or MODE == 3 or MODE == 4):
            seller_buyer_conversations = [simulate_conversation(GENERIC_SELLER_PROMPT, GENERIC_BUYER_PROMPT, MODE) for _ in tqdm(range(NUM_ROUNDS))]
        if (MODE == 1):
            seller_buyer_conversations = [simulate_conversation(GENERATE_SCENARIO_PROMPT("Seller", "seller", "sell a car", "Buyer", "buyer", "buy a car"), "", MODE) for _ in tqdm(range(NUM_ROUNDS))]
        with open(f"{data_dir}/{SELLER_BUYER_FILE}", "w") as f:
            json.dump(seller_buyer_conversations, f, indent=4)

    if CHITCHAT_ACTIVE:
        logging.info("Running chitchat conversations...")
        if (MODE == 0 or MODE == 2 or MODE == 3 or MODE == 4):
            chitchat_conversations = [simulate_conversation(GENERIC_CHITCHAT_PROMPT1, GENERIC_CHITCHAT_PROMPT2, MODE) for _ in tqdm(range(NUM_ROUNDS))]
        if (MODE == 1):
            chitchat_conversations = [simulate_conversation(GENERATE_SCENARIO_PROMPT("Person 1", "person", "have a conversation", "Person 2", "person", "have a conversation"), "", MODE) for _ in tqdm(range(NUM_ROUNDS))]
        with open(f"{data_dir}/{CHITCHAT_FILE}", "w") as f:
            json.dump(chitchat_conversations, f, indent=4)

    if THERAPIST_PATIENT_ACTIVE:
        logging.info("Running therapist patient conversations...")
        if (MODE == 0 or MODE == 2 or MODE == 3 or MODE == 4):
            therapist_patient_conversations = [simulate_conversation(GENERIC_THERAPIST_PROMPT, GENERIC_PATIENT_PROMPT, MODE) for _ in tqdm(range(NUM_ROUNDS))]
        if (MODE == 1):
            therapist_patient_conversations = [simulate_conversation(GENERATE_SCENARIO_PROMPT("Patient", "patient", "discuss their mental health issues with a therapist", "Therapist", "therapist", "help the patient with their mental health issues"), "", MODE) for _ in tqdm(range(NUM_ROUNDS))]    
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
    # run_just_task_convos()

    # task strategy
    #run_buyer_seller_strategy_convos()
    #run_therapist_patient_strategy_convos()

    if USE_PERSONAS:
        run_therapist_patient_strategy_convos(usePersonas = True)


if __name__ == "__main__":
    main()