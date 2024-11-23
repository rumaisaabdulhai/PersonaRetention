from openai import OpenAI
import os
import random
import pathlib
import json

# Number of back and forth exchanges between LLMs
NUM_EXCHANGES = 10
MODEL = "gpt-4o-mini"
name1 = "Seller"
name2 = "Buyer"
SELLER_FILE = "qa_pairs_car_dealer.json"
BUYER_FILE = "qa_pairs_generic.json"

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

scenario1 = """
Background seller: The agent never gives discounts, never talks about the features of the car, and is very concise. 
"""

scenario2 = """Background buyer: The buyer will never buy from the seller unless given a discount.
Preferred brands: Tesla
Preferred features: ["Apple CarPlay/Android Auto", "Bluetooth", "Blind spot monitoring", "Navigation system", "Leather seats", "Sunroof/moonroof", "Remote start", "Heated seats", "Third-row seating", "Backup camera"] 
Budget: 90k"""

def simulate_conversation(background_text1, background_text2, questions1, answers1, questions2, answers2):
    """
    Simulate a conversation between two LLMs with the given background text and questions.
    """
    # Step 1: Feed each persona into the LLM memory
    llm1_memory = [
        {"role": "system", "content": f"You are a seller, talking to a buyer and trying to help them buy a car. {scenario1}\n This is your story:" + background_text1}
    ]
    llm2_memory = [
        {"role": "system", "content": f"You are a buyer, talking to a seller and looking to purchase a new car. {scenario2}\n This is your story:" + background_text2}
    ]

    accuracies_llm1 = []
    accuracies_llm2 = []
    for turn in range(NUM_EXCHANGES):
        # Seller begins the conversation
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm1_memory,
            max_completion_tokens=500
        )

        answer = response.choices[0].message.content
        print(f"\n{name1}: {answer}")

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # Buyer responds to the seller
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm2_memory,
            max_completion_tokens=500
        )

        answer = response.choices[0].message.content
        print(f"\n{name2}: {answer}")

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        # print("--------")
        num_right_llm1 = 0
        num_right_llm2 = 0

        for idx in range(len(questions1)):
            # ask a background question to LLM 1
            question = questions1[idx]
            real_answer = answers1[idx]
            content = f"Please answer the following question about yourself: {question}\nYour answer must belong to one of the given multiple choice options. Example format of answer:\nA) John"
            # print(f"{content}\n")
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm1_memory + [{"role": "system", "content": content}],
                max_completion_tokens=100
            )
            answer = response.choices[0].message.content

            if answer.strip(".") == real_answer.strip("."):
                # print(f"LLM 1 responded correctly! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")
                num_right_llm1 += 1
            # else: 
                # print(f"LLM 1 incorrect response! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")

        for idx in range(len(questions2)):
            # ask a background question to LLM 2
            question = questions2[idx]
            real_answer = answers2[idx]
            content = f"Please answer the following question about yourself: {question}\nYour answer must belong to one of the given multiple choice options. Example format of answer:\nA) John"
            # print(f"{content}\n")
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm2_memory + [{"role": "system", "content": content}],
                max_completion_tokens=100
            )
            answer = response.choices[0].message.content

            if answer.strip(".") == real_answer.strip("."):
                # print(f"LLM 2 responded correctly! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")
                num_right_llm2 += 1
            # else:
                # print(f"LLM 2 incorrect response! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")

        accuracy_llm1 = num_right_llm1 / len(questions1)
        accuracy_llm2 = num_right_llm2 / len(questions2)
        accuracies_llm1.append(accuracy_llm1)
        accuracies_llm2.append(accuracy_llm2)

    # print("--------")
    print("LLM 1 Accuracies: ", accuracies_llm1)
    print("LLM 2 Accuracies: ", accuracies_llm2)
    print(f"LLM 1 average accuracy: {sum(accuracies_llm1) / len(accuracies_llm1)}")
    print(f"LLM 2 average accuracy: {sum(accuracies_llm2) / len(accuracies_llm2)}")
    return accuracies_llm1, accuracies_llm2


def main():
    """
    Simulate a conversation between two LLMs with the given background text and questions.
    """
    seller_personas = []
    with open(f"{pathlib.Path(__file__).parent}/data/{SELLER_FILE}", "r") as f:
        seller_personas = json.load(f)

    buyer_personas = []
    with open(f"{pathlib.Path(__file__).parent}/data/{BUYER_FILE}", "r") as f:
        buyer_personas = json.load(f)
    
    for i, seller in enumerate(seller_personas):
        background_text1 = seller["story"]
        questions1 = [qa[0] for qa in seller["qa"]]
        answers1 = [qa[1] for qa in seller["qa"]]

        for j, buyer in enumerate(buyer_personas):
            background_text2 = buyer["story"]
            questions2 = [qa[0] for qa in buyer["qa"]]
            answers2 = [qa[1] for qa in buyer["qa"]]
            print("--------")
            print(f"Conversation between Seller {i + 1} and Buyer {j + 1}")
            accuracies_llm1, accuracies_llm2 = simulate_conversation(background_text1, background_text2, questions1, answers1, questions2, answers2)
            break


if __name__ == "__main__":
    main()