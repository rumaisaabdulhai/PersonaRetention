from openai import OpenAI
import os
import random

# Number of back and forth exchanges between LLMs
NUM_EXCHANGES = 5 
MODEL = "gpt-4o-mini"
name1 = "Agent 1"
name2 = "Agent 2"

# Number of questions to ask about each persona
NUM_QUESTIONS = 10

background_text1 = """
I'm 31 and grew up in SC with my parents and three brothers. I was a ballerina for 11 years. I loved exploring the world with
my family. My life was very close knit. I loved being a dancer and enjoyed school very much. I went to Ohio State University
in Columbus, Ohio where I majored in Criminology and Spanish. I graduated with honors and then earned a masters in
Criminal Justice and Peace and Justice. I spent a year volunteering in Costa Rica. I've always been drawn to teach and be in
the academic setting. I've only taught high school for 1.5 years. I thoroughly enjoy my students and consider them my
community. I live and eat with them. I give them more than just content in history, I give them a life lesson. I want to build
these students into model citizens who are contributing to a better community everyday and I know teaching can help me
achieve that. My students come from a wide diversity of backgrounds. They are in public school because their families have
extremely low incomes. Most of my students come from single parent households, some do not even have one. My students
don't have mentors at home who can help them navigate what college will look like or what career will be the best for them.
A lot of my students have never been outside of the county or traveled at all. Students like these need something to look
forward to and teaching is exactly that. I want to inspire them to be greater than they have ever imagined they could be. I
want them to know they have other people in this world rooting for them and helping them achieve the things they say they
want. I want them to know that the decisions they make today will change their tomorrow.
"""

questions1 = [
    "How old are you?",
    "Where did you grow up?",
    "How many years did you practice ballet?",
    "Which university did you attend?",
    "What was your undergraduate major?",
    "What did you earn your master's degree in?",
    "Where did you spend a year volunteering?",
    "How long have you been teaching high school?",
    "What is the primary background of your students?",
    "What is your goal as a teacher?"
]

answers1 = [
    "31",
    "South Carolina (SC) with your parents and three brothers",
    "11 years",
    "Ohio State University in Columbus, Ohio",
    "Criminology and Spanish",
    "Criminal Justice and Peace and Justice",
    "Costa Rica",
    "1.5 years",
    "They come from low-income families, often from single-parent households, and many have limited travel or cultural experiences outside of their county",
    "To inspire students to become model citizens, contribute to a better community, and achieve more than they imagined possible by making impactful life decisions"
]

background_text2 = """
I've spent over half of my life in the Wild West of Oakland. I was born in Oakland, I grew up in Oakland, and I’ve raised a
family in the East Bay since the 1980s. I have a 27 year old son, a daughter who will be 23 in May, and a step daughter who
will be 13 this May. I have a great deal of respect for the richness that is the East Bay and the beautiful cities of Oakland,
Berkeley, and Richmond. It is also a place of great pain and suffering. I believe that the culture of Oakland is extraordinarily
important and the cultural and spiritual truths of our ancestors are being silenced and even destroyed by the new class of city
government and their underlings who view people of color as “collateral damage” in their pursuit of gentrification and profit. I
grew up on the streets of West Oakland at a time when families were made up of 10 and more. 20 to 25 kids played in the
street in front of 10 to 12 unit apartment buildings. A few black teenage punks were seen cruising the neighborhood but
everyone knew each other and cared about each other. I was witness to horrible tragedy, deaths, drug dealing, etc. etc. The
point is that I was not afraid to be in the streets of West Oakland and I still am not afraid to be on the streets of West
Oakland. I know it well and I know who I am as a black man in West Oakland.
Back in the mid 1970s, I went to The UC Berkeley where I studied fine art and photography and studied with the great
photographer Minor White, while being mentored by David Harris. After a few years working at a high tech company (which I
could not stand), I decided to devote my life to spiritual and religious inquiry. I was already married and had two children. In
1984, I received a Bachelor of Science degree in religious studies from the Graduate Theological Union in Berkeley, followed
by a Masters of Theological Studies from Pacific School of Religion in Berkeley, and a Masters of Divinity from Starr King
School for the Ministry in Berkeley, followed by a PhD from New College of California in San Francisco in the 1990s. In the
1980s, I began working at San Quentin Prison, teaching African American religious history to African American inmates.
Since then, I have developed a successful career as an independent contractor as a consultant, business coach, and
motivational speaker.
"""

questions2 = [
    "Where were you born?",
    "When did you start raising a family in the East Bay?",
    "How old is your son?",
    "How old will your daughter be in May?",
    "What is your view on gentrification in Oakland?",
    "What university did you attend in the mid-1970s?",
    "Who was one of the notable photographers you studied with?",
    "What degrees did you earn from religious institutions in Berkeley?",
    "In which prison did you begin teaching African American religious history in the 1980s?",
    "What is your current profession?"
]

answers2 = [
    "Oakland, California.",
    "Since the 1980s.",
    "27 years old.",
    "23 years old.",
    "You believe that gentrification is causing harm to people of color and that the cultural and spiritual heritage of Oakland is being silenced and destroyed.",
    "University of California, Berkeley (UC Berkeley).",
    "Minor White.",
    "A Bachelor of Science in religious studies, a Masters of Theological Studies, and a Masters of Divinity.",
    "San Quentin Prison.",
    "An independent contractor as a consultant, business coach, and motivational speaker."
]

# https://www.wondermind.com/article/conversation-starters/
convo_questions = ["What's the most adventurous thing you've ever done?",
             "If money weren't a problem, what would you do on your average Tuesday?",
             "If you could have a conversation with anyone in history, who would it be and what would you ask them?",
             "What is the biggest compliment you could receive?",
             "What's one experience you believe everyone should have at least once?", 
             "If you had three wishes, what would they be?", 
             "If you could wake up tomorrow having gained one ability or quality, what would it be?", 
             "What makes you get up in the morning?",
             "What are you most proud of?", 
             "Do you have a favorite quote that inspires you?", 
             "If you could pick one TV show to describe the relationship you have with your family, what would it be?", 
             "What's the most generous thing you've ever done for yourself?",
             "You've had a rough day at work. What do you do to relax?",
             "If there was a museum featuring artifacts from your life, what items would be must-see exhibits, and what stories would they tell?"]

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Step 1: Feed each persona into the LLM memory
llm1_memory = [
    {"role": "system", "content": f"You are {name1}. You are talking to {name2}. This is your story:" + background_text1}
]
llm2_memory = [
    {"role": "system", "content": f"You are {name2}. You are talking to {name1}. This is your story:" + background_text2}
]

# random question idxs
shuffled_idxs = list(range(len(questions1)))
random.shuffle(shuffled_idxs)
assert len(convo_questions) % 2 == 0, "NUM_EXCHANGES must be an even number"

def simulate_conversation():
    i = 0
    for turn in range(NUM_EXCHANGES):
        # Sample a random question
        random_question = convo_questions[shuffled_idxs[i]]
        i += 1
        content = f"{name1}: {random_question}"
        print(content + "\n")

        # LLM 1 asks the question, therefore it is the assistant
        llm1_memory.append({"role": "assistant", "content": content})

        # LLM 2 is being asked the question, therefore LLM 1 is the user
        llm2_memory.append({"role": "user", "content": content})

        # LLM 2 responds to the question
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm2_memory,
            max_completion_tokens=100
        )

        answer = response.choices[0].message.content
        print(f"{answer}")

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "user", "content": answer})

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "assistant", "content": answer})

        # Sample a random question
        random_question = convo_questions[shuffled_idxs[i]]
        i += 1
        content = f"{name2}: {random_question}"
        print(content + "\n")

        # LLM 2 asks the question, therefore it is the assistant
        llm2_memory.append({"role": "assistant", "content": content})

        # LLM 1 is being asked the question, therefore LLM 2 is the user
        llm1_memory.append({"role": "user", "content": content})

        # LLM 1 responds to the question
        response = client.chat.completions.create(
            model=MODEL,
            messages=llm1_memory,
            max_completion_tokens=100
        )

        answer = response.choices[0].message.content
        print(f"{answer}")

        # add the response to LLM 2's memory
        llm2_memory.append({"role": "user", "content": answer})

        # add the response to LLM 1's memory
        llm1_memory.append({"role": "assistant", "content": answer})

        print("\n")

        # Ask a set of random questions about each persona
        idxs = random.sample(range(len(questions1)), NUM_QUESTIONS)

        num_right_llm1 = 0
        num_right_llm2 = 0

        for idx in idxs:
            # ask a background question to LLM 1
            question = questions1[idx]
            content = f"{question} Please give short, straightforward answers."
            print(f"{content}\n")
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm1_memory + [{"role": "system", "content": content}],
                max_completion_tokens=100
            )
            answer = response.choices[0].message.content

            # Ask LLM if the response is correct
            content = f"Given the background story, for the question: {question} which is asked to {name1}, \
            is the following response correct: {answer}. The real answer is {answers1[idx]}. Please respond with 1 for yes and 0 for no."
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": background_text1 + "\n" + content}],
                max_completion_tokens=100
            )
            is_correct = response.choices[0].message.content
            if is_correct == "1":
                # print(f"LLM 1 responded correctly! The answer was {answer} and the real answer was {answers1[idx]}\n")
                num_right_llm1 += 1
            else:
                print(f"LLM incorrect response! The answer was {answer} and the real answer was {answers1[idx]}\n")

            # ask a background question to LLM 2
            question = questions2[idx]
            content = f"{question} Please give short, straightforward answers."
            print(f"{content}\n")
            response = client.chat.completions.create(
                model=MODEL,
                messages=llm2_memory + [{"role": "system", "content": content}],
                max_completion_tokens=100
            )
            answer = response.choices[0].message.content

            # Ask LLM if the response is correct
            content = f"Given the background story, for the question: {question} which is asked to {name2}, \
            is the following response correct: {answer}. The real answer is {answers2[idx]}. Please respond with 1 for yes and 0 for no."
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": background_text2 + "\n" + content}],
                max_completion_tokens=100
            )
            is_correct = response.choices[0].message.content
            if is_correct == "1":
                # print(f"LLM 2 responded correctly! The answer was {answer} and the real answer was {answers2[idx]}\n")
                num_right_llm2 += 1
            else:
                print(f"LLM incorrect response! The answer was {answer} and the real answer was {answers2[idx]}\n")




if __name__ == "__main__":
    simulate_conversation()