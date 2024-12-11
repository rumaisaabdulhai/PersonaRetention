from convo_prompts import BUYER_STRATEGIES
from convo_prompts import SELLER_STRATEGIES
from convo_prompts import CHITCHAT_STRATEGIES_1
from convo_prompts import CHITCHAT_STRATEGIES_2
from convo_prompts import THERAPIST_STRATEGIES
from convo_prompts import PATIENT_STRATEGIES

from openai import OpenAI
import json
import os
import itertools



OPENAI_API_KEY = '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'

client = OpenAI(api_key=OPENAI_API_KEY)
def evaluate_line(strategy, line_content):
    prompt = (
        f"Determine whether the following line aligns with the described strategy.\n\n"
        f"Strategy: {strategy}\n"
        f"Line: {line_content}\n\n"
        f"Respond with '1' if it aligns, '-1' if it does not align, and '0' if it is unclear or neutral. Provide a brief explanation."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    try:
        score = int(answer.strip().split("\n")[0]) 
    except ValueError:
        score = 0 
    explanation = answer.strip()
    return score, explanation

def evaluate_conversation(file_path, first_strategy, second_strategy):
    with open(file_path, 'r') as file:
        conversation = json.load(file)
    
    first_score = 0
    second_score = 0
    results = []
    conversation = list(itertools.chain(*conversation))

    starting = conversation[0]['content']
    if "convince" or "a good impression" in starting:
        role = "Person 2"
    else:
        role = "Person 1"

    for exchange in conversation[1:]:
        if role == "Person 1":
            strategy = first_strategy
        else:
            strategy = second_strategy
        # if len(exchange['content'].split()) > 0:
        #     role = exchange['content'].split()[0]
        # else:
        #     role = ""
        # if "Seller" in role or "SELLER" in role:
        #     role = "Seller"
        # elif "BUYER" in role or "Buyer" in role:
        #     role = "Buyer" 
        # elif "Therapist" in role or "THERAPIST" in role:
        #     role = "Therapist"
        # elif "Patient" in role or "PATIENT" in role:
        #     role = "Patient"
        # else:
        #     role = ""
        content = exchange['content']
        # if role == "Seller" or role == "Patient":
        #     strategy = second_strategy
        # elif role == "Therapist" or role == "Buyer":
        #     strategy = first_strategy
        # else:
        #     strategy = ""

        score, explanation = evaluate_line(strategy, content)
        results.append({
            "role": role,
            "content": content,
            "strategy": strategy,
            "score": score,
            "explanation": explanation
        })
        
        if strategy == first_strategy:
            first_score += score
        elif strategy == second_strategy:
            second_score += score

        if role == "Person 1":
            role = "Person 2"
        else:
            role = "Person 1"
    
    return {
        "results": results,
        "first_score": first_score,
        "second_score": second_score
    }

def process_conversations(directory):
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            parts = filename.replace('.json', '').split('_')
            category = parts[0] 
            first_idx = int(parts[1])
            second_idx = int(parts[2]) if category == 'chitchat' else int(parts[3])
            
            if category == 'chitchat':
                first_strategy = CHITCHAT_STRATEGIES_1[first_idx]
                second_strategy = CHITCHAT_STRATEGIES_2[second_idx]
            elif category == 'therapist':
                first_strategy = THERAPIST_STRATEGIES[first_idx]
                second_strategy = PATIENT_STRATEGIES[second_idx]
            else:
                first_strategy = BUYER_STRATEGIES[first_idx]
                second_strategy = SELLER_STRATEGIES[second_idx]
            
            file_path = os.path.join(directory, filename)
            if category == 'chitchat':
                results[filename] = evaluate_conversation(file_path, first_strategy, second_strategy)
    
    return results

current_directory = os.getcwd() 
conversation_directory = "convos/task_strategy_persona_data"
directory_path = os.path.join(current_directory, conversation_directory)


evaluation_results = process_conversations(directory_path)

with open("chitchat_persona_evaluation_results.json", "w") as output_file:
    json.dump(evaluation_results, output_file, indent=4)

