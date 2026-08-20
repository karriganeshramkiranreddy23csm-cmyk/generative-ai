# knowledge_base.py
# Contains facts, conditions, and medical knowledge representations

CONDITIONS = {
    "Common Cold": {
        "symptoms": {"runny nose", "sneezing", "sore throat", "cough"}
    },
    "Influenza": {
        "symptoms": {"fever", "headache", "body ache", "fatigue", "cough"}
    },
    "Migraine": {
        "symptoms": {"headache", "nausea", "sensitivity to light", "throbbing pain"}
    },
    "Gastroenteritis (Stomach Flu)": {
        "symptoms": {"fever", "diarrhea", "nausea", "vomiting", "abdominal pain"}
    },
    "Allergies": {
        "symptoms": {"itchy eyes", "sneezing", "runny nose"}
    },
    "COVID-19": {
        "symptoms": {"fever", "dry cough", "fatigue", "loss of smell", "loss of taste", "shortness of breath"}
    },
    "Strep Throat": {
        "symptoms": {"sore throat", "fever", "swollen lymph nodes", "pain when swallowing"}
    },
    "Food Poisoning": {
        "symptoms": {"nausea", "vomiting", "diarrhea", "abdominal pain", "weakness"}
    },
    "Dengue Fever": {
        "symptoms": {"high fever", "severe headache", "joint pain", "muscle pain", "skin rash"}
    },
    "Malaria": {
        "symptoms": {"fever", "chills", "sweating", "headache", "muscle pain"}
    },
    "Tuberculosis": {
        "symptoms": {"persistent cough", "weight loss", "night sweats", "fever", "fatigue"}
    },
    "Anemia": {
        "symptoms": {"fatigue", "weakness", "pale skin", "dizziness", "shortness of breath"}
    },
    "Appendicitis": {
        "symptoms": {"severe abdominal pain", "nausea", "vomiting", "fever"}
    },
    "Asthma": {
        "symptoms": {"shortness of breath", "wheezing", "chest tightness", "dry cough"}
    }
}

EMERGENCY_SYMPTOMS = {
    "chest pain",
    "severe difficulty breathing",
    "unconsciousness",
    "coughing up blood",
    "sudden confusion",
    "blue lips or face",
    "seizures"
}
