import streamlit as st
import google.generativeai as genai

# ----------------------------------------------------
# Load API key from Streamlit Secrets
# ----------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Please add it in Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)

# ----------------------------------------------------
# Configure Gemini Model
# ----------------------------------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    generation_config={
        "temperature": 1.0,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 150
    }
)

def generate(prompt, max_tokens=None):
    try:
        if max_tokens is not None:
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# ----------------------------------------------------
# Title
# ----------------------------------------------------
st.title("📘 AI Storytelling - Writer View")
st.write("A Storytelling - AI Flow Writer View.")


# ----------------------------------------------------
# STEP 1: Theme
# ----------------------------------------------------
st.header("1️⃣ Select Story Theme")
theme = st.selectbox("Choose a genre:", ["Fantasy", "Science Fiction", "Mystery", "Adventure"])


# ----------------------------------------------------
# STEP 2: Characters
# ----------------------------------------------------
st.header("2️⃣ Define Main Characters")

col1, col2 = st.columns(2)

with col1:
    c1_name = st.text_input("Character 1 Name", "Aria")
    c1_personality = st.text_input("Character 1 Personality", "Brave, curious, kind-hearted")
    c1_background = st.text_area("Character 1 Background", "A young adventurer seeking ancient secrets")

with col2:
    c2_name = st.text_input("Character 2 Name", "Dr. Orion")
    c2_personality = st.text_input("Character 2 Personality", "Intelligent, secretive, analytical")
    c2_background = st.text_area("Character 2 Background", "A scientist with a mysterious past and hidden agenda")

characters = f"""
Characters:
1. {c1_name} – {c1_personality}. Background: {c1_background}
2. {c2_name} – {c2_personality}. Background: {c2_background}
"""


# ----------------------------------------------------
# STEP 3: Starting Point (User Only)
# ----------------------------------------------------
st.header("3️⃣ Begin the Story")

starting_point = st.text_area(
    "Enter the Starting Point:",
    "Aria and Dr. Orion arrive at the entrance of an ancient, mystical forest rumored to contain a legendary artifact."
)

if st.button("Save Starting Point"):
    st.session_state["start_story"] = starting_point


if "start_story" in st.session_state:
    st.subheader("Your Starting Scene")
    st.write(st.session_state["start_story"])


# ----------------------------------------------------
# STEP 4: Auto AI Question + User Action
# ----------------------------------------------------
st.header("4️⃣ Participant Input")
st.write("✔ AI automatically generates a Question\n✔ You enter the Action")

if "start_story" in st.session_state and "story_question" not in st.session_state:
    question_prompt = f"""
    Generate ONE thoughtful question asking what the characters should do next.
    Limit to 25–30 words.

    Theme: {theme}
    {characters}

    Starting Scene:
    {st.session_state['start_story']}
    """
    st.session_state["story_question"] = generate(question_prompt)


if "story_question" in st.session_state:
    st.subheader("Generated Question (AI)")
    st.write(st.session_state["story_question"])

action_input = st.text_input(
    "Enter your action:",
    "Aria examines the map while Dr. Orion looks for clues around the entrance."
)
st.session_state["participant_action"] = action_input


# ----------------------------------------------------
# STEP 5: AI Story Response
# ----------------------------------------------------
st.header("5️⃣ AI Response to Action - Continuation of story")

if st.button("Generate AI Story Response"):
    ai_prompt = f"""
    Continue the story based on this user action.
    Limit to ~120 words.

    Theme: {theme}
    {characters}

    Starting Scene:
    {st.session_state.get('start_story', '')}

    Action:
    {action_input}
    """
    st.session_state["ai_story"] = generate(ai_prompt)

if "ai_story" in st.session_state:
    st.subheader("AI Story Continuation")
    st.write(st.session_state["ai_story"])


# ----------------------------------------------------
# STEP 6: Auto AI Decision Point
# ----------------------------------------------------
st.header("6️⃣ Decision-Making & Branching Paths")
st.write("✔ AI automatically generates Decision Point\n✔ You enter the final decision")

if "ai_story" in st.session_state and "decision_question" not in st.session_state:
    decision_prompt = f"""
    Generate ONE decision-making question that creates two branching choices.
    Limit to 25–35 words.

    Theme: {theme}
    {characters}

    Previous Story:
    {st.session_state['ai_story']}
    """
    st.session_state["decision_question"] = generate(decision_prompt)

if "decision_question" in st.session_state:
    st.subheader("AI Generated Decision Point")
    st.write(st.session_state["decision_question"])

decision_taken = st.text_input("Enter your decision:", "They decide to follow the hidden path.")
st.session_state["decision_taken"] = decision_taken


# ----------------------------------------------------
# STEP 7: Refinement
# ----------------------------------------------------
st.header("7️⃣ Iteration & Refinement")
refinement_input = st.text_input(
    "Enter your refinement instruction:",
    "Adjust the character dialogue to better reflect their personalities."
)
st.session_state["refinement"] = refinement_input


# ----------------------------------------------------
# STEP 8: Conclusion
# ----------------------------------------------------
st.header("8️⃣ Conclusion")
conclusion_input = st.text_area(
    "Write your conclusion:",
    "Aria and Dr. Orion uncover the artifact and must decide whether to use its power or keep it hidden."
)
st.session_state["conclusion"] = conclusion_input


# ----------------------------------------------------
# STEP 9: Final Story
# ----------------------------------------------------
st.header("9️⃣ Final Complete Story (LLM Generated)")
st.write("This will generate a full narrative story without length limits.")

if st.button("Generate Final Story"):
    final_story_prompt = f"""
Create a polished, narrative-style adventure story using all the elements given.
Blend the starting scene, AI question, user action, AI response, decision point,
user decision, refinement, and conclusion into ONE smooth, immersive story.

Rules:
- Produce ONLY the story with headings
- Natural flow
- No word or length limit
- Use rich descriptions and dialogues
- Conclude as per given conclusion

Inputs:

Theme:
{theme}

Characters:
{characters}

Starting Scene:
{st.session_state.get('start_story', '')}

User Action:
{st.session_state.get('participant_action', '')}

AI Story Response:
{st.session_state.get('ai_story', '')}

User Decision:
{st.session_state.get('decision_taken', '')}

Refinement:
{st.session_state.get('refinement', '')}

Conclusion:
{st.session_state.get('conclusion', '')}
"""
    response = model.generate_content(
        final_story_prompt,
        generation_config={"max_output_tokens": None}
    )
    st.session_state["final_story"] = response.text

if "final_story" in st.session_state:
    st.subheader("📄 Final Complete Story")
    st.write(st.session_state["final_story"])

    st.download_button("Download Final Story (.txt)", st.session_state["final_story"], "Final_Story.txt")
