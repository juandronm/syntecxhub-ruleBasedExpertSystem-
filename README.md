# Rule-Based Expert System

This project is a small rule-based expert system built with Python and Streamlit. It accepts user interests as input, stores them as facts, applies if-then rules using forward chaining, and recommends career paths based on the inferred conclusions.

## Project Goal

The system was designed to satisfy these requirements:

- build a small rule engine with a facts base
- accept user facts and infer conclusions using forward chaining
- support chaining of rules through multiple inference steps
- show the reasoning path so the user can understand how conclusions were reached

## How It Works

The project uses a local symbolic inference engine instead of relying on an LLM to make the decisions.

### Facts Base

User messages are analyzed for keywords such as:

- `math`
- `programming`
- `biology`
- `law`
- `design`
- `physics`

These keywords are converted into internal facts such as:

- `likes_math`
- `likes_programming`
- `likes_biology`

### Rule Engine

The system contains a set of if-then rules. Example:

```text
IF likes_math THEN analytical_profile
IF analytical_profile THEN career_applied_mathematics
IF analytical_profile AND computing_profile THEN career_data_science
```

### Forward Chaining

The system starts with the initial facts extracted from the user input.

It then:

1. checks which rules can fire
2. adds newly inferred facts
3. repeats the process until no new facts are produced

This allows multi-step inference.

### Inference Log

Each fired rule is recorded so the user can see the reasoning path, for example:

```text
R1: because ['likes_math'] were true, inferred ['analytical_profile'].
R15: because ['analytical_profile'] were true, inferred ['career_applied_mathematics'].
```

## Project Structure

```text
rule-basedExpertSystem/
├── README.md
├── .env
└── src/
    ├── main.py
    └── model.py
```

### Files

- [src/main.py](c:\Users\juanr\OneDrive\Escritorio\SYNTECXHUB\rule-basedExpertSystem\src\main.py)
  Streamlit user interface for the chatbot-style expert system.

- [src/model.py](c:\Users\juanr\OneDrive\Escritorio\SYNTECXHUB\rule-basedExpertSystem\src\model.py)
  Core expert-system logic, including:
  - keyword-to-fact extraction
  - rules base
  - forward chaining
  - explanation output

## How To Run

### 1. Create and activate a virtual environment

```bash
uv venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
uv pip install streamlit
```

### 3. Run the app

```bash
streamlit run src/main.py
```

## Example Inputs

- `I like math`
- `I like programming and electronics`
- `I like biology and helping people`
- `I like law and writing`

## Example Output

The system returns:

- the extracted facts base
- the recommended careers
- the inference log showing how the rules fired

## Notes

- This project is now a real rule-based expert system, not just an LLM prompt wrapper.
- The quality of the result depends on the keywords detected from the user message.
- The system can be extended by adding more keywords, rules, and career conclusions in `src/model.py`.

## Future Improvements

- add support for negative facts such as `I do not like biology`
- rank recommendations by specificity
- add internal scrolling and cleaner UI sections in the chat panel
- expand the rule base with more domains and careers