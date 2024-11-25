"""
This file contains the prompts for the different types of conversations.
"""

# prompts for just task convos
GENERIC_SELLER_PROMPT = "You are a seller, talking to a buyer and trying to help them buy a car. You must help them reach a conclusion to purchase or not purchase a car.\nYou must begin the conversation with Seller:"
GENERIC_BUYER_PROMPT = "You are a buyer, talking to a seller and looking to purchase a new car. You must reach a decision to purchase or not purchase a car.\nYou must begin the conversation with Buyer:"

GENERIC_CHITCHAT_PROMPT1 = "You are a person who is having a conversation with another person. You must engage in a conversation with the other person.\nYou must begin the conversation with Person 1:"
GENERIC_CHITCHAT_PROMPT2 = "You are a person who is having a conversation with another person. You must engage in a conversation with the other person.\nYou must begin the conversation with Person 2:"

GENERIC_THERAPIST_PROMPT = "You are a therapist, talking to a patient. You must help the patient with their mental health issues.\nYou must begin the conversation with Therapist:"
GENERIC_PATIENT_PROMPT = "You are a patient, talking to a therapist. You must discuss your mental health issues with the therapist.\nYou must begin the conversation with Patient:"

def GENERATE_SCENARIO_PROMPT(LLM1_name, LLM1_role, LLM1_goal, LLM2_name, LLM2_role, LLM2_goal):
    return f"{LLM1_name} is a {LLM1_role}, engaging in a conversation with {LLM2_name}, who is a {LLM2_role}. The goal of {LLM1_name} is to {LLM1_goal}. The goal of {LLM2_name} is to {LLM2_goal}"

SELLER_STRATEGIES = [
    ("", ""),
    ("-Anchoring", ". You will use an anchoring strategy in which you start with an aggressive or high offer to set the tone and create a reference point for the negotiation."),
    ("-Reciprocity", ". You will use a reciprocity strategy in which you offer a small concession or gesture upfront to encourage the other party to reciprocate."),
    ("-Bundling", ". You will attempt to combine multiple items or services into one package to make the offer appear more valuable.")
]