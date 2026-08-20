import streamlit as st
from agent import RuleBasedReasoningAgent
from knowledge_base import CONDITIONS, EMERGENCY_SYMPTOMS
from rules import RULES

# Initialize the agent
agent = RuleBasedReasoningAgent()

st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺", layout="wide")

st.title("🩺 AI Symptom Checker")
st.subheader("Rule-Based Medical Reasoning Agent")

st.warning("""
**⚠️ EDUCATIONAL DEMONSTRATION ONLY**

This symptom checker is not a medical diagnostic tool.
The results are possible matches based on predefined
educational rules and should not be treated as a diagnosis.

For medical concerns, consult a qualified healthcare
professional.
""")

st.write("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Select Symptoms")
    
    available_symptoms = [
        "Fever", "High fever", "Chills", "Sweating", "Night sweats",
        "Cough", "Dry cough", "Persistent cough", "Coughing up blood",
        "Sore throat", "Pain when swallowing", "Swollen lymph nodes",
        "Runny nose", "Sneezing", "Loss of smell", "Loss of taste",
        "Headache", "Severe headache", "Sensitivity to light", "Throbbing pain",
        "Body ache", "Muscle pain", "Joint pain", "Fatigue", "Weakness",
        "Nausea", "Vomiting", "Diarrhea", "Abdominal pain", "Severe abdominal pain",
        "Shortness of breath", "Severe difficulty breathing", "Wheezing", "Chest tightness", "Chest pain",
        "Itchy eyes", "Skin rash", "Pale skin", "Dizziness", "Weight loss",
        "Sudden confusion", "Blue lips or face", "Seizures", "Unconsciousness"
    ]
    
    selected_symptoms = st.multiselect("Select all that apply:", available_symptoms)
    
    additional_symptom = st.text_input("Enter any other symptom (comma separated):")
    
    col_btn_1, col_btn_2 = st.columns([1, 1])
    with col_btn_1:
        check_btn = st.button("🔍 Check Symptoms", type="primary")
    with col_btn_2:
        reset_btn = st.button("🔄 Reset")
        
    if reset_btn:
        if 'results' in st.session_state:
            del st.session_state['results']
        st.rerun()
    
    if check_btn:
        all_symptoms = list(selected_symptoms)
        if additional_symptom:
            extra = [s.strip().lower() for s in additional_symptom.split(',') if s.strip()]
            all_symptoms.extend(extra)
            
        if not all_symptoms:
            st.error("Please select or enter at least one symptom.")
        else:
            st.session_state['results'] = agent.analyze(all_symptoms)

with col2:
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        if results['emergencies']:
            st.error("""
            **🚨 URGENT SAFETY NOTICE**

            A potentially serious symptom has been reported.
            This educational tool cannot assess emergencies.

            Please seek immediate professional medical assistance
            or contact your local emergency service.
            """)
        else:
            st.markdown("### Possible Rule-Based Matches")
            matches = results['matches']
            
            if not matches:
                st.info("""
                No strong rule-based match was found.

                The current educational knowledge base may not contain
                a rule covering this combination of symptoms.

                This does not mean that nothing is wrong.

                Please consult a qualified healthcare professional
                if you are concerned about your symptoms.
                """)
            else:
                for match in matches:
                    rule = match['rule']
                    with st.expander(f"🩺 Possible Match: {rule['conclusion']}", expanded=True):
                        st.markdown(f"**Rule Match Score:** {match['score']:.0f}%")
                        st.markdown("""
                        **Meaning:**
                        This percentage of the symptoms required by this predefined educational
                        rule were present.
                        
                        This is NOT an 80% probability of having the condition.
                        """)
                        
                        st.markdown("**Matched symptoms:**")
                        for sym in match['matched_symptoms']:
                            st.markdown(f"- ✓ {sym.capitalize()}")
                            
                        st.markdown("**Missing symptoms:**")
                        if match['missing_symptoms']:
                            for sym in match['missing_symptoms']:
                                st.markdown(f"- ❌ {sym.capitalize()}")
                        else:
                            st.markdown("- None")
                            
                        st.markdown("**Reason:**")
                        st.write("The selected symptoms satisfy the predefined educational rule for this condition.")
                        st.caption("⚠️ This is not a diagnosis.")

# Expanders for educational demonstration
st.write("---")

with st.expander("🔬 Knowledge Representation"):
    st.markdown("### Facts")
    if 'results' in st.session_state:
        for fact in st.session_state['results']['facts']:
            st.code(fact)
    else:
        st.write("No facts generated yet.")
        
    st.markdown("### Rules")
    for rule in RULES:
        st.code(f"{rule['id']}:\nIF {' AND '.join(rule['conditions'])}\nTHEN possible {rule['conclusion']}")

    st.markdown("### Inference")
    if 'results' in st.session_state:
        all_evaluated = st.session_state['results']['all_evaluated']
        if all_evaluated:
            for eval_match in all_evaluated:
                rule = eval_match['rule']
                score = eval_match['score']
                st.markdown(f"**Evaluating Rule {rule['id']}**:")
                for cond in rule['conditions']:
                    if cond in eval_match['matched_symptoms']:
                        st.write(f"- {cond} ✓")
                    else:
                        st.write(f"- {cond} ❌")
                if score >= 50:
                    st.markdown(f"**→ {rule['id']} MATCHED ({score:.0f}%) → possible {rule['conclusion']}**")
                else:
                    st.markdown(f"**→ {rule['id']} REJECTED ({score:.0f}%)**")
                st.write("---")
        else:
            st.write("No rules could be evaluated.")
    else:
        st.write("Run a query to see inference.")

with st.expander("🧠 Agent Reasoning"):
    if 'results' in st.session_state:
        st.markdown("Step 1: Symptoms converted into facts.")
        
        st.markdown("Step 2: Facts compared against the knowledge base.")
        
        matches = st.session_state['results']['matches']
        if matches:
            top_match = matches[0]
            st.markdown(f"Step 3: Rule {top_match['rule']['id']} matched:")
            st.code(" AND ".join(top_match['rule']['conditions']))
            
            st.markdown(f"Step 4: Rule {top_match['rule']['id']} concluded:")
            st.code(f"possible {top_match['rule']['conclusion']}")
            
            st.markdown("Step 5: Matching score calculated.")
            st.markdown("Step 6: Result ranked and displayed.")
        else:
            st.markdown("Step 3: No rules strongly matched the provided facts.")
            
    else:
        st.write("No reasoning steps generated yet.")
