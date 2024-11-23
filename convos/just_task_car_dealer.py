"""
How consistent are prompted models for tasks?
"""
from openai import OpenAI
import os
import pathlib
import json
from convo_prompts import generic_seller_prompt, generic_buyer_prompt

MAX_COMPLETION_TOKENS = 500
NUM_ROUNDS = 10 # Number of rounds for each task
NUM_EXCHANGES = 20 # Number of back and forth exchanges between LLMs
MODELS = ["gpt-4o-mini", "davinci-002", "llama3", "llama3", "gemma"]
name1 = "Seller"
name2 = "Buyer"

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def simulate_conversation(model):
    """
    Simulate a conversation between two LLMs with the given background text and questions.
    """
    llm1_memory = [
        {"role": "system", "content": generic_seller_prompt}
    ]
    llm2_memory = [
        {"role": "system", "content": generic_buyer_prompt}
    ]

    for turn in range(NUM_EXCHANGES):
        # Seller begins the conversation
        # response = client.chat.completions.create(
        #     model=model,
        #     messages=llm1_memory,
        #     max_completion_tokens=MAX_COMPLETION_TOKENS
        # )
        response = client.completions.create(
            model=model,
            prompt=generic_seller_prompt,
            max_tokens=MAX_COMPLETION_TOKENS
        )

        answer = response.choices[0].text.strip()

        # answer = response.choices[0].message.content
        print(f"\n{name1}: {answer}")

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # Buyer responds to the seller
        response = client.chat.completions.create(
            model=model,
            messages=llm2_memory,
            max_completion_tokens=MAX_COMPLETION_TOKENS
        )

        answer = response.choices[0].message.content
        print(f"\n{name2}: {answer}")

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        # print("--------")

def main():
    """
    Simulate a conversation between two LLMs with the given background text and questions.
    """
    simulate_conversation(model=MODELS[1])

if __name__ == "__main__":
    main()