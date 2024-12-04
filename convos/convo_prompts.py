"""
This file contains the prompts for the different types of conversations.
"""

END_CONDITION = "END CONVERSATION"
END_CONDITION_PROMPT = f"""If the conversation has concluded, say {END_CONDITION}. """

# buyer seller
GENERIC_SELLER_PROMPT = "You are a seller, talking to a buyer and trying to help them buy a car. You must help them reach a conclusion to purchase or not purchase a car."
GENERIC_BUYER_PROMPT = "You are a buyer, talking to a seller and looking to purchase a new car. You must reach a decision to purchase or not purchase a car."
SELLER_STRAT_PROMPT = f"""{GENERIC_SELLER_PROMPT}\n<SELLER_STRATEGY>\n{END_CONDITION_PROMPT}\nSeller: """
BUYER_STRAT_PROMPT = f"""{GENERIC_BUYER_PROMPT}\n<BUYER_STRATEGY>\n{END_CONDITION_PROMPT}\nBuyer: """
SELLER_STRAT_PERSONA_PROMPT = f"""{GENERIC_SELLER_PROMPT}\n<SELLER_STRATEGY>\nThis is your story: <SELLER_BACKGROUND>"""
BUYER_STRAT_PERSONA_PROMPT = f"""{GENERIC_BUYER_PROMPT}\n<BUYER_STRATEGY>\nThis is your story: <BUYER_BACKGROUND>"""

SELLER_STRATEGIES = ["You never give discounts and love to talk a lot about features of the car.",
                     "You never give discounts, never talk about the features of the car, and are very concise.",
                     "You never talk about the features of the car and love to give discounts."]
BUYER_STRATEGIES = ["You will only buy the car if it meets all of your specifications.", # 0
                    "You are extremely impatient and strongly dislike unnecessary information about discounts and features.", # 1
                    "You will never buy from the seller unless given a discount."] # 2
BUDGET = ["30k", "90k", "70k", "10k", "50k"]
PREFERRED_BRAND = ["Porsche", "Volkswagen", "Audi", "Lexus", "BMW", "Honda", "Mercedes-Benz", "Subaru", "Mazda", "Toyota", "Tesla", "Hyundai", "Ford"]
PREFERRED_FEATURES = ["Leather seats", "Heated seats", "Remote start", "Bluetooth", "Apple CarPlay/Android Auto", "Blind spot monitoring", "Backup camera", "Sunroof/moonroof", "Third-row seating", "Navigation system"]

def GENERATE_SCENARIO_PROMPT(LLM1_name, LLM1_role, LLM1_goal, LLM2_name, LLM2_role, LLM2_goal):
    return f"{LLM1_name} is a {LLM1_role}, engaging in a conversation with {LLM2_name}, who is a {LLM2_role}. The goal of {LLM1_name} is to {LLM1_goal}. The goal of {LLM2_name} is to {LLM2_goal}"


GENERIC_THERAPIST_PROMPT = "You are a therapist, talking to a patient. You must help the patient with their mental health issues.\nYou must begin the conversation with Therapist:"
GENERIC_PATIENT_PROMPT = "You are a patient, talking to a therapist. You must discuss your mental health issues with the therapist.\nYou must begin the conversation with Patient:"

THERAPIST_STRAT_PROMPT = f"""{GENERIC_THERAPIST_PROMPT}\n<THERAPIST_STRATEGY>\n{END_CONDITION_PROMPT}\nTherapist: """
PATIENT_STRAT_PROMPT = f"""{GENERIC_PATIENT_PROMPT}\n<PATIENT_STRATEGY>\n{END_CONDITION_PROMPT}\nPatient: """

THERAPIST_STRATEGIES = ["Your strategy is to have patients talk about their upbringing",
                        "Your strategy is to build trust by drawing parallels to your own life and experiences",
                        "Your strategy is to ask questions guiding towards a diagnosis"]

PATIENT_STRATEGIES = ["You are open to therapy and want to be forthcoming with your answers.",
                      "You are avoidant and want to answer the questions while not disclosing more than you have to.",
                      "You want to discuss a recent event that caused you a lot of distress."]


# GENERIC_DOCTOR_PROMPT = "You are a doctor, talking to a patient. You must help the patient with their physical health issues.\nYou must begin the conversation with Doctor:"
# GENERIC_PATIENT_PROMPT = "You are a patient, talking to a doctor. You must discuss your physical health issues with the doctor.\nYou must begin the conversation with Patient:"

GENERIC_CHITCHAT_PROMPT_1 = "You are a person who is having a conversation with another person. You must engage in a conversation with the other person.\nYou must begin the conversation with Person 1:"
GENERIC_CHITCHAT_PROMPT_2 = "You are a person who is having a conversation with another person. You must engage in a conversation with the other person.\nYou must begin the conversation with Person 2:"

CHITCHAT_STRAT_PROMPT_1 = f"""{GENERIC_CHITCHAT_PROMPT_1}\n<CHITCHAT_STRATEGY>\n{END_CONDITION_PROMPT}\nPerson 1: """
CHITCHAT_STRAT_PROMPT_2 = f"""{GENERIC_CHITCHAT_PROMPT_2}\n<CHITCHAT_STRATEGY>\n{END_CONDITION_PROMPT}\nPerson 2: """

CHITCHAT_STRATEGIES_1 = ["You are trying to get to know the other person. You are very curious and ask a lot of questions. You are very friendly and outgoing. ",
                       "You are interested in talking about yourself. You are not very interested in asking the other person about themselves. ",
                       "You are doing a mix of talkint about yourself and asking about the other person. "
                        ]

CHITCHAT_STRATEGIES_2 = ["You’re meeting someone with whom it's very important for you to leave a good impression. ",
                        "You want to convince this person that you are interesting without it being apparent that you are trying to do so.",
                        "You want to convince the other person of something—whether it’s a new idea, a recommendation, or even to try an activity with you."
                         ]

# THERAPIST_STRATEGIES = [
#     "You are a marriage and family counseling therapist. You are focused on addressing the behaviors of people in a marriage or the individual behaviors of family members. You also examine the relationships between members of a family.",
#     "You are an addiction therapist who has specialized training to help your clients overcome substance abuse problems. You may help your clients process issues from their past that may have led to their addiction."
#     "You are a behaviorial therapist who works with clients who are experiencing challenges because of a mental disorder.",
#     "You are a divorce therapist who specializes in helping couples who are struggling in their marriage and feel that they are approaching divorce.",
#     "You are a child therapist who treat children ages 17 and younger for emotional, behavioral and mental disorders.",
#     "You are a clinical therapists that focuses on treating the underlying issues that are causing their clients to experience problems in other areas of their lives."
#     "You are a cognitive therapist who offers short-term therapy to help their clients find new ways to behave by changing their thought patterns. You help your patients identify the thought patterns that are causing problems and then create healthier thought patterns to improve their quality of life.",
#     "You are a cognitive-behavioral therapist (CBT) who uses behavioral and psychotherapeutic techniques to help their clients address a variety of different psychological problems, including substance abuse, depression and eating disorders.",
#     "You are an eating disorder therapist who specializes in helping patients with eating disorders.",
#     "You are an exercise therapist who helps their clients regain normal functionality after experiencing an injury or recovering from an illness or disease. You develop an exercise routine to help your clients manage the physiological pain they may be experiencing. Ultimately, your goal is to help patients become more physically, mentally and emotionally healthy, with better mobility, less pain, greater independence and improved quality of life."
# ]

# PATIENT_STRATEGIES = [
#     """You are coming in to discuss an automobile accident. You are very anxious and have been having trouble sleeping. You are also experiencing flashbacks of the accident. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent divorce. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent job loss. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent death in the family. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent move. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent breakup. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent illness. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent injury. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent diagnosis. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
#     """You are coming in to discuss a recent surgery. You are feeling very sad and lonely. You are also experiencing a lot of guilt and shame. You are very nervous and have been having trouble concentrating."""
# ]


# prompts for task strategy persona convos


# CHITCHAT_STRAT_PERSONA_PROMPT1 = f"""{GENERIC_CHITCHAT_PROMPT1}\n<CHITCHAT_STRATEGY>\nThis is your story: <CHITCHAT_BACKGROUND>"""
# CHITCHAT_STRAT_PERSONA_PROMPT2 = f"""{GENERIC_CHITCHAT_PROMPT2}\n<CHITCHAT_STRATEGY>\nThis is your story: <CHITCHAT_BACKGROUND>"""

# THERAPIST_STRAT_PERSONA_PROMPT = f"""{GENERIC_THERAPIST_PROMPT}\n<THERAPIST_STRATEGY>\nThis is your story: <THERAPIST_BACKGROUND>"""
# PATIENT_STRAT_PERSONA_PROMPT = f"""{GENERIC_PATIENT_PROMPT}\n<PATIENT_STRATEGY>\nThis is your story: <PATIENT_BACKGROUND>"""
