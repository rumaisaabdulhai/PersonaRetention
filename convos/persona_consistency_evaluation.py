from openai import OpenAI
import json
import os
import itertools

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def evaluate_line(strategy, line_content):
    prompt = (
        f"Determine whether the following line aligns with the described backstory.\n\n"
        f"Backstory: {strategy}\n"
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

def evaluate_conversation(file_path, first_persona, second_persona, category, first_name=None, second_name=None):

    with open(file_path, 'r') as file:
        conversation = json.load(file)
    conversation = list(itertools.chain(*conversation))

    # figure out if conversation is invalid
    first_utterance = conversation[1]['content']
    if category == "therapist":
        if "Therapist:" in first_utterance and "Patient:" in first_utterance:
            return None
    elif category == "buyer":
        if "Buyer:" in first_utterance and "Seller:" in first_utterance:
            return None
    elif category == "chitchat":
        if "Person 1:" in first_utterance and "Person 2:" in first_utterance:
            return None

    max_score_first = 0
    max_score_second = 0

    first_score = 0
    second_score = 0
    results = []

    # 0/1: 0 for therapist, 1 for patient
    # 0/1: 0 for buyer, 1 for seller
    # 0/1: 0 for person 1, 1 for person 2
    started_first = 0

    if category == "therapist":
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{conversation[1]['content']}\nDoes this sound like a therapist or a patient? Please say 0 for therapist and 1 for patient. Only output the number."}]
        )
        answer = response.choices[0].message.content
        started_first = int(answer.strip())
        print(conversation[1]['content'])
        print("started_first: " + str(started_first))

    elif category == "buyer":
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{conversation[1]['content']}\nDoes this sound like a buyer: someone looking to buy a car or a seller: someone who is helping someone purchase a car? Please say 0 for buyer and 1 for seller. Only output the number."}]
        )
        answer = response.choices[0].message.content
        started_first = int(answer.strip())
        print(conversation[1]['content'])
        print("started_first: " + str(started_first))

    elif category == "chitchat":
        fname = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract only the full name from this sentence: {first_name}"}]
        )
        first_name = fname.choices[0].message.content

        sname = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract only the full name from this sentence: {second_name}"}]
        )
        second_name = sname.choices[0].message.content

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Exchange 1: {conversation[1]['content']}\nExchange 2: {conversation[2]['content']}\nAccording to these exchanges, in which exchange does {first_name} (not {second_name}) speak in? Please say 0 for if this person speaks in the 1st exchange and 1 for if they speak in the 2nd exchange. Only output the number."}]
        )
        answer = response.choices[0].message.content
        started_first = int(answer.strip())
        print(conversation[1]['content'])
        print(conversation[2]['content'])
        print(first_name + ", " + second_name)
        print("started_first: " + str(started_first))

    turn = started_first

    for i in range(1, len(conversation)):

        content = conversation[i]['content']

        # determine if the conversation is invalid
        if category == "therapist":
            if "Therapist:" in content and "Patient:" in content:
                return None
        elif category == "buyer":
            if "Buyer:" in content and "Seller:" in content:
                return None
        elif category == "chitchat":
            if "Person 1:" in content and "Person 2:" in content:
                return None

        if turn == 0:
            if category == "therapist":
                role = "Therapist"
                strategy = first_persona
            elif category == "buyer":
                role = "Buyer"
                strategy = first_persona
            elif category == "chitchat":
                role = "Person 1"
                strategy = first_persona

            score, explanation = evaluate_line(strategy, content)
            results.append({
                "role": role,
                "content": content,
                "strategy": strategy,
                "score": score,
                "explanation": explanation
            })

            max_score_first += 1
            first_score += score
            # switch turns
            turn = 1
        
        else:
            if category == "therapist":
                role = "Patient"
                strategy = second_persona
            elif category == "buyer":
                role = "Seller"
                strategy = second_persona
            elif category == "chitchat":
                role = "Person 2"
                strategy = second_persona

            score, explanation = evaluate_line(strategy, content)
            results.append({
                "role": role,
                "content": content,
                "strategy": strategy,
                "score": score,
                "explanation": explanation
            })

            max_score_second += 1
            second_score += score
            # switch turns
            turn = 0

    print(f"First score: {first_score}")
    print(f"Second score: {second_score}")
    print(f"Max score first: {max_score_first}")
    print(f"Max score second: {max_score_second}")

    return {
        "results": results,
        "first_score": first_score,
        "second_score": second_score,
        "max_score_first": max_score_first,
        "max_score_second": max_score_second
    }

def process_conversations(directory):
    # load the personas first
    # therapist personas
    current_directory = os.getcwd() 
    persona1_path = "personas/data/therapist_personas.json"
    directory1_path = os.path.join(current_directory, persona1_path)
    with open(directory1_path, 'r') as file:
        therapist_personas = json.load(file)

    # generic personas
    persona2_path = "personas/data/generic_personas.json"
    directory2_path = os.path.join(current_directory, persona2_path)
    with open(directory2_path, 'r') as file:
        generic_personas = json.load(file)
    
    # seller personas
    current_directory = os.getcwd() 
    persona3_path = "personas/data/car_dealer_personas.json"
    directory3_path = os.path.join(current_directory, persona3_path)
    with open(directory3_path, 'r') as file:
        seller_personas = json.load(file)

    results = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            parts = filename.replace('.json', '').split('_')
            category = parts[0] 
            first_idx = int(parts[-2])
            second_idx = int(parts[-1])

            # depending on the category, get the respective persona
            if category == "therapist":
                # therapist persona
                continue
                first_persona = therapist_personas[first_idx]["biography"]
                second_persona = therapist_personas[second_idx]["biography"]
                file_path = os.path.join(directory, filename)
                result = evaluate_conversation(file_path, first_persona, second_persona, category)
                if result is not None:
                    results[filename] = result
                else:
                    print(f"Invalid conversation: {filename}")
            
            elif category == "buyer":
                # buyer persona
                continue
                first_persona = generic_personas[first_idx]["biography"]
                second_persona = seller_personas[second_idx]["biography"]
                file_path = os.path.join(directory, filename)
                result = evaluate_conversation(file_path, first_persona, second_persona, category)
                if result is not None:
                    results[filename] = result
                else:
                    print(f"Invalid conversation: {filename}")

            elif category == "chitchat":
                # generic persona
                first_persona = generic_personas[first_idx]["biography"]
                second_persona = generic_personas[10 + second_idx]["biography"]

                first_name = generic_personas[first_idx]["name"]
                second_name = generic_personas[10 + second_idx]["name"]

                file_path = os.path.join(directory, filename)
                file_path = os.path.join(directory, filename)
                result = evaluate_conversation(file_path, first_persona, second_persona, category, first_name, second_name)
                if result is not None:
                    results[filename] = result
                else:
                    print(f"Invalid conversation: {filename}")

    return results

current_directory = os.getcwd() 
conversation_directory = "convos/task_strategy_persona_data"
directory_path = os.path.join(current_directory, conversation_directory)

evaluation_results = process_conversations(directory_path)

# with open("tp_persona_consistency_eval.json", "w") as output_file:
#     json.dump(evaluation_results, output_file, indent=4)

# with open("bs_persona_consistency_eval.json", "w") as output_file:
#     json.dump(evaluation_results, output_file, indent=4)

with open("chitchat_persona_consistency_eval.json", "w") as output_file:
    json.dump(evaluation_results, output_file, indent=4)