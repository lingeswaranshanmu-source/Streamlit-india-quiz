import streamlit as st
import json
import random
import time
import os
from datetime import datetime

# -------------------------
# Load Question Bank
# -------------------------
@st.cache_data
def load_questions():
    with open("data/questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# -------------------------
# Leaderboard functions
# -------------------------
LEADERBOARD_FILE = "data/leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_leaderboard(entries):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

def add_to_leaderboard(username, mode, score, correct_count, total_q, duration):
    entries = load_leaderboard()
    entries.append({
        "username": username,
        "mode": mode,
        "score": score,
        "correct_count": correct_count,
        "questions_count": total_q,
        "duration_seconds": duration,
        "created_at": datetime.utcnow().isoformat()
    })
    save_leaderboard(entries)

# -------------------------
# Scoring helpers
# -------------------------
def compute_score(q, user_answer, time_taken, streak):
    type_base = {"mcq": 10, "true_false": 5, "fill_blank": 15, "matching": 20}
    difficulty_multiplier = {"easy": 1.0, "medium": 1.5, "hard": 2.0}
    time_limit = 30
    time_bonus_cap = type_base[q["type"]] * 0.5
    streak_bonus_unit = 2

    base = type_base[q["type"]] * difficulty_multiplier[q["difficulty"]]

    correct = False
    if q["type"] in ["mcq", "true_false"]:
        correct = (user_answer == q["answer"])
    elif q["type"] == "fill_blank":
        correct = user_answer.strip().lower() in [a.lower() for a in q["answer"]]
    elif q["type"] == "matching":
        correct = all(
            user_answer.get(pair["left"]) == pair["right"] for pair in q["pairs"]
        )

    if not correct:
        return 0, False

    time_bonus = round((max(0, time_limit - time_taken) / time_limit) * time_bonus_cap)
    streak_bonus = round(streak_bonus_unit * (streak - 1) * difficulty_multiplier[q["difficulty"]])
    total = round(base + time_bonus + streak_bonus)

    return total, True


def reset_quiz(mode="fixed"):
    st.session_state.mode = mode
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.finished = False
    st.session_state.streak = 0
    st.session_state.start_time = time.time()
    # ✅ Shuffle once and store, no duplicates
    st.session_state.quiz = random.sample(questions, min(10, len(questions)))
    st.session_state.show_feedback = False


# -------------------------
# Session Init
# -------------------------
if "current_q" not in st.session_state:
    reset_quiz()

quiz = st.session_state.quiz
current_q = st.session_state.current_q

# -------------------------
# UI
# -------------------------
st.title("🇮🇳 Indian History Quiz (1900–1947)")

# Mode selector at top (only at first Q)
if current_q == 0 and not st.session_state.finished:
    st.sidebar.header("Choose Quiz Mode")
    mode = st.sidebar.radio("Mode:", ["Fixed (10Q)", "Timed (5 min)"])
    st.session_state.mode = "fixed" if mode.startswith("Fixed") else "timed"

# Progress bar
st.progress((current_q) / len(quiz))

if not st.session_state.finished:
    q = quiz[current_q]
    st.subheader(f"Question {current_q+1} of {len(quiz)}")
    st.markdown(f"**{q['question']}**")

    # Disable inputs once feedback is being shown
    is_locked = st.session_state.show_feedback

    user_answer = None
    if q["type"] == "mcq":
        user_answer = st.radio(
            "Choose one:",
            q["options"],
            index=None,
            key=f"q{q['id']}_{current_q}",
            disabled=is_locked
        )
    elif q["type"] == "true_false":
        user_answer = st.radio(
            "Choose True/False:",
            ["True", "False"],
            index=None,
            key=f"q{q['id']}_{current_q}",
            disabled=is_locked
        )
    elif q["type"] == "fill_blank":
        user_answer = st.text_input(
            "Type your answer:",
            key=f"q{q['id']}_{current_q}",
            disabled=is_locked
        )
    elif q["type"] == "matching":
        user_answer = {}
        for pair in q["pairs"]:
            user_answer[pair["left"]] = st.selectbox(
                f"Match for {pair['left']}",
                [pair["right"]] + [p["right"] for p in q["pairs"] if p["right"] != pair["right"]],
                key=f"q{q['id']}_{current_q}_{pair['left']}",
                disabled=is_locked
            )

    # Submit button
    disable_submit = (
        (q["type"] in ["mcq", "true_false"] and user_answer is None) or
        (q["type"] == "fill_blank" and not user_answer.strip()) or
        (q["type"] == "matching" and not all(user_answer.values()))
    )

    if not st.session_state.show_feedback:
        if st.button("Submit", key=f"submit{current_q}", disabled=disable_submit):
            time_taken = time.time() - st.session_state.get(f"q_start_{q['id']}", time.time())
            score, correct = compute_score(q, user_answer, time_taken, st.session_state.streak + 1)

            if correct:
                st.success(f"✅ Correct! +{score} points")
                st.session_state.score += score
                st.session_state.streak += 1
            else:
                st.error("❌ Incorrect! +0 points")
                st.session_state.streak = 0

            st.info(f"Explanation: {q['explanation']}")

            # Save answer + points
            st.session_state.answers[q["id"]] = {
                "answer": user_answer,
                "correct": correct,
                "points": score
            }

            st.session_state.show_feedback = True
            st.rerun()
    else:
        # Show feedback screen with "Next" button
        last_answer = st.session_state.answers[q["id"]]
        if last_answer["correct"]:
            st.success(f"✅ Correct! +{last_answer['points']} points")
        else:
            st.error("❌ Incorrect! +0 points")
        st.info(f"Explanation: {q['explanation']}")

        if st.button("Next Question"):
            st.session_state.show_feedback = False
            if current_q + 1 < len(quiz):
                st.session_state.current_q += 1
            else:
                st.session_state.finished = True
            st.rerun()

else:
    st.success("🎉 Quiz Complete!")
    total_correct = sum(a['correct'] for a in st.session_state.answers.values())
    duration = int(time.time() - st.session_state.start_time)

    st.write(f"Your Final Score: **{st.session_state.score}** points")
    st.write(f"Accuracy: {total_correct}/{len(quiz)}")
    st.write(f"Total Time: {duration} seconds")

    # Ask for username & save to leaderboard
    username = st.text_input("Enter your username to submit to leaderboard:")
    if st.button("Submit to Leaderboard") and username.strip():
        add_to_leaderboard(
            username=username.strip(),
            mode=st.session_state.mode,
            score=st.session_state.score,
            correct_count=total_correct,
            total_q=len(quiz),
            duration=duration
        )
        st.success("✅ Score submitted to leaderboard!")

    # Show leaderboard
    st.subheader("🏆 Leaderboard (Top 10)")
    leaderboard = sorted(load_leaderboard(), key=lambda x: x["score"], reverse=True)[:10]
    if leaderboard:
        for i, entry in enumerate(leaderboard, 1):
            st.write(
                f"{i}. {entry['username']} — {entry['score']} pts "
                f"({entry['correct_count']}/{entry['questions_count']} correct, {entry['mode']})"
            )
    else:
        st.info("No entries yet. Be the first!")

    if st.button("Restart Quiz"):
        reset_quiz()
        st.rerun()
