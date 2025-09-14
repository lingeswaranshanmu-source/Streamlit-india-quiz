import streamlit as st
import json
import random

# -------------------------
# Load Question Bank
# -------------------------
@st.cache_data
def load_questions():
    with open("data/questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# -------------------------
# Helper Functions
# -------------------------
def get_score(q, user_answer):
    """Compute base score for a single question."""
    type_base = {"mcq": 10, "true_false": 5, "fill_blank": 15, "matching": 20}
    difficulty_multiplier = {"easy": 1.0, "medium": 1.5, "hard": 2.0}

    base = type_base[q["type"]] * difficulty_multiplier.get(q["difficulty"], 1.0)

    correct = False
    if q["type"] in ["mcq", "true_false"]:
        correct = (user_answer == q["answer"])
    elif q["type"] == "fill_blank":
        correct = user_answer.strip().lower() in [a.lower() for a in q["answer"]]
    elif q["type"] == "matching":
        correct = all(
            user_answer.get(pair["left"]) == pair["right"] for pair in q["pairs"]
        )

    return (int(base), correct)


def reset_quiz():
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.finished = False


# -------------------------
# Session State Init
# -------------------------
if "current_q" not in st.session_state:
    reset_quiz()

# Shuffle questions for each run
if "quiz" not in st.session_state:
    st.session_state.quiz = random.sample(questions, 10)  # pick 10 random Qs

quiz = st.session_state.quiz
current_q = st.session_state.current_q

# -------------------------
# UI - Quiz Flow
# -------------------------
st.title("🇮🇳 Indian History Quiz (1900–1947)")

if not st.session_state.finished:
    q = quiz[current_q]
    st.subheader(f"Question {current_q+1} of {len(quiz)}")
    st.markdown(f"**{q['question']}**")

    user_answer = None

    if q["type"] == "mcq":
        user_answer = st.radio("Choose one:", q["options"], key=f"q{q['id']}")
    elif q["type"] == "true_false":
        user_answer = st.radio("Choose True/False:", ["True", "False"], key=f"q{q['id']}")
    elif q["type"] == "fill_blank":
        user_answer = st.text_input("Type your answer:", key=f"q{q['id']}")
    elif q["type"] == "matching":
        user_answer = {}
        for pair in q["pairs"]:
            user_answer[pair["left"]] = st.selectbox(
                f"Match for {pair['left']}",
                [pair["right"]] + [p["right"] for p in q["pairs"] if p["right"] != pair["right"]],
                key=f"q{q['id']}_{pair['left']}"
            )

    if st.button("Submit", key=f"submit{current_q}"):
        score, correct = get_score(q, user_answer)
        if correct:
            st.success(f"✅ Correct! +{score} points")
            st.session_state.score += score
        else:
            st.error("❌ Incorrect!")
        st.info(f"Explanation: {q['explanation']}")

        # Store answer
        st.session_state.answers[q["id"]] = {"answer": user_answer, "correct": correct}

        # Move to next
        if current_q + 1 < len(quiz):
            st.session_state.current_q += 1
        else:
            st.session_state.finished = True
        st.experimental_rerun()

else:
    st.success("🎉 Quiz Complete!")
    st.write(f"Your Final Score: **{st.session_state.score}** points")
    st.write(f"Accuracy: {sum(a['correct'] for a in st.session_state.answers.values())}/{len(quiz)}")

    if st.button("Restart Quiz"):
        reset_quiz()
        st.experimental_rerun()
