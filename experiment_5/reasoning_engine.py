# reasoning_engine.py
# Handles rule matching, inference and scoring

from rules import RULES
from knowledge_base import CONDITIONS

class ReasoningEngine:
    def __init__(self):
        self.rules = RULES
        self.conditions = CONDITIONS

    def match_rules(self, facts: set) -> list:
        """
        Forward-chaining inference mechanism.
        Checks each rule against the provided facts.
        """
        matches = []
        for rule in self.rules:
            # Check if all conditions in the rule are present in facts
            rule_conditions = set(rule["conditions"])
            
            matched_symptoms = rule_conditions.intersection(facts)
            missing_symptoms = rule_conditions - facts
            
            # Simple scoring: percentage of rule conditions met
            if len(rule_conditions) > 0:
                score = (len(matched_symptoms) / len(rule_conditions)) * 100
            else:
                score = 0
                
            # If at least a partial match (e.g. > 0% for demonstration, but let's say >= 50% for relevance)
            # The assignment mentions "If 3 out of 4 symptoms match -> 75% rule match"
            if score > 0:
                matches.append({
                    "rule": rule,
                    "score": score,
                    "matched_symptoms": list(matched_symptoms),
                    "missing_symptoms": list(missing_symptoms)
                })
                
        # Rank by score descending
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches

    def evaluate_emergency(self, facts: set, emergency_symptoms: set) -> list:
        """Check if any emergency symptoms are present."""
        return list(facts.intersection(emergency_symptoms))
