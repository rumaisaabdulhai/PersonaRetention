from openai import OpenAI
import os
import pathlib
import json
import logging
from eval_prompts import *

logging.basicConfig(
    level=logging.INFO,  # Default level
    format='%(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()         # Log to the console
    ]
)

TASK_DIR = "task_data"
STATS_DIR = "task_stats"
SELLER_BUYER_STATS_FILE = "task_seller_buyer_stats.json"
LOGGING = False
MAX_COMPLETION_TOKENS = 50
MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def get_readable_conversation(memory):
    """
    Get the readable conversation from the memory.

    Args:
        memory (list): The memory of the conversation.

    Returns:
        str: The readable conversation.
    """
    conversation = ""
    for i in range(1, len(memory)):
        conversation += f"{memory[i]['content']}\n"
    return conversation

def eval_seller_buyer_task(llm1_memory, llm2_memory):
    """
    Evaluate the task conversation between two LLMs.

    Args:
        llm1_memory (list): The memory of the first LLM.
        llm2_memory (list): The memory of the second LLM.
    """
    # ask for agreement from buyer
    response = client.chat.completions.create(
        model=MODEL,
        messages=llm1_memory + [{"role": "system", "content": AGREEMENT_PROMPT_BUYER}], # memory of the buyer
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    buyer_agreement = response.choices[0].message.content
    if buyer_agreement == "1":
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm1_memory + [{"role": "system", "content": BUYING_PRICE_PROMPT}],
            max_completion_tokens=MAX_COMPLETION_TOKENS
        )
        buying_price = response.choices[0].message.content

    # ask for agreement from seller
    response = client.chat.completions.create(
        model=MODEL,
        messages=llm2_memory + [{"role": "system", "content": AGREEMENT_PROMPT_SELLER}], # memory of the seller
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    seller_agreement = response.choices[0].message.content
    if seller_agreement == "1":
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm2_memory + [{"role": "system", "content": SELLING_PRICE_PROMPT}],
            max_completion_tokens=MAX_COMPLETION_TOKENS
        )
        sell_price = response.choices[0].message.content

    if seller_agreement == "1" and buyer_agreement == "1":
        agreement_reached = 1
    else:
        agreement_reached = 0
        buying_price = -1
        sell_price = -1

    # ask if there is more to discuss
    response = client.chat.completions.create(
        model=MODEL,
        messages=llm1_memory + [{"role": "system", "content": MORE_TO_DISCUSS_PROMPT}],
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    more_to_discuss_llm1 = response.choices[0].message.content

    response = client.chat.completions.create(
        model=MODEL,
        messages=llm2_memory + [{"role": "system", "content": MORE_TO_DISCUSS_PROMPT}],
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    more_to_discuss_llm2 = response.choices[0].message.content

    if more_to_discuss_llm1 == "1" and more_to_discuss_llm2 == "1":
        more_to_discuss = 1
    else:
        more_to_discuss = 0

    # find how long the conversation was
    sub_llm1_memory = [llm1_memory[0]]
    sub_llm2_memory = [llm2_memory[0]]
    convo_complete = 0
    convo_length = 0

    for i in range(1, len(llm1_memory)):
        sub_llm1_memory.append(llm1_memory[i])
        sub_llm2_memory.append(llm2_memory[i])
        convo_length += 1
    
        response = client.chat.completions.create(
            model=MODEL,
            messages=sub_llm1_memory + [{"role": "system", "content": CONVO_COMPLETE_PROMPT}],
            max_completion_tokens=MAX_COMPLETION_TOKENS
        )
        complete_llm1 = response.choices[0].message.content

        response = client.chat.completions.create(
            model=MODEL,
            messages=sub_llm2_memory + [{"role": "system", "content": CONVO_COMPLETE_PROMPT}],
            max_completion_tokens=MAX_COMPLETION_TOKENS
        )
        complete_llm2 = response.choices[0].message.content

        if complete_llm1 == "1" and complete_llm2 == "1":
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=sub_llm1_memory + [{"role": "system", "content": CONVO_COMPLETE_PROMPT}],
                max_completion_tokens=MAX_COMPLETION_TOKENS
            )
            complete_llm1 = response.choices[0].message.content

            response = client.chat.completions.create(
                model=MODEL,
                messages=sub_llm2_memory + [{"role": "system", "content": CONVO_COMPLETE_PROMPT}],
                max_completion_tokens=MAX_COMPLETION_TOKENS
            )
            complete_llm2 = response.choices[0].message.content

            if complete_llm1 == "1" and complete_llm2 == "1":
                convo_complete = 1
                break

    return agreement_reached, int(buying_price), int(sell_price), more_to_discuss, convo_complete, convo_length

def main():
    """
    Evaluate the seller buyer (just task) conversations and save the statistics.
    """
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    if LOGGING:
        logging.disable(logging.NOTSET)
    else:
        logging.disable(logging.CRITICAL)

    # make stats dir
    output_dir =  pathlib.Path(f"{pathlib.Path(__file__).parent}/{STATS_DIR}")
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = f"{pathlib.Path(__file__).parent.parent}/convos/{TASK_DIR}/buyer_seller_conversations.json"
    with open(data_dir, "r") as f:
        buyer_seller_conversations = json.load(f)
    evals = []

    for conversation in buyer_seller_conversations:
        buyer_memory, seller_memory = conversation
        agreement_reached, buying_price, sell_price, more_to_discuss, convo_complete, convo_length = eval_seller_buyer_task(buyer_memory, seller_memory)
        evals.append({
            "agreement_reached": agreement_reached,
            "buying_price": buying_price,
            "sell_price": sell_price,
            "more_to_discuss": more_to_discuss,
            "convo_complete": convo_complete,
            "convo_length": convo_length
        })

    with open(f"{output_dir}/{SELLER_BUYER_STATS_FILE}", "w") as f:
        json.dump(evals, f, indent=4)

if __name__ == "__main__":
    main()