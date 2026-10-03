import streamlit as st
import random
import time

st.set_page_config(page_title="Stump the Bot", layout="centered")

# -----------------------------
# GAME DATA
# -----------------------------
CATEGORIES = {
    "Sports": [
        {"q": "Who won the 2020 NBA Championship?", "a": "Lakers", "points": 1},
        {"q": "Which NFL team has the most Super Bowl wins?", "a": "Steelers", "points": 3},
    ],
    "Movies": [
        {"q": "Who directed Inception?", "a": "Christopher Nolan", "points": 1},
        {"q": "Which film won Best Picture in 1994?", "a": "Forrest Gump", "points": 3},
    ],
    "History": [
        {"q": "Who was the first President of the United States?", "a": "George Washington", "points": 1},
        {"q": "In what year did World War II end?", "a": "1945", "points": 3},
    ],
    "Data & Stats": [
        {"q": "What does 'SQL' stand for?", "a": "Structured Query Language", "points": 1},
        {"q": "What is the term for data that follows a bell curve?", "a": "Normal distribution", "points": 3},
    ],
}

# Bot accuracy settings
BOT_ACCURACY = {
    1: 0.75,  # bot gets 1-point questions right 75% of the time
    3: 0.55,  # bot gets 3-point questions right 55% of the time
}

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.categories_left = list(CATEGORIES.keys())
    st.session_state.current_category = None
    st.session_state.current_question_index = 0
    st.session_state.player_score = 0
    st.session_state.bot_score = 0
    st.session_state.strikes = 0
    st.session_state.pass_used = False
    st.session_state.game_over = False
    st.session_state.message = ""

# -----------------------------
# RESET FUNCTION
# -----------------------------
def reset_game():
    st.session_state.game_started = True
    st.session_state.categories_left = list(CATEGORIES.keys())
    st.session_state.current_category = None
    st.session_state.current_question_index = 0
    st.session_state.player_score = 0
    st.session_state.bot_score = 0
    st.session_state.strikes = 0
    st.session_state.pass_used = False
    st.session_state.game_over = False
    st.session_state.message = ""

# -----------------------------
# BOT ANSWER LOGIC
# -----------------------------
def bot_answers(points):
    if random.random() < BOT_ACCURACY[points]:
        return True
    return False

# -----------------------------
# GAME OVER SCREEN
# -----------------------------
def show_game_over():
    st.error("### Game Over!")
    st.write(f"**Your Score:** {st.session_state.player_score}")
    st.write(f"**Bot Score:** {st.session_state.bot_score}")

    if st.session_state.player_score > st.session_state.bot_score:
        st.success("### You beat the Bot!")
        st.balloons()
    elif st.session_state.player_score < st.session_state.bot_score:
        st.error("### The Bot wins!")
    else:
        st.info("### It's a tie!")

    if st.button("Play Again"):
        reset_game()

# -----------------------------
# MAIN GAME UI
# -----------------------------
st.title("🧠 Stump the Bot")
st.subheader("A 1v1 trivia showdown against an AI know-it-all")

if not st.session_state.game_started:
    if st.button("Start Game"):
        reset_game()
    st.stop()

if st.session_state.game_over:
    show_game_over()
    st.stop()

# -----------------------------
# CATEGORY SELECTION
# -----------------------------
if st.session_state.current_category is None:
    st.write("### Choose a Category")

    for cat in st.session_state.categories_left:
        if st.button(cat):
            st.session_state.current_category = cat
            st.session_state.current_question_index = 0
            st.toast(f"{cat} selected!", icon="🎯")
    st.stop()

# -----------------------------
# QUESTION LOGIC
# -----------------------------
category = st.session_state.current_category
questions = CATEGORIES[category]
q_index = st.session_state.current_question_index
question = questions[q_index]

st.write(f"## Category: {category}")
st.write(f"### Question ({question['points']} pts): {question['q']}")

player_answer = st.text_input("Your Answer")

col1, col2 = st.columns(2)

with col1:
    submit = st.button("Submit Answer")

with col2:
    pass_q = st.button("Pass Question", disabled=st.session_state.pass_used)

# -----------------------------
# PASS LOGIC
# -----------------------------
if pass_q and not st.session_state.pass_used:
    st.session_state.pass_used = True
    st.toast("Pass used!", icon="🟨")

    # Bot still answers
    bot_correct = bot_answers(question["points"])
    if bot_correct:
        st.session_state.bot_score += question["points"]
        st.toast("Bot got it right!", icon="🤖")
    else:
        st.toast("Bot missed it!", icon="❌")

    # Move to next question
    st.session_state.current_question_index += 1

    if st.session_state.current_question_index >= 2:
        st.session_state.categories_left.remove(category)
        st.session_state.current_category = None

    if len(st.session_state.categories_left) == 0:
        st.session_state.game_over = True

    st.rerun()

# -----------------------------
# SUBMIT ANSWER LOGIC
# -----------------------------
if submit and player_answer.strip() != "":
    correct = player_answer.strip().lower() == question["a"].lower()

    # Player scoring
    if correct:
        st.session_state.player_score += question["points"]
        st.success("Correct!")
        st.toast(f"+{question['points']} points!", icon="🟩")
    else:
        st.session_state.strikes += 1
        st.error("Wrong!")
        st.toast("Strike added!", icon="❌")

    # Bot scoring
    bot_correct = bot_answers(question["points"])
    if bot_correct:
        st.session_state.bot_score += question["points"]
        st.toast("Bot got it right!", icon="🤖")
    else:
        st.toast("Bot missed it!", icon="❌")

    # Check strikes
    if st.session_state.strikes >= 3:
        st.session_state.game_over = True
        st.rerun()

    # Move to next question
    st.session_state.current_question_index += 1

    if st.session_state.current_question_index >= 2:
        st.session_state.categories_left.remove(category)
        st.session_state.current_category = None

    if len(st.session_state.categories_left) == 0:
        st.session_state.game_over = True

    st.rerun()

# -----------------------------
# SCOREBOARD
# -----------------------------
st.write("---")
st.write(f"### Scoreboard")
st.write(f"**You:** {st.session_state.player_score}")
st.write(f"**Bot:** {st.session_state.bot_score}")
st.write(f"**Strikes:** {st.session_state.strikes} / 3")
if st.session_state.pass_used:
    st.write("**Pass Used:** Yes")
