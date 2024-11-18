from openai import OpenAI
import os
import random
import pathlib
import json

# Number of back and forth exchanges between LLMs
NUM_EXCHANGES = 10
MODEL = "gpt-4o-mini"
# MODEL = "davinci-002"
name1 = "Agent 1"
name2 = "Agent 2"
QA_FILE = "qa_pairs.json"

# Number of questions to ask about each persona
NUM_QUESTIONS = 3

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
        {"role": "system", "content": f"You are {name1}. You are a seller, talking to {name2} and trying to help them buy a car. {scenario1}\n This is your story:" + background_text1}
    ]
    llm2_memory = [
        {"role": "system", "content": f"You are {name2}. You are a buyer, talking to {name1} and looking to purchase a new car. {scenario2}\n This is your story:" + background_text2}
    ]

    # random question idxs
    shuffled_idxs = list(range(len(questions1)))
    random.shuffle(shuffled_idxs)
    i = 0
    for turn in range(NUM_EXCHANGES):
        print(f"Turn {i + 1}")

        # Seller begins the conversation
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm1_memory,
            max_completion_tokens=100
        )

        answer = response.choices[0].message.content
        print(f"{answer}")

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # Buyer responds to the seller
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm2_memory,
            max_completion_tokens=100
        )

        answer = response.choices[0].message.content
        print(f"{answer}")

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        i += 1
        print("--------")

        # Ask a set of random questions about each persona
        idxs = random.sample(range(len(questions1)), NUM_QUESTIONS)
        num_right_llm1 = 0
        num_right_llm2 = 0

        for idx in idxs:
            # ask a background question to LLM 1
            question = questions1[idx]
            real_answer = answers1[idx]
            content = f"Please answer the following question about yourself: {question}\nYour answer must belong to one of the given multiple choice options. Example format of answer:\nA) John"
            print(f"{content}\n")
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm1_memory + [{"role": "system", "content": content}],
                max_completion_tokens=100
            )
            answer = response.choices[0].message.content

            # Ask LLM if the response is correct
            # content = f"Given the background story, for the question: \"{question}\" which is asked to {name1}, is the following response correct: {answer} The real answer is {real_answer} Please respond with 1 for yes and 0 for no."
            # print(f"{content}\n")
            # response = client.chat.completions.create(
            #     model=MODEL,
            #     messages=[{"role": "system", "content": background_text1 + "\n" + content}],
            #     max_completion_tokens=100
            # )
            # is_correct = response.choices[0].message.content
            # if is_correct == "1":
            #     print(f"LLM 1 responded correctly! Given answer:\"{answer}\" \nExpected answer:\"{real_answer}\"\n")
            #     num_right_llm1 += 1
            # else:
            #     print(f"LLM 1 incorrect response! Given answer:\"{answer}\" \nExpected answer:\"{real_answer}\"\n")
            if answer.strip(".") == real_answer.strip("."):
                print(f"LLM 1 responded correctly! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")
                num_right_llm1 += 1
            else: 
                print(f"LLM 1 incorrect response! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")

            # ask a background question to LLM 2
            question = questions2[idx]
            real_answer = answers2[idx]
            content = f"Please answer the following question about yourself: {question}\nYour answer must belong to one of the given multiple choice options. Example format of answer:\nA) John"
            print(f"{content}\n")
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm2_memory + [{"role": "system", "content": content}],
                max_completion_tokens=100
            )
            answer = response.choices[0].message.content

            # Ask LLM if the response is correct
            # content = f"Given the background story, for the question: \"{question}\" which is asked to {name2}, is the following response correct: {answer} The real answer is {real_answer} Please respond with 1 for yes and 0 for no."
            # print(f"{content}\n")
            # response = client.chat.completions.create(
            #     model=MODEL,
            #     messages=[{"role": "system", "content": background_text2 + "\n" + content}],
            #     max_completion_tokens=100
            # )
            # is_correct = response.choices[0].message.content
            # if is_correct == "1":
            #     print(f"LLM 2 responded correctly! Given answer:\"{answer}\" \nExpected answer:\"{real_answer}\"\n")
            #     num_right_llm2 += 1
            # else:
            #     print(f"LLM 2 incorrect response! Given answer:\"{answer}\" \nExpected answer:\"{real_answer}\"\n")
            if answer.strip(".") == real_answer.strip("."):
                print(f"LLM 2 responded correctly! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")
                num_right_llm2 += 1
            else:
                print(f"LLM 2 incorrect response! Given answer: \"{answer}\", Expected answer: \"{real_answer}\"\n")

        print("--------")


def main():
    """
    Simulate a conversation between two LLMs with the given background text and questions.
    """
    background_stories = []
    with open(f"{pathlib.Path(__file__).parent}/data/{QA_FILE}", "r") as f:
        background_stories = json.load(f)

    entry = background_stories[0]
    background_text1 = entry["story"]
    questions1 = [qa[0] for qa in entry["qa"]]
    answers1 = [qa[1] for qa in entry["qa"]]

    entry = background_stories[1]
    background_text2 = entry["story"]
    questions2 = [qa[0] for qa in entry["qa"]]
    answers2 = [qa[1] for qa in entry["qa"]]
    simulate_conversation(background_text1, background_text2, questions1, answers1, questions2, answers2)


if __name__ == "__main__":
    main()