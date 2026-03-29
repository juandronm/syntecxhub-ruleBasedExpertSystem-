# 🧠 Rule-Based Expert System: Career Discovery

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> A lightweight, local, and purely symbolic rule-based expert system that recommends career paths using forward chaining inference—no LLMs required!

---

## 📖 Overview

This project is a small, interactive expert system built with **Python** and **Streamlit**. It takes users' interests as input, converts them into internal facts, and applies a set of *if-then* rules using **forward chaining**. The system then infers logical conclusions to recommend suitable career paths while showing the step-by-step reasoning path.

## ✨ Key Features

- **🧠 Local Symbolic Inference Engine:** Relies on deterministic logic and facts rather than probabilistic LLMs.
- **🔍 Natural Language Fact Extraction:** Analyzes user input for keywords (e.g., `math`, `programming`, `biology`, `design`) and translates them into internal facts (e.g., `likes_math`).
- **⚙️ Forward Chaining:** Applies multiple iterations of `if-then` rules until no new facts can be inferred, allowing for complex, multi-step reasoning.
- **🔎 Explainable AI (XAI):** Generates an **Inference Log** that details exactly *which* rules fired and *why*, providing full transparency into how conclusions were reached.

---

## 🛠️ How It Works

### The Knowledge Base
The system consists of two main components:
1. **Facts Base**: Translates user keywords into standard symbolic facts.
2. **Rule Engine**: A predefined set of logical rules.
   
*Example Rules:*
```text
IF likes_math THEN analytical_profile
IF analytical_profile THEN career_applied_mathematics
IF analytical_profile AND computing_profile THEN career_data_science
```

### The Inference Engine
Starting with facts extracted from the user's input, the system:
1. Scans the rule base to check which rules evaluate to true.
2. Fires those rules to generate **new facts** (e.g., inferred profiles or careers).
3. Repeats the process iteratively until the conclusion state is stable.

---

## 📂 Project Structure

```text
rule-basedExpertSystem/
├── README.md               # You are here!
├── .env                    # Environment variables
└── src/
    ├── main.py             # Streamlit UI & Chatbot Frontend
    └── model.py            # Core logic (Rules, Extraction, Inference)
```

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Create a Virtual Environment
We recommend using `uv` (or standard Python `venv`).
```bash
uv venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
uv pip install streamlit
```

### 3. Run the Application
```bash
streamlit run src/main.py
```

---

## 💡 Example Usage

**User Input:**
> *"I like programming and electronics"*

**System Output:**
- **Extracted Facts:** `likes_programming`, `likes_electronics`
- **Recommended Careers:** `Software Engineer`, `Embedded Systems Engineer`
- **Inference Log:** 
  ```text
  R1: because ['likes_programming'] were true, inferred ['computing_profile'].
  ...
  ```

---

## 🔮 Future Improvements

- [ ] **Negative Facts Support:** Allow users to express dislikes (e.g., *"I do not like biology"*).
- [ ] **Recommendation Ranking:** Sort inferred careers by specificity or confidence level.
- [ ] **Enhanced UI:** Add internal scrolling and cleaner modular sections to the chat panel.
- [ ] **Expanded Knowledge Base:** Add more diverse domains, keywords, and deeper career paths.

---
*Built with ❤️ using Python and Streamlit.*