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
SATISFACTION_PROMPT = "How satisfied are you with the conversation? Please rate the conversation from 1 to 5, with 1 being the lowest and 5 being the highest. Return just the number."

# prompts for chitchat evaluation
# CHITCHAT_PROMPT = "Did you and the other person have a good conversation? Please say 1 for Yes or 0 for No."

# prompts for therapist patient evaluation
# PATIENT_IMPROVEMENT_PROMPT = "Did the patient show improvement in their mental health? Please say 1 for Yes or 0 for No."
# PATIENT_DIAGNOSIS_PROMPT = "What is the diagnosis of the patient? Return the diagnosis as a string."
# PATIENT_TREATMENT_PROMPT = "What is the treatment plan for the patient? Return the treatment plan as a string."
# PATIENT_NEXT_STEPS_PROMPT = "What are the next steps for the patient? Return the next steps as a string."
# PATIENT_COMPLETE_PROMPT = "Based on this conversation so far, is the conversation complete? Complete means you have said goodbye. Please say 1 for Yes or 0 for No. Return just the number."
# MORE_TO_DISCUSS_PROMPT = "Is there still more to discuss? Please say 1 for Yes or 0 for No. Return just the number."