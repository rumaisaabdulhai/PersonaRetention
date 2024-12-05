from convo_prompts import BUYER_STRATEGIES
from convo_prompts import SELLER_STRATEGIES

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

def evaluate_conversation(file_path, seller_strategy, buyer_strategy):
    with open(file_path, 'r') as file:
        conversation = json.load(file)
    
    buyer_score = 0
    seller_score = 0
    results = []
    conversation = list(itertools.chain(*conversation))
    conversation = list(itertools.chain(*conversation))

    for exchange in conversation:
        role = exchange['content'].split()[0]
        content = exchange['content']
        strategy = seller_strategy if role == "Seller:" else buyer_strategy

        
        score, explanation = evaluate_line(strategy, content)
        results.append({
            "role": role,
            "content": content,
            "strategy": strategy,
            "score": score,
            "explanation": explanation
        })
        
        if role == "Seller":
            seller_score += score
        elif role == "Buyer":
            buyer_score += score
    
    return {
        "results": results,
        "buyer_score": buyer_score,
        "seller_score": seller_score
    }

def process_conversations(directory):
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            parts = filename.replace('.json', '').split('_')
            buyer_idx = int(parts[1])
            seller_idx = int(parts[3])
            
            buyer_strategy = BUYER_STRATEGIES[buyer_idx]
            seller_strategy = SELLER_STRATEGIES[seller_idx]
            
            file_path = os.path.join(directory, filename)
            evaluate_conversation(file_path, seller_strategy, buyer_strategy)
            results[filename] = evaluate_conversation(file_path, seller_strategy, buyer_strategy)
    
    return results

current_directory = os.getcwd() 
conversation_directory = "convos/task_strategy_data"
directory_path = os.path.join(current_directory, conversation_directory)


evaluation_results = process_conversations(directory_path)

with open("evaluation_results.json", "w") as output_file:
    json.dump(evaluation_results, output_file, indent=4)

