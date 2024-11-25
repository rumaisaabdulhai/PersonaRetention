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

TASK_STRAT_DIR = "task_strategy_data"
TASK_STRAT_STATS_DIR = "task_strategy_stats"

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

    # ask for satisfaction
    response = client.chat.completions.create(
        model=MODEL,
        messages=llm1_memory + [{"role": "system", "content": SATISFACTION_PROMPT}],
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    satisfaction_llm1 = response.choices[0].message.content

    response = client.chat.completions.create(
        model=MODEL,
        messages=llm2_memory + [{"role": "system", "content": SATISFACTION_PROMPT}],
        max_completion_tokens=MAX_COMPLETION_TOKENS
    )
    satisfaction_llm2 = response.choices[0].message.content

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

    return agreement_reached, int(buying_price), int(sell_price), more_to_discuss, convo_complete, int(satisfaction_llm1), int(satisfaction_llm2), convo_length


def eval_task_buyer_seller():
    # make stats dir
    output_dir =  pathlib.Path(f"{pathlib.Path(__file__).parent}/{STATS_DIR}")
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = f"{pathlib.Path(__file__).parent.parent}/convos/{TASK_DIR}/buyer_seller_conversations.json"
    with open(data_dir, "r") as f:
        buyer_seller_conversations = json.load(f)
    evals = []

    for conversation in buyer_seller_conversations:
        buyer_memory, seller_memory = conversation
        agreement_reached, buying_price, sell_price, more_to_discuss, convo_complete, satisfaction_buyer, satisfaction_seller, convo_length = eval_seller_buyer_task(buyer_memory, seller_memory)
        evals.append({
            "agreement_reached": agreement_reached,
            "buying_price": buying_price,
            "sell_price": sell_price,
            "more_to_discuss": more_to_discuss,
            "convo_complete": convo_complete,
            "satisfaction_buyer": satisfaction_buyer,
            "satisfaction_seller": satisfaction_seller,
            "convo_length": convo_length
        })

    with open(f"{output_dir}/{SELLER_BUYER_STATS_FILE}", "w") as f:
        json.dump(evals, f, indent=4)


def eval_task_strategy_buyer_seller():
    # make stats dir for strategy
    output_dir =  pathlib.Path(f"{pathlib.Path(__file__).parent}/{TASK_STRAT_STATS_DIR}")
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = pathlib.Path(f"{pathlib.Path(__file__).parent.parent}/convos/{TASK_STRAT_DIR}")

    for file in data_dir.iterdir():
        with open(file, "r") as f:
            conversations = json.load(f)
        evals = []

        for conversation in conversations:
            seller_memory, buyer_memory = conversation
            agreement_reached, buying_price, sell_price, more_to_discuss, convo_complete, satisfaction_buyer, satisfaction_seller, convo_length = eval_seller_buyer_task(buyer_memory, seller_memory)
            evals.append({
                "agreement_reached": agreement_reached,
                "buying_price": buying_price,
                "sell_price": sell_price,
                "more_to_discuss": more_to_discuss,
                "convo_complete": convo_complete,
                "satisfaction_buyer": satisfaction_buyer,
                "satisfaction_seller": satisfaction_seller,
                "convo_length": convo_length
            })

        with open(f"{output_dir}/{file.name}", "w") as f:
            json.dump(evals, f, indent=4)


def aggregate_stats(data_list):

    num_agreement_reached = 0 # number of agreements reached
    num_agree_complete_no_more_to_discuss = 0 # agreement reached, conversation ended, and no more to discuss
    num_agree_complete_more_to_discuss = 0 # agreement reached, conversation ended, and more to discuss
    num_agree_incomplete_no_more_to_discuss = 0 # agreement reached, conversation not ended, and no more to discuss
    num_agree_incomplete_more_to_discuss = 0 # agreement reached, conversation not ended, and more to discuss

    num_disagree_complete_no_more_to_discuss = 0 # disagreement reached, conversation ended, and no more to discuss
    num_disagree_complete_more_to_discuss = 0 # disagreement reached, conversation ended, and more to discuss
    num_disagree_incomplete_no_more_to_discuss = 0 # disagreement reached, conversation not ended, and no more to discuss
    num_disagree_incomplete_more_to_discuss = 0 # disagreement reached, conversation not ended, and more to discuss

    average_satisfaction_buyer_agreement = 0 # average satisfaction of buyer
    average_satisfaction_seller_agreement = 0 # average satisfaction of seller

    average_satisfaction_buyer_no_agreement = 0 # average satisfaction of buyer
    average_satisfaction_seller_no_agreement = 0 # average satisfaction of seller
    
    average_length = 0 # average length of conversation

    for data in data_list:
        agreement_reached = data['agreement_reached']
        # buying_price = data['buying_price']
        # sell_price = data['sell_price']
        more_to_discuss = data['more_to_discuss']
        convo_complete = data['convo_complete']
        satisfaction_buyer = data['satisfaction_buyer']
        satisfaction_seller = data['satisfaction_seller']
        convo_length = data['convo_length']

        if agreement_reached == 1:
            num_agreement_reached += 1
            if convo_complete == 1:
                if more_to_discuss == 0:
                    num_agree_complete_no_more_to_discuss += 1
                else:
                    num_agree_complete_more_to_discuss += 1
            else:
                if more_to_discuss == 0:
                    num_agree_incomplete_no_more_to_discuss += 1
                else:
                    num_agree_incomplete_more_to_discuss += 1

            average_satisfaction_buyer_agreement += satisfaction_buyer
            average_satisfaction_seller_agreement += satisfaction_seller
        else:
            if convo_complete == 1:
                if more_to_discuss == 0:
                    num_disagree_complete_no_more_to_discuss += 1
                else:
                    num_disagree_complete_more_to_discuss += 1
            else:
                if more_to_discuss == 0:
                    num_disagree_incomplete_no_more_to_discuss += 1
                else:
                    num_disagree_incomplete_more_to_discuss += 1
    
            average_satisfaction_buyer_no_agreement += satisfaction_buyer
            average_satisfaction_seller_no_agreement += satisfaction_seller

        average_length += convo_length

    num_conversations = len(data_list)
    average_length /= num_conversations
    num_disagreement = num_conversations - num_agreement_reached

    if num_disagreement != 0:
        average_satisfaction_buyer_no_agreement /= num_disagreement
        average_satisfaction_seller_no_agreement /= num_disagreement
    else:
        average_satisfaction_buyer_no_agreement = -1
        average_satisfaction_seller_no_agreement = -1

    if num_agreement_reached != 0:
        average_satisfaction_buyer_agreement /= num_agreement_reached
        average_satisfaction_seller_agreement /= num_agreement_reached
    else:
        average_satisfaction_buyer_agreement = -1
        average_satisfaction_seller_agreement = -1


    return {
        "num_conversations": num_conversations,
        "num_agreement_reached": num_agreement_reached,
        "num_agree_complete_no_more_to_discuss": num_agree_complete_no_more_to_discuss,
        "num_agree_complete_more_to_discuss": num_agree_complete_more_to_discuss,
        "num_agree_incomplete_no_more_to_discuss": num_agree_incomplete_no_more_to_discuss,
        "num_agree_incomplete_more_to_discuss": num_agree_incomplete_more_to_discuss,
        "num_disagreement": num_disagreement,
        "num_disagree_complete_no_more_to_discuss": num_disagree_complete_no_more_to_discuss,
        "num_disagree_complete_more_to_discuss": num_disagree_complete_more_to_discuss,
        "num_disagree_incomplete_no_more_to_discuss": num_disagree_incomplete_no_more_to_discuss,
        "num_disagree_incomplete_more_to_discuss": num_disagree_incomplete_more_to_discuss,
        "average_length": average_length,
        "average_satisfaction_buyer_agreement": average_satisfaction_buyer_agreement,
        "average_satisfaction_seller_agreement": average_satisfaction_seller_agreement,
        "average_satisfaction_buyer_no_agreement": average_satisfaction_buyer_no_agreement,
        "average_satisfaction_seller_no_agreement": average_satisfaction_seller_no_agreement
    }


def run_aggregate_stats():
    stats_file = pathlib.Path(f"{pathlib.Path(__file__).parent}/{STATS_DIR}/{SELLER_BUYER_STATS_FILE}")
    with open(stats_file, "r") as f:
        data = json.load(f)

    
    output_dir = pathlib.Path(f"{pathlib.Path(__file__).parent}/agg_{STATS_DIR}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    stats = aggregate_stats(data)
    with open(f"{output_dir}/agg_{SELLER_BUYER_STATS_FILE}", "w") as f:
        json.dump(stats, f, indent=4)

    stats_dir = pathlib.Path(f"{pathlib.Path(__file__).parent}/{TASK_STRAT_STATS_DIR}")

    output_dir = pathlib.Path(f"{pathlib.Path(__file__).parent}/agg_{TASK_STRAT_STATS_DIR}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in stats_dir.iterdir():
        if file.suffix != '.json':
            continue
        with open(file, "r") as f:
            data = json.load(f)
        stats = aggregate_stats(data)
        with open(f"{output_dir}/agg_{file.name}", "w") as f:
            json.dump(stats, f, indent=4)

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

    # eval_task_buyer_seller()

    # eval_task_strategy_buyer_seller()

    run_aggregate_stats()


if __name__ == "__main__":
    main()