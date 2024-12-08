"""
How consistent are prompted models for tasks?
Generate conversations between two LLMs for three different tasks: buyer-seller, chitchat, and therapist-patient.
"""
import copy
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

MODEL = "gpt-4o-mini"

NUM_PERSONAS = 10
TASK_DIR = "task_data"
QA_DIR = "QAs_after_conversations"

LOGGING = False
MAX_COMPLETION_TOKENS = 500

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def run_seller_buyer_qa():

    data_dir = f"{pathlib.Path(__file__).parent}/{QA_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    logging.info("Running buyer seller qa...")

    seller_personas_path = pathlib.Path(__file__).parent.parent / "personas/data/car_dealer_personas.json"
    with open(seller_personas_path, 'r') as f:
        seller_personas = json.load(f)
    buyer_personas_path = pathlib.Path(__file__).parent.parent / "personas/data/generic_personas.json"
    with open(buyer_personas_path, 'r') as f:
        buyer_personas = json.load(f)
    seller_qa_path = pathlib.Path(__file__).parent.parent / "qa/data/qa_pairs_car_dealer.json"
    with open(seller_qa_path, 'r') as f:
        seller_qas = json.load(f)
    buyer_qa_path = pathlib.Path(__file__).parent.parent / "qa/data/qa_pairs_generic.json"
    with open(buyer_qa_path, 'r') as f:
        buyer_qas = json.load(f)    

    with open("buyer_strategies.json") as f:
        buyer_strategies = json.load(f)

    for i, buyer_strategy in tqdm(enumerate(buyer_strategies)):
        for j, seller_strategy in enumerate(SELLER_STRATEGIES):
            offset = 3 * i + j
            for k, buyer_persona in enumerate(buyer_personas):
                if k == NUM_PERSONAS:
                    break
                seller_persona_index = (k+offset) % NUM_PERSONAS
                seller_prompt = f"""You have the following biography: "{seller_personas[seller_persona_index]['biography']}" """ + SELLER_STRAT_PROMPT.replace("<SELLER_STRATEGY>", seller_strategy)
                buyer_prompt = f"""You have the following biography: "{buyer_persona['biography']}" """ + BUYER_STRAT_PROMPT.replace("<BUYER_STRATEGY>", buyer_strategy)
                filename = f"task_strategy_persona_data/buyer_{i}_seller_{j}_persona_{k}_{seller_persona_index}.json"
                convo_path = pathlib.Path(__file__).parent / filename
                with open(convo_path, 'r') as f:
                    convo = json.load(f)
                    buyer_convo = copy.deepcopy(convo)
                    seller_convo = copy.deepcopy(convo)
                    buyer_convo[0][0]["content"] = buyer_prompt
                    seller_convo[0][0]["content"] = seller_prompt

                buyer_qa_set = buyer_qas[k]["qa"]
                seller_qa_set = seller_qas[seller_persona_index]["qa"]
                qa_results = []
                qa_results.append(ask_qas(buyer_convo, buyer_qa_set))
                qa_results.append(ask_qas(seller_convo, seller_qa_set))
                
                with open(f"{data_dir}/buyer_{i}_seller_{j}_persona_{k}_{seller_persona_index}_qa.json", "w") as f:
                    json.dump(qa_results, f, indent=4)



def run_therapist_patient_qa():
    """
    Run the conversations for the three tasks: seller-buyer, chitchat, and therapist-patient.
    """
    data_dir = f"{pathlib.Path(__file__).parent}/{QA_DIR}"
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    logging.info("Running therapist patient qa...")

    therapist_personas_path = pathlib.Path(__file__).parent.parent / "personas/data/therapist_personas.json"
    with open(therapist_personas_path, 'r') as f:
        therapist_personas = json.load(f)
    patient_personas_path = pathlib.Path(__file__).parent.parent / "personas/data/generic_personas.json"
    with open(patient_personas_path, 'r') as f:
        patient_personas = json.load(f)
    therapist_qa_path = pathlib.Path(__file__).parent.parent / "qa/data/qa_pairs_therapist.json"
    with open(therapist_qa_path, 'r') as f:
        therapist_qas = json.load(f)
    patient_qa_path = pathlib.Path(__file__).parent.parent / "qa/data/qa_pairs_generic.json"
    with open(patient_qa_path, 'r') as f:
        patient_qas = json.load(f)    

    for i, patient_strategy in enumerate(PATIENT_STRATEGIES):
        for j, therapist_strategy in enumerate(THERAPIST_STRATEGIES):
            offset = 3 * i + j
            for k, persona in enumerate(therapist_personas):
                if k == NUM_PERSONAS:
                    break
                patient_persona_index = (k+offset) % NUM_PERSONAS
                therapist_prompt = f"""You have the following biography: "{persona['biography']}" """ + PATIENT_STRAT_PROMPT.replace("<THERAPIST_STRATEGY>", therapist_strategy)
                patient_prompt = f"""You have the following biography: "{patient_personas[patient_persona_index]['biography']}" """ + THERAPIST_STRAT_PROMPT.replace("<PATIENT_STRATEGY>", patient_strategy)
                filename = f"task_strategy_persona_data/therapist_{i}_patient_{j}_persona_{k}_{patient_persona_index}.json"
                convo_path = pathlib.Path(__file__).parent / filename
                with open(convo_path, "r") as f:
                    convo = json.load(f)
                    therapist_convo = copy.deepcopy(convo)
                    patient_convo = copy.deepcopy(convo)
                    therapist_convo[0][0]["content"] = therapist_prompt
                    patient_convo[0][0]["content"] = patient_prompt

                therapist_qa_set = therapist_qas[k]["qa"]
                patient_qa_set = patient_qas[patient_persona_index]["qa"]
                qa_results = []
                qa_results.append(ask_qas(therapist_convo, therapist_qa_set))
                qa_results.append(ask_qas(patient_convo, patient_qa_set))

                with open(f"{data_dir}/therapist_{i}_patient_{j}_persona_{k}_{patient_persona_index}_qa.json", "w") as f:
                    json.dump(qa_results, f, indent=4)

def run_chitchat_qa(runtimes = 1):
    """
    Run the conversations for the three tasks: seller-buyer, chitchat, and therapist-patient.
    """

    for i in range(runtimes):
        data_dir = f"{pathlib.Path(__file__).parent}/{QA_DIR}"
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
        logging.info("Running buyer seller conversations...")

        personas_path = pathlib.Path(__file__).parent.parent / "personas/data/generic_personas.json"
        with open(personas_path, 'r') as f:
            personas = json.load(f)    
        persona_qa_path = pathlib.Path(__file__).parent.parent / "qa/data/qa_pairs_generic.json"
        with open(persona_qa_path, 'r') as f:
            persona_qas = json.load(f)    

        group1_personas = personas[0:NUM_PERSONAS]
        group2_personas = personas[NUM_PERSONAS:(2*NUM_PERSONAS)]
        group1_qas = persona_qas[0:NUM_PERSONAS]
        group2_qas = persona_qas[NUM_PERSONAS:(2*NUM_PERSONAS)]

        for i, chitchat_strategy_1 in enumerate(CHITCHAT_STRATEGIES_1):
            for j, chitchat_strategy_2 in enumerate(CHITCHAT_STRATEGIES_2):
                offset = 3 * i + j
                for k, group1_persona in enumerate(group1_personas):
                    if k == NUM_PERSONAS:
                        break
                    group2_persona_index = (k+offset) % NUM_PERSONAS
                    group1_persona_prompt = f"""You have the following biography: "{group1_persona['biography']}" """ + CHITCHAT_STRAT_PROMPT_1.replace("<CHITCHAT_STRATEGY>", chitchat_strategy_1)
                    group2_persona_prompt = f"""You have the following biography: "{group2_personas[group2_persona_index]['biography']}" """ + CHITCHAT_STRAT_PROMPT_2.replace("<CHITCHAT_STRATEGY>", chitchat_strategy_2)
                    filename = f"task_strategy_persona_data/chitchat_{i}_{j}_persona_{k}_{group2_persona_index}.json"
                    convo_path = pathlib.Path(__file__).parent / filename
                    with open(convo_path, 'r') as f:
                        convo = json.load(f)
                        group1_convo = copy.deepcopy(convo)
                        group2_convo = copy.deepcopy(convo)
                        group1_convo[0][0]["content"] = group1_persona_prompt
                        group2_convo[0][0]["content"] = group2_persona_prompt
                    
                    group1_qa_set = group1_qas[k]["qa"]
                    group2_qa_set = group2_qas[group2_persona_index]["qa"]
                    qa_results = []
                    qa_results.append(ask_qas(group1_convo, group1_qa_set))
                    qa_results.append(ask_qas(group2_convo, group2_qa_set))
                    with open(f"{data_dir}/chitchat_{i}_{j}_persona_{k}_{group2_persona_index}_qa.json", "w") as f:
                        json.dump(qa_results, f, indent=4)

def ask_qas(memory, qa_set):
    answered_qas = []
    for id, qa in enumerate(qa_set):
        
        if len(qa) == 2:
            question, correct_answer = qa
        else:
            question, correct_answer, id = qa

        if question == "":
            answered_qas.append({"id": id, "question": "", "answer": "", "given answer": ""})
            continue

        #cleanup
        question = question.replace(".","")
        question = question.replace("true statement about you?", "true statement about you? Choose only one answer and give the answer exactly as it's presented in the question.")
        correct_answer = correct_answer.replace(".","")
        if correct_answer.startswith(" "):
            correct_answer = correct_answer[1:]

        memory_copy = memory[0].copy()
        primed_question = question + " Provide only the answer without further explanation. "
        memory_copy.append({"role": "user", "content": primed_question})

        response = client.chat.completions.create(
            model=MODEL,
            messages=memory_copy,
            max_completion_tokens=MAX_COMPLETION_TOKENS
        )
        answer = response.choices[0].message.content.strip()
        answered_qas.append({"id": id, "question": question, "answer": correct_answer, "given answer": answer})
    return answered_qas
    

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

    #run_seller_buyer_qa()
    #run_therapist_patient_qa()
    run_chitchat_qa(5)


if __name__ == "__main__":
    main()