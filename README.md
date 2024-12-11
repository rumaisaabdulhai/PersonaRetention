# README

## Persona Generation

### File: `personas/generate_persona.py`
- **Setup**:
  - Set the `NUM_PERSONAS` and `MODE` values to reflect the amount and type of personas you want to generate.
  - Prompts are found in `persona_prompts.py` and categories can be edited as desired. If edited, the `Persona` class should be given the same edits. Future updates will unpack this text from the `Persona` class so that changes do not have to be made in multiple locations.
- **Run**:
  - Execute `generate_persona.py`.
- **Output**:
  - Personas will be generated in `personas/data`. Review them to ensure:
    - Proper population of the category information.
    - Alignment with the persona.
    - Diversity of data (if lacking, this can be fixed through multiple regenerations or by specifically prompting for elements that are not diverse to use a preselection of items).

## Question Generation

### File: `qa/generate_qa.py`
- **Setup**:
  - Set the `INPUT_FILE_NAME` to the name of the persona file you are generating questions and answers for.
  - Set the `OUTPUT_FILE_NAME` to the desired name of the output file.
- **Run**:
  - Execute `generate_qa.py`.
- **Validation**:
  - Generated QA sets take question choices from other models, so they must be evaluated through human validation to ensure:
    - Options are distinct.
    - Incorrect answers cannot be interpreted in a way that makes them true.

## Generate Conversations

### File: `convos/generate_convos.py`
- **Setup**:
  - Set parameters at the top of the file for your experiment.
  - Observe and modify conversational prompts in `convo_prompts.py` as desired.
  - Comment or uncomment functions in `main()` to select the desired conversation types. Future updates will implement modes similar to persona generation.
- **Run**:
  - Execute `generate_convos.py`.
- **Output**:
  - Conversations will be generated for each combination of strategy and stored in the `task_strategy_persona_data` folder (assuming `USE_PERSONAS = true`).

## Question and Answer Sets

### File: `convos/generate_qa`
- **Setup**:
  - Ensure `persona number`, `task`, and `qa directory names` match the global variables.
  - Select evaluations to perform based on the set being used by commenting functions in `main`. The file selection depends on the naming convention matching that used in the research (it should generate automatically if no changes have been made).
- **Output**:
  - Generated QA sets will be stored in separate folders for each run.

### File: `convos/qa_evaluator.py`
- **Setup**:
  - Ensure the `QA_FOLDER` name matches the naming conventions of the folders you are checking. Numbers will be added as the program looks through `NUM_FOLDERS`, which, if following the steps, will work with the folder name scheme.

## Persona Consistency Evaluation

### File: `convos/persona_consistency_evaluation.py`
- **Note**: This program was used to establish a proof-of-concept. This evaluation should ideally be human-performed.
- **Setup**:
  - Ensure `conversation_directory` in `main` matches your directory.
- **Run**:
  - Execute `persona_consistency_evaluation.py`.

## Task Strategy Evaluation

### File: `convos/strategy_evaluation.py`
- **Note**: This program was used to establish a proof-of-concept. This evaluation should ideally be human-performed.
- **Setup**:
  - Ensure `conversation_directory` in `main` matches your directory.
- **Run**:
  - Execute `strategy_evaluation.py`.

---

**Note**: The environment requires an `OPENAI_API_KEY` to be saved as an OS variable for successful execution of the scripts.
