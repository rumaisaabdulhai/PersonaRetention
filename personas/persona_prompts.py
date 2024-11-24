"""
Stores all the prompts used.
"""

generate_persona_prompt = f"""Provide a background for <type> that includes all of the following information, as if it was written by a person using \
    natural language. It should not be presented as a list, but as if someone was providing the information naturally in an introduction \
    in the first person. It should be contained to one paragraph. \
    Name\
    Age\
    Where they're from\
    Where their parents are from Religion and extent it is adhered to\
    Socioeconomic status - current\
    Socioeconomic status - childhood\
    Siblings (including name, age, relationship)\
    Languages and dialects spoken\
    Sexual orientation\
    Gender identity\
    Relationship status\
    Significant past relationships\
    Occupation - current and past\
    Education\
    Cultural influences\
    Political views\
    Health and wellness\
    Hobbies and interests\
    Values and Beliefs outside religion\
    Fears and anxieties\
    Life Goals and Ambitions Defining Life Experiences\
    Friendship Circles\
    Daily Routine and Habits\
    Pet ownership - current and past\
    Favorite Media\
    Living Situation\
    Places Traveled to\
    An example: "My name is Aura Samanta. I'm 34 and grew up in Seattle, though my parents emigrated from Mumbai. I'm non-binary (they/them), bisexual, and in a happy relationship with my partner, Alex. My family struggled financially during my childhood, but now I'm middle class, working as a UX designer after studying design in college. I respect my family's Hindu traditions but identify as agnostic. My younger sister Priya, 30, is my closest confidant, and while we mainly spoke English growing up, I know bits of Hindi and Marathi. I'm passionate about art, hiking, and vegetarian cooking, and I value kindness, creativity, and social justice, aligning with my progressive political views. A defining moment was backpacking across Europe, which shaped my love for travel and multiculturalism. I live in a cozy apartment with my rescue cat, Luna, and unwind with books, podcasts, or Studio Ghibli films. Though I've traveled extensively, I dream of exploring South America next, striving to create meaningful work and live with curiosity and compassion."
    """

extract_persona_prompt = """
    From the following biography, generate one sentence summaries for each of the attributes of the Persona class with similar structure to the accompanying examples. The persona class is structured as follows:

    class Persona:
        def __init__(self):
            # Comments are to show samples for modular generation
            self.name = ""  # "My name is Jane Doe."
            self.age = ""  # "I am 35 years old."
            self.location_from = ""  # "I am from Houston, Texas."
            self.location_mother_from = "" # "My mother is from Capetown, South Africa."
            self.location_father_from = "" # "My father is from Mumbai, India."
            self.religion = "" # "I am Christian.", "I was raised Jewish but don't practice."
            self.socioeconomic_status = "" # I am middle class.", "I am a wealthy homeowner.", "I am struggling to make ends meet."
            self.siblings = "" # "I am an only child." "I have a brother and a sister."
            self.languages_spoken = "" # "I speak only English.", "I speak Portuguese, English, and Bengali."
            self.sexual_orientation = "" # "I am heterosexual.", "I'm bisexual."
            self.gender_identity = "" # "I am a woman.", "I identify as nonbinary."
            self.relationship_status = "" # "I'm currently single.", "I have been married for 4 years."
            self.significant_past_relationships = "" # "I was engaged for 2 years but it was called off.", "I have never been in a long term relationship."
            self.occupation_current = "" # "I am a landscaper.", "I do small business consulting."
            self.occupation_past = "" # "I used to be a frycook in high school.", "In college I worked as a librarian's assistant."
            self.education = "" # "I have my G.E.D.", "I have a bachelors in Finance from Northeastern University."
            self.cultural_influences = "" # "I grew up in a devout Mormon community.", "I grew up in a Nigerian Igbo community."
            self.political_views = "" # "I don't follow politics.", "I am a democratic socialist."
            self.health = "" # "I am very healthy and exercise often, but have a bad knee.", "I am legally blind."
            self.hobbies_and_interests = "" # "I enjoy painting and hiking.", "I am a huge history buff."
            self.beliefs_and_values = "" # "I believe minimizing our carbon footprint is imperative.", "I am vegan for moral reasons."
            self.fears_and_anxieties = "" # "I am deathly afraid of heights.", "I have anxiety with personal conflict."
            self.life_goals_and_ambitions = "" # "I hope to retire at an early age.", "I want to start my own company.", "All I want out of life is a big family."
            self.defining_life_experiences = "" # "I was orphaned at a young age.", "I would bake with my grandma every Sunday growing up."
            self.friendship_circles = "" # "I've had the same few best friends for years.", "I have no close friends but run in a lot of social circles."
            self.daily_routine_and_habits = "" # "I do a morning yoga routine every morning before work.", "I spend an hour reading every night before I go to bed."
            self.pet_ownership = "" # "I don't have any pets.", "I have a black laborador retriever named Sparky."
            self.favorite_media = "" # "I have rewatched the TV show Friends a dozen times.", "I watch football games every night."
            self.living_situation = "" # "I currently live by myself in a studio apartment.", "I live in a single-family home with my husband and two children."
            self.places_traveled = "" # "I have never left my home city.", "I have traveled to most of South America, and a few countries in Europe."

    Biography: <biography>

    Format the output as follows, with the attribute from the class matching the key for the attribute:
    name: <summary>
    age: <summary>
    ...

    """