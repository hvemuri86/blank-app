import streamlit as st
import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv

# Load environment variables from .env file (override existing) for local development
load_dotenv(override=True)

def get_config(key, default=None):
    """Get configuration from Streamlit secrets (cloud) or environment variables (local)"""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        if key in st.secrets:
            return st.secrets[key]
    except (AttributeError, FileNotFoundError):
        # Secrets not available (local development)
        pass
    # Fall back to environment variables (for local development)
    return os.getenv(key, default)

def initialize_azure_client():
    """Initialize Azure OpenAI client"""
    try:
        client = AzureOpenAI(
            api_key=get_config("AZURE_OPENAI_API_KEY"),
            api_version=get_config("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=get_config("AZURE_OPENAI_ENDPOINT")
        )
        return client
    except Exception as e:
        st.error(f"Failed to connect to Azure OpenAI: {str(e)}")
        st.info("Please check your environment variables: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT")
        return None

def generate_mystery(client, deployment_name):
    """Generate a new mystery story using Azure OpenAI"""
    system_prompt = """You are a creative storyteller for children (Grade 4 level).
    Create a simple, kid-friendly mystery story with exactly 3 suspects.
    Return ONLY a JSON object with this exact structure:
    {
        "story": "A short mystery description (2-3 sentences, include an emoji)",
        "suspects": ["Suspect1", "Suspect2", "Suspect3"],
        "culprit": "The guilty suspect (must be one from the list)",
        "secret_details": "Private details about what really happened (for AI to give hints from)"
    }
    Keep it fun and appropriate for kids. Examples: stolen cookies, missing toys, mysterious drawings, etc."""

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate a new mystery for kids to solve."}
            ],
            temperature=0.8,
            response_format={"type": "json_object"}
        )

        mystery_data = json.loads(response.choices[0].message.content)
        return mystery_data
    except Exception as e:
        st.error(f"Error generating mystery: {str(e)}")
        return None

def get_ai_hint(client, deployment_name, mystery, question, conversation_history):
    """Get a hint from Azure OpenAI based on the question"""
    system_prompt = f"""You are a helpful detective assistant helping a Grade 4 child solve a mystery.

MYSTERY: {mystery['story']}
SUSPECTS: {', '.join(mystery['suspects'])}
THE REAL CULPRIT: {mystery['culprit']}
WHAT REALLY HAPPENED: {mystery['secret_details']}

IMPORTANT RULES:
1. Give helpful HINTS, but NEVER directly say who did it
2. Use simple language for kids (Grade 4 level)
3. Be encouraging and fun
4. If asked about the innocent suspects, give clues that point away from them
5. If asked about the real culprit, give subtle clues that point toward them
6. Keep responses short (2-3 sentences)
7. Use emojis to keep it fun
8. Don't reveal the answer even if asked directly - say "That would spoil the fun! Keep investigating!"

Previous conversation:
{conversation_history}

Respond to the child's question with a helpful hint."""

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_completion_tokens=150
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Hmm, I'm having trouble thinking right now. Try asking another question! 🤔"

def initialize_game(client, deployment_name):
    """Initialize a new game"""
    with st.spinner("🎲 Creating a new mystery..."):
        mystery = generate_mystery(client, deployment_name)
        if mystery:
            st.session_state.mystery = mystery
            st.session_state.culprit = mystery["culprit"]
            st.session_state.questions_asked = []
            st.session_state.game_over = False
            st.session_state.won = False
            st.success("✨ New mystery created! Start investigating!")
        else:
            st.error("Couldn't create a mystery. Please check your Azure OpenAI setup.")

def main():
    st.set_page_config(page_title="🔍 AI Detective Game", page_icon="🔍", layout="centered")

    # Title
    st.title("🔍 AI Detective Game")
    st.markdown("### Solve mysteries with AI-powered hints!")

    # Initialize Azure OpenAI client
    if 'client' not in st.session_state:
        st.session_state.client = initialize_azure_client()
        st.session_state.deployment_name = get_config("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

    if not st.session_state.client:
        st.warning("⚠️ Azure OpenAI is not configured. Please set up your environment variables.")
        with st.expander("📋 Setup Instructions"):
            st.code("""
# Windows (PowerShell):
$env:AZURE_OPENAI_API_KEY="your-api-key"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
$env:AZURE_OPENAI_DEPLOYMENT="your-deployment-name"

# Windows (Command Prompt):
set AZURE_OPENAI_API_KEY=your-api-key
set AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
set AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# Linux/Mac:
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
            """)
        return

    # Initialize game if needed
    if 'mystery' not in st.session_state:
        initialize_game(st.session_state.client, st.session_state.deployment_name)

    # Check if mystery was created successfully
    if 'mystery' not in st.session_state or not st.session_state.mystery:
        return

    # Show the mystery story
    st.markdown("---")
    st.markdown("## 📖 The Mystery")
    st.info(st.session_state.mystery["story"])

    # Show suspects
    st.markdown("## 🕵️ Suspects")
    suspect_cols = st.columns(len(st.session_state.mystery["suspects"]))
    for idx, suspect in enumerate(st.session_state.mystery["suspects"]):
        with suspect_cols[idx]:
            st.markdown(f"### {suspect}")
            # Add some fun emojis based on common suspect types
            if any(word in suspect.lower() for word in ["dog", "puppy"]):
                st.markdown("🐕")
            elif any(word in suspect.lower() for word in ["cat", "kitty"]):
                st.markdown("🐱")
            elif any(word in suspect.lower() for word in ["brother", "boy"]):
                st.markdown("👦")
            elif any(word in suspect.lower() for word in ["sister", "girl"]):
                st.markdown("👧")
            elif any(word in suspect.lower() for word in ["bird", "parrot"]):
                st.markdown("🦜")
            elif any(word in suspect.lower() for word in ["robot", "toy"]):
                st.markdown("🤖")
            elif any(word in suspect.lower() for word in ["fish"]):
                st.markdown("🐠")
            elif any(word in suspect.lower() for word in ["dad", "father"]):
                st.markdown("👨")
            elif any(word in suspect.lower() for word in ["mom", "mother"]):
                st.markdown("👩")
            else:
                st.markdown("❓")

    st.markdown("---")

    if not st.session_state.game_over:
        # Question section
        st.markdown("## 💭 Ask Questions")
        st.markdown("*Ask anything! The AI will give you hints!*")

        # Show previous questions and hints
        if st.session_state.questions_asked:
            with st.expander("🔍 Previous Questions & Hints", expanded=True):
                for q, h in st.session_state.questions_asked:
                    st.markdown(f"**You:** {q}")
                    st.markdown(f"**Detective AI:** {h}")
                    st.markdown("---")

        # Ask a new question
        question = st.text_input(
            "Type your question here:",
            key="question_input",
            placeholder="Example: Was the Dog near the kitchen? Did anyone see the Cat?"
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🔎 Ask", type="primary", use_container_width=True)

        if ask_button and question:
            with st.spinner("🤔 Thinking..."):
                # Build conversation history
                conv_history = "\n".join([f"Child: {q}\nAI: {h}" for q, h in st.session_state.questions_asked[-3:]])

                # Get AI hint
                hint = get_ai_hint(
                    st.session_state.client,
                    st.session_state.deployment_name,
                    st.session_state.mystery,
                    question,
                    conv_history
                )

                st.session_state.questions_asked.append((question, hint))
                st.rerun()

        st.markdown("---")

        # Guess section
        st.markdown("## 🎯 Make Your Guess")
        st.markdown("*Think you know who did it?*")

        guess = st.selectbox("Who is the culprit?", ["Choose..."] + st.session_state.mystery["suspects"])

        if st.button("✅ Submit Guess", type="primary", disabled=(guess == "Choose...")):
            st.session_state.game_over = True
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

        # Show what really happened
        with st.expander("📖 The Full Story"):
            st.markdown(st.session_state.mystery.get("secret_details", "Mystery solved!"))

        st.markdown("---")

        # Play again button
        if st.button("🔄 Play Again", type="primary"):
            initialize_game(st.session_state.client, st.session_state.deployment_name)
            st.rerun()

    # Sidebar with instructions
    with st.sidebar:
        st.markdown("## 🎮 How to Play")
        st.markdown("""
        1. **Read** the mystery story
        2. **Look** at the suspects
        3. **Ask** questions - ask anything!
        4. **Get** AI-powered hints
        5. **Guess** who did it!

        ### 💡 Tips
        - Ask about what suspects were doing
        - Ask about motives or opportunities
        - Ask about evidence or clues
        - The AI gives hints, not answers!
        - Use your detective skills!
        """)

        st.markdown("---")
        st.markdown(f"### 📊 Questions Asked: {len(st.session_state.questions_asked)}")

        st.markdown("---")
        st.markdown("### ⚙️ AI Status")
        if st.session_state.client:
            st.success("✅ Connected to Azure OpenAI")
            st.caption(f"Model: {st.session_state.deployment_name}")
        else:
            st.error("❌ Not connected")

if __name__ == "__main__":
    main()
