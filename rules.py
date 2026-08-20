# rules.py
# Contains explicit IF-THEN rules for forward chaining

RULES = [
    {
        "id": "R1",
        "conditions": ["fever", "cough", "body ache"],
        "conclusion": "Influenza",
        "explanation": "Fever, cough, and body ache are key indicators of Influenza."
    },
    {
        "id": "R2",
        "conditions": ["runny nose", "sneezing", "sore throat"],
        "conclusion": "Common Cold",
        "explanation": "Runny nose, sneezing, and sore throat match the common cold rule."
    },
    {
        "id": "R3",
        "conditions": ["headache", "nausea"],
        "conclusion": "Migraine",
        "explanation": "Headache and nausea match the migraine rule."
    },
    {
        "id": "R4",
        "conditions": ["fever", "diarrhea", "vomiting"],
        "conclusion": "Gastroenteritis (Stomach Flu)",
        "explanation": "Fever, diarrhea, and vomiting match the gastrointestinal rule."
    },
    {
        "id": "R5",
        "conditions": ["itchy eyes", "sneezing", "runny nose"],
        "conclusion": "Allergies",
        "explanation": "Itchy eyes, sneezing, and runny nose match the allergy rule."
    },
    {
        "id": "R6",
        "conditions": ["fever", "loss of smell", "loss of taste", "dry cough"],
        "conclusion": "COVID-19",
        "explanation": "Loss of smell/taste along with fever and dry cough match the COVID-19 rule."
    },
    {
        "id": "R7",
        "conditions": ["sore throat", "fever", "pain when swallowing"],
        "conclusion": "Strep Throat",
        "explanation": "Severe sore throat with fever and pain swallowing suggests Strep Throat."
    },
    {
        "id": "R8",
        "conditions": ["nausea", "vomiting", "diarrhea", "abdominal pain"],
        "conclusion": "Food Poisoning",
        "explanation": "Sudden onset of vomiting, diarrhea, and abdominal pain matches food poisoning."
    },
    {
        "id": "R9",
        "conditions": ["high fever", "severe headache", "joint pain", "muscle pain"],
        "conclusion": "Dengue Fever",
        "explanation": "High fever combined with severe joint/muscle pain suggests Dengue."
    },
    {
        "id": "R10",
        "conditions": ["fever", "chills", "sweating"],
        "conclusion": "Malaria",
        "explanation": "Cycles of fever, chills, and heavy sweating match the malaria rule."
    },
    {
        "id": "R11",
        "conditions": ["persistent cough", "night sweats", "weight loss"],
        "conclusion": "Tuberculosis",
        "explanation": "A persistent cough with night sweats and weight loss is a classic TB pattern."
    },
    {
        "id": "R12",
        "conditions": ["fatigue", "weakness", "pale skin", "dizziness"],
        "conclusion": "Anemia",
        "explanation": "Fatigue accompanied by pale skin and dizziness matches the anemia rule."
    },
    {
        "id": "R13",
        "conditions": ["severe abdominal pain", "nausea", "fever"],
        "conclusion": "Appendicitis",
        "explanation": "Severe abdominal pain with nausea and fever suggests Appendicitis."
    },
    {
        "id": "R14",
        "conditions": ["shortness of breath", "wheezing", "chest tightness"],
        "conclusion": "Asthma",
        "explanation": "Wheezing, shortness of breath, and chest tightness match the asthma rule."
    }
]
