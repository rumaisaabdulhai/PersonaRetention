"""
This file contains the prompts used in the evaluation of the conversations.
"""

# prompts for seller buyer evaluation
AGREEMENT_PROMPT_BUYER = "Did you and the seller come to an agreement? This means that you agreed to purchase a car. Please say 1 for Yes or 0 for No."
AGREEMENT_PROMPT_SELLER = "Did you and the buyer come to an agreement? This means that you successfully sold a car. Please say 1 for Yes or 0 for No."
BUYING_PRICE_PROMPT = "What was the buying price of the car? Return just the number without the dollar symbol."
SELLING_PRICE_PROMPT = "What was the selling price of the car? Return just the number without the dollar symbol."
MORE_TO_DISCUSS_PROMPT = "Is there still more to discuss? Has the buyer made a final decision? Please say 1 for Yes or 0 for No. Return just the number."
CONVO_COMPLETE_PROMPT = "Based on this conversation so far, is the conversation complete? Complete means you have said goodbye. Please say 1 for Yes or 0 for No. Return just the number."