import re
from typing import Iterable


KEYWORD_TO_FACTS = {
    "programming": {"likes_programming"},
    "coding": {"likes_programming"},
    "software": {"likes_programming"},
    "electronics": {"likes_electronics"},
    "circuits": {"likes_electronics"},
    "robotics": {"likes_electronics", "likes_programming"},
    "math": {"likes_math"},
    "mathematics": {"likes_math"},
    "algebra": {"likes_math"},
    "calculus": {"likes_math"},
    "statistics": {"likes_math"},
    "physics": {"likes_physics"},
    "chemistry": {"likes_chemistry"},
    "biology": {"likes_biology"},
    "medicine": {"likes_biology", "likes_helping_people"},
    "design": {"likes_design"},
    "drawing": {"likes_design"},
    "art": {"likes_design"},
    "creative": {"likes_design"},
    "creativity": {"likes_design"},
    "law": {"likes_law"},
    "legal": {"likes_law"},
    "debate": {"likes_law"},
    "argue": {"likes_law"},
    "arguing": {"likes_law"},
    "writing": {"likes_writing"},
    "write": {"likes_writing"},
    "people": {"likes_helping_people"},
    "helping": {"likes_helping_people"},
    "help": {"likes_helping_people"},
    "solving problems": {"likes_problem_solving"},
    "problem solving": {"likes_problem_solving"},
    "problems": {"likes_problem_solving"},
    "analysis": {"likes_problem_solving"},
    "analyzing": {"likes_problem_solving"},
    "technology": {"likes_technology"},
    "tech": {"likes_technology"},
}


RULES = [
    {
        "name": "R1",
        "if": {"likes_math"},
        "then": {"analytical_profile"},
        "because": "Math interest suggests analytical thinking.",
    },
    {
        "name": "R2",
        "if": {"likes_programming"},
        "then": {"computing_profile"},
        "because": "Programming interest suggests comfort with software and systems.",
    },
    {
        "name": "R3",
        "if": {"likes_electronics"},
        "then": {"hardware_profile"},
        "because": "Electronics interest suggests comfort with hardware and physical systems.",
    },
    {
        "name": "R4",
        "if": {"likes_design"},
        "then": {"creative_profile"},
        "because": "Design interest suggests a creative and user-focused profile.",
    },
    {
        "name": "R5",
        "if": {"likes_biology"},
        "then": {"life_science_profile"},
        "because": "Biology interest points toward life sciences and health-related paths.",
    },
    {
        "name": "R6",
        "if": {"likes_physics"},
        "then": {"physical_science_profile"},
        "because": "Physics interest points toward physical sciences and engineering thinking.",
    },
    {
        "name": "R7",
        "if": {"likes_chemistry"},
        "then": {"chemical_science_profile"},
        "because": "Chemistry interest points toward chemical sciences and process-based careers.",
    },
    {
        "name": "R8",
        "if": {"likes_law"},
        "then": {"argumentation_profile"},
        "because": "Law-related interests suggest argumentation and policy-oriented strengths.",
    },
    {
        "name": "R9",
        "if": {"likes_helping_people"},
        "then": {"service_profile"},
        "because": "Helping people suggests a service and care-oriented profile.",
    },
    {
        "name": "R10",
        "if": {"likes_writing"},
        "then": {"communication_profile"},
        "because": "Writing interest suggests communication strength.",
    },
    {
        "name": "R11",
        "if": {"likes_problem_solving"},
        "then": {"problem_solver_profile"},
        "because": "Problem-solving interest suggests persistence with complex tasks.",
    },
    {
        "name": "R12",
        "if": {"likes_technology"},
        "then": {"technology_profile"},
        "because": "Technology interest points toward modern digital and technical environments.",
    },
    {
        "name": "R13",
        "if": {"computing_profile"},
        "then": {"career_software_engineering"},
        "because": "A computing profile alone already supports software-oriented careers.",
    },
    {
        "name": "R14",
        "if": {"hardware_profile"},
        "then": {"career_electronic_engineering"},
        "because": "A hardware profile alone supports electronic engineering careers.",
    },
    {
        "name": "R15",
        "if": {"analytical_profile"},
        "then": {"career_applied_mathematics"},
        "because": "An analytical profile alone supports mathematics-oriented careers.",
    },
    {
        "name": "R16",
        "if": {"physical_science_profile"},
        "then": {"career_physics"},
        "because": "A physical science profile alone supports physics-related careers.",
    },
    {
        "name": "R17",
        "if": {"chemical_science_profile"},
        "then": {"career_chemistry"},
        "because": "A chemical science profile alone supports chemistry-related careers.",
    },
    {
        "name": "R18",
        "if": {"creative_profile"},
        "then": {"career_graphic_design"},
        "because": "A creative profile alone supports design careers.",
    },
    {
        "name": "R19",
        "if": {"life_science_profile"},
        "then": {"career_biology"},
        "because": "A life science profile alone supports biology-related careers.",
    },
    {
        "name": "R20",
        "if": {"argumentation_profile"},
        "then": {"career_law"},
        "because": "An argumentation profile alone supports law-related careers.",
    },
    {
        "name": "R21",
        "if": {"technology_profile"},
        "then": {"career_information_technology"},
        "because": "A technology profile alone supports information technology careers.",
    },
    {
        "name": "R22",
        "if": {"analytical_profile", "computing_profile"},
        "then": {"career_software_engineering", "career_data_science"},
        "because": "Analytical plus computing interests match software and data careers.",
    },
    {
        "name": "R23",
        "if": {"computing_profile", "hardware_profile"},
        "then": {"career_iot_engineering", "career_mechatronics"},
        "because": "Computing plus hardware interests match IoT and mechatronics paths.",
    },
    {
        "name": "R24",
        "if": {"analytical_profile", "physical_science_profile"},
        "then": {"career_physics", "career_engineering"},
        "because": "Analytical and physics interests support physics and engineering careers.",
    },
    {
        "name": "R25",
        "if": {"creative_profile", "technology_profile"},
        "then": {"career_ui_ux_design"},
        "because": "Creative and technology interests fit UI/UX design.",
    },
    {
        "name": "R26",
        "if": {"creative_profile", "computing_profile"},
        "then": {"career_interactive_design"},
        "because": "Creative and computing interests fit interactive digital design.",
    },
    {
        "name": "R27",
        "if": {"life_science_profile", "service_profile"},
        "then": {"career_medicine", "career_biomedical_engineering"},
        "because": "Biology plus helping people fits medicine and biomedical engineering.",
    },
    {
        "name": "R28",
        "if": {"life_science_profile", "technology_profile"},
        "then": {"career_biotechnology"},
        "because": "Biology plus technology fits biotechnology.",
    },
    {
        "name": "R29",
        "if": {"chemical_science_profile", "analytical_profile"},
        "then": {"career_chemical_engineering", "career_chemistry"},
        "because": "Chemistry plus analytical thinking fits chemistry and chemical engineering.",
    },
    {
        "name": "R30",
        "if": {"argumentation_profile", "communication_profile"},
        "then": {"career_law"},
        "because": "Law-oriented and communication strengths fit legal careers.",
    },
    {
        "name": "R31",
        "if": {"service_profile", "communication_profile"},
        "then": {"career_psychology", "career_education"},
        "because": "Helping people and communication fit psychology and education.",
    },
    {
        "name": "R32",
        "if": {"analytical_profile", "problem_solver_profile"},
        "then": {"career_applied_mathematics"},
        "because": "Analytical and problem-solving strengths fit applied mathematics.",
    },
    {
        "name": "R33",
        "if": {"technology_profile", "problem_solver_profile"},
        "then": {"career_information_technology"},
        "because": "Technology and problem-solving fit IT-oriented paths.",
    },
]


CAREER_LABELS = {
    "career_software_engineering": "Software Engineering",
    "career_data_science": "Data Science",
    "career_iot_engineering": "IoT Engineering",
    "career_mechatronics": "Mechatronics",
    "career_electronic_engineering": "Electronic Engineering",
    "career_physics": "Physics",
    "career_engineering": "Engineering",
    "career_ui_ux_design": "UI/UX Design",
    "career_interactive_design": "Interactive Design",
    "career_graphic_design": "Graphic Design",
    "career_medicine": "Medicine",
    "career_biomedical_engineering": "Biomedical Engineering",
    "career_biology": "Biology",
    "career_biotechnology": "Biotechnology",
    "career_chemical_engineering": "Chemical Engineering",
    "career_chemistry": "Chemistry",
    "career_law": "Law",
    "career_psychology": "Psychology",
    "career_education": "Education",
    "career_applied_mathematics": "Applied Mathematics",
    "career_information_technology": "Information Technology",
}

FACT_LABELS = {
    "likes_programming": "Likes programming",
    "likes_electronics": "Likes electronics",
    "likes_math": "Likes math",
    "likes_physics": "Likes physics",
    "likes_chemistry": "Likes chemistry",
    "likes_biology": "Likes biology",
    "likes_design": "Likes design",
    "likes_law": "Likes law",
    "likes_writing": "Likes writing",
    "likes_helping_people": "Likes helping people",
    "likes_problem_solving": "Likes problem solving",
    "likes_technology": "Likes technology",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_facts_from_text(text: str) -> set[str]:
    normalized = normalize_text(text)
    facts = set()

    for keyword, mapped_facts in KEYWORD_TO_FACTS.items():
        if keyword in normalized:
            facts.update(mapped_facts)

    return facts


def extract_facts_from_history(chat_history: Iterable[dict] | None) -> set[str]:
    facts = set()
    if not chat_history:
        return facts

    for message in chat_history:
        if message.get("role") == "user":
            facts.update(extract_facts_from_text(message.get("content", "")))
    return facts


def forward_chain(initial_facts: set[str]) -> tuple[set[str], list[str]]:
    facts = set(initial_facts)
    steps = []
    fired_rules = set()

    changed = True
    while changed:
        changed = False
        for rule in RULES:
            if rule["name"] in fired_rules:
                continue
            if rule["if"].issubset(facts):
                new_facts = rule["then"] - facts
                fired_rules.add(rule["name"])
                if new_facts:
                    facts.update(new_facts)
                    steps.append(
                        f"{rule['name']}: because {sorted(rule['if'])} were true, inferred {sorted(new_facts)}. {rule['because']}"
                    )
                    changed = True

    return facts, steps


def build_response(initial_facts: set[str], inferred_facts: set[str], steps: list[str]) -> str:
    career_facts = [fact for fact in inferred_facts if fact.startswith("career_")]
    career_names = [CAREER_LABELS[fact] for fact in career_facts if fact in CAREER_LABELS]

    if not initial_facts:
        return (
            "### Result\n"
            "I do not have enough facts yet.\n\n"
            "### What I Need\n"
            "Tell me some interests such as math, programming, biology, design, law, physics, or helping people.\n\n"
            "### Inference Log\n"
            "- No rules fired because no recognizable facts were provided."
        )

    fact_labels = [FACT_LABELS.get(fact, fact.replace("_", " ").title()) for fact in sorted(initial_facts)]
    facts_section = "\n".join(f"- {label}" for label in fact_labels)

    if not career_names:
        return (
            "### Result\n"
            "I extracted some facts, but I do not yet have enough information to infer a strong career conclusion.\n\n"
            f"### Facts Base\n{facts_section}\n\n"
            "### Inference Log\n"
            + ("\n".join(f"- {step}" for step in steps) if steps else "- No rules fired yet.")
            + "\n\n### Next Step\nTell me one or two more interests so I can continue the forward chaining."
        )

    unique_careers = []
    for career in career_names:
        if career not in unique_careers:
            unique_careers.append(career)

    steps_section = "\n".join(f"- {step}" for step in steps) if steps else "- No extra inference steps were needed."
    careers_section = "\n".join(f"- {career}" for career in unique_careers)

    return (
        "### Result\n"
        "Based on the facts you provided and the inferred facts from the rule engine, these are the best-matching careers.\n\n"
        f"### Facts Base\n{facts_section}\n\n"
        "### Recommended Careers\n"
        f"{careers_section}\n\n"
        "### Inference Log\n"
        f"{steps_section}"
    )


def model_response(msg=None, chat_history=None):
    if chat_history:
        initial_facts = extract_facts_from_history(chat_history)
    else:
        initial_facts = extract_facts_from_text(msg or "")

    inferred_facts, steps = forward_chain(initial_facts)
    return build_response(initial_facts, inferred_facts, steps)


if __name__ == "__main__":
    print(model_response("I like law, writing, and debate"))
