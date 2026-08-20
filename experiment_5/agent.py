# agent.py
# AI-agent orchestration

from reasoning_engine import ReasoningEngine
from knowledge_base import EMERGENCY_SYMPTOMS

class RuleBasedReasoningAgent:
    def __init__(self):
        self.engine = ReasoningEngine()
        self.emergency_symptoms = EMERGENCY_SYMPTOMS

    def analyze(self, symptoms: list) -> dict:
        """
        Processes symptoms (Step 1 - Receive facts), evaluates them (Step 2/3 - Match/Score),
        and returns results (Step 4/5 - Rank/Explain).
        """
        # Step 1: Convert symptoms into structured facts
        facts = set(symptom.lower() for symptom in symptoms if symptom.strip())
        
        # Check for emergency
        emergencies = self.engine.evaluate_emergency(facts, self.emergency_symptoms)
        
        # Step 2 & 3: Match rules and calculate scores
        # Step 4: Rank possible matches
        # We only keep strong matches (e.g., score >= 50%) for the suggestions
        all_matches = self.engine.match_rules(facts)
        strong_matches = [m for m in all_matches if m["score"] >= 50]
        
        return {
            "facts": list(facts),
            "emergencies": emergencies,
            "matches": strong_matches,
            "all_evaluated": all_matches
        }
