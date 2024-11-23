generate_qa_together_prompt = """Please carefully read the backstory of this person. \
    Create <num_question> straight-forward questions and answers about this person where \
    the answers are directly found in the backstory. \
    The questions should be multiple choice with <num_multiple_choice> options. \
    The questions should be in second person and the answers should be in first person. \
    Return just the questions and answers. Each question should be fully contained in one line including the multiple choice options. \
    Each question and answer pair should be separated by a new line. Each answer should be a new line after the question. An example looks like: \
    What is your name? A) John B) Mike C) Jessica D) Stacy\n\
    A) John \n \
    How many kids do you have? A) 1 B) 2 C) 3 D) 4\n \
    C) 3"""

generate_qa_separately_prompt = """Please generate a question and answer pair about the following information: <info>. \
    The question should be multiple choice with <num_multiple_choice> options. The question should be in second person. \
    Return just the question and answer. The question should be fully contained \
    in one line including the multiple choice options. The question and answer pair should be separated by a new line. The answer must be as brief and short as possible. An example looks like: \
    What is your name? A) John B) Mike C) Jessica D) Stacy\n\
    A) John"""