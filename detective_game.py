import streamlit as st
import random

# Mystery scenarios
MYSTERIES = [
    {
        "story": "🍪 Someone stole the last chocolate chip cookie from the cookie jar! It was sitting on the kitchen counter this morning, but now it's gone. There are crumbs leading to the living room.",
        "suspects": ["Dog", "Cat", "Brother"],
        "culprit": "Brother",
        "clues": {
            "Dog": ["The dog was sleeping in the backyard all morning", "The dog doesn't like chocolate", "The dog can't reach the counter"],
            "Cat": ["The cat was playing with toys in the bedroom", "The cat prefers milk over cookies", "The cat is too small to climb the counter"],
            "Brother": ["Your brother was watching TV in the living room", "Your brother loves chocolate chip cookies", "Your brother was near the kitchen earlier"]
        }
    },
    {
        "story": "🎨 Someone drew funny pictures all over the living room wall with colorful markers! Mom is going to be upset. The drawings include stars, hearts, and smiley faces.",
        "suspects": ["Little Sister", "Parrot", "Robot Toy"],
        "culprit": "Little Sister",
        "clues": {
            "Little Sister": ["Your sister has marker stains on her hands", "Your sister was in the living room alone", "Your sister loves drawing stars and hearts"],
            "Parrot": ["The parrot was in its cage all day", "Parrots can't hold markers", "The parrot only knows how to squawk"],
            "Robot Toy": ["The robot toy has no hands to hold markers", "The robot toy was turned off", "Toys can't draw by themselves"]
        }
    },
    {
        "story": "🧸 Someone hid all the teddy bears in the house! They were on the shelf yesterday, but now they're missing. You heard giggling sounds earlier.",
        "suspects": ["Cousin", "Goldfish", "Dad"],
        "culprit": "Cousin",
        "clues": {
            "Cousin": ["Your cousin was playing hide and seek earlier", "Your cousin was laughing in the closet", "Your cousin loves playing pranks"],
            "Goldfish": ["The goldfish is in its tank and can't leave the water", "Fish don't have hands to move things", "The goldfish has been swimming all day"],
            "Dad": ["Dad was at work all morning", "Dad is too busy to play pranks", "Dad didn't hear any giggling"]
        }
    }
]

def initialize_game():
    """Initialize a new game"""
    mystery = random.choice(MYSTERIES)
    st.session_state.mystery = mystery
    st.session_state.culprit = mystery["culprit"]
    st.session_state.questions_asked = []
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.guess_made = False

def get_hint(suspect):
    """Get a hint about a suspect"""
    mystery = st.session_state.mystery
    clues = mystery["clues"][suspect]

    # Return a clue based on how many questions were asked about this suspect
    asked_about_suspect = [q for q in st.session_state.questions_asked if suspect.lower() in q.lower()]
    clue_index = len(asked_about_suspect) % len(clues)

    return clues[clue_index]

def main():
    st.set_page_config(page_title="🔍 Kid Detective Game", page_icon="🔍", layout="centered")

    # Initialize game if needed
    if 'mystery' not in st.session_state:
        initialize_game()

    # Title
    st.title("🔍 Kid Detective Game")
    st.markdown("### Solve the mystery by asking questions!")

    # Show the mystery story
    st.markdown("---")
    st.markdown("## 📖 The Mystery")
    st.info(st.session_state.mystery["story"])

    # Show suspects
    st.markdown("## 🕵️ Suspects")
    cols = st.columns(len(st.session_state.mystery["suspects"]))
    for idx, suspect in enumerate(st.session_state.mystery["suspects"]):
        with cols[idx]:
            st.markdown(f"### {suspect}")
            if suspect == "Dog":
                st.markdown("🐕")
            elif suspect == "Cat":
                st.markdown("🐱")
            elif suspect == "Brother":
                st.markdown("👦")
            elif suspect == "Little Sister":
                st.markdown("👧")
            elif suspect == "Parrot":
                st.markdown("🦜")
            elif suspect == "Robot Toy":
                st.markdown("🤖")
            elif suspect == "Cousin":
                st.markdown("🧒")
            elif suspect == "Goldfish":
                st.markdown("🐠")
            elif suspect == "Dad":
                st.markdown("👨")

    st.markdown("---")

    if not st.session_state.game_over:
        # Question section
        st.markdown("## 💭 Ask Questions")
        st.markdown("*Ask about the suspects to get hints!*")

        # Show previous questions and hints
        if st.session_state.questions_asked:
            with st.expander("🔍 Previous Questions & Hints", expanded=True):
                for q, h in st.session_state.questions_asked:
                    st.markdown(f"**You:** {q}")
                    st.markdown(f"**Detective AI:** {h}")
                    st.markdown("---")

        # Ask a new question
        question = st.text_input("Type your question here:", key="question_input", placeholder="Example: Was it the dog?")

        if st.button("🔎 Ask Question", type="primary"):
            if question:
                # Find which suspect the question is about
                hint = None
                for suspect in st.session_state.mystery["suspects"]:
                    if suspect.lower() in question.lower():
                        hint = get_hint(suspect)
                        break

                if hint:
                    st.session_state.questions_asked.append((question, hint))
                    st.rerun()
                else:
                    st.warning("🤔 Please ask about one of the suspects!")

        st.markdown("---")

        # Guess section
        st.markdown("## 🎯 Make Your Guess")
        st.markdown("*Think you know who did it?*")

        guess = st.selectbox("Who is the culprit?", ["Choose..."] + st.session_state.mystery["suspects"])

        if st.button("✅ Submit Guess", type="primary", disabled=(guess == "Choose...")):
            st.session_state.game_over = True
            st.session_state.guess_made = True
            if guess == st.session_state.culprit:
                st.session_state.won = True
            else:
                st.session_state.won = False
            st.rerun()

    else:
        # Game over - show results
        st.markdown("---")
        if st.session_state.won:
            st.balloons()
            st.success(f"## 🎉 Congratulations! You solved it!")
            st.markdown(f"### **{st.session_state.culprit}** was the culprit!")
            st.markdown("You're an amazing detective! 🕵️")
        else:
            st.error(f"## ❌ Oh no! That wasn't correct!")
            st.markdown(f"### The real culprit was **{st.session_state.culprit}**!")
            st.markdown("Don't worry, try again! 💪")

        st.markdown("---")

        # Play again button
        if st.button("🔄 Play Again", type="primary"):
            initialize_game()
            st.rerun()

    # Sidebar with instructions
    with st.sidebar:
        st.markdown("## 🎮 How to Play")
        st.markdown("""
        1. **Read** the mystery story
        2. **Look** at the suspects
        3. **Ask** questions about the suspects
        4. **Get** hints from the Detective AI
        5. **Guess** who did it!

        ### 💡 Tips
        - Ask about each suspect
        - Look for clues in the hints
        - The AI won't tell you directly!
        - Use your detective skills!
        """)

        st.markdown("---")
        st.markdown(f"### 📊 Questions Asked: {len(st.session_state.questions_asked)}")

if __name__ == "__main__":
    main()
