# 🔍 AI Detective Game (Azure OpenAI Powered)

A fun and educational detective game for kids (Grade 4 level) powered by Azure OpenAI!

## 🌟 What's Different?

This AI-powered version uses **Azure OpenAI** to:
- ✨ Generate unique mysteries every time you play
- 🤖 Respond naturally to ANY question you ask
- 💡 Give contextual, intelligent hints
- 📖 Create dynamic storylines

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd C:\Users\hvemuri\source\streamlit
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

You need an Azure OpenAI resource. Get your credentials from the Azure Portal.

#### Option A: Set Environment Variables (Recommended)

**Windows (PowerShell):**
```powershell
$env:AZURE_OPENAI_API_KEY="your-api-key"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
$env:AZURE_OPENAI_DEPLOYMENT="gpt-4"
```

**Windows (Command Prompt):**
```cmd
set AZURE_OPENAI_API_KEY=your-api-key
set AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
set AZURE_OPENAI_DEPLOYMENT=gpt-4
```

**Linux/Mac:**
```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="gpt-4"
```

#### Option B: Use .env File

1. Copy `.env.example` to `.env`
2. Fill in your Azure OpenAI credentials
3. Install python-dotenv: `pip install python-dotenv`
4. Load variables before running

### 3. Run the Game

```bash
streamlit run detective_game_ai.py
```

The game will open in your browser!

## 🎮 How to Play

1. **Read** the AI-generated mystery story
2. **Ask** any questions - the AI understands natural language!
   - "Was the dog near the kitchen?"
   - "What was the cat doing?"
   - "Did anyone see who took the cookie?"
3. **Analyze** the AI hints
4. **Make** your guess
5. **Play again** - every mystery is different!

## ✨ Features

- **🤖 AI-Powered**: Uses Azure OpenAI GPT models
- **🎲 Unique Mysteries**: Every game is different
- **💬 Natural Conversation**: Ask questions naturally
- **🧠 Smart Hints**: AI gives contextual clues without spoiling
- **👶 Kid-Friendly**: Age-appropriate language and content
- **🎨 Colorful UI**: Fun and engaging interface
- **📊 Progress Tracking**: See all your questions and hints

## 🔧 Azure OpenAI Models

Recommended models:
- **gpt-4** - Best quality, most creative mysteries
- **gpt-35-turbo** - Faster, more cost-effective

## 💰 Cost Considerations

Each game makes API calls to Azure OpenAI:
- 1 call to generate the mystery (~500 tokens)
- 1 call per question asked (~200 tokens each)

Typical game: ~1,500-2,000 tokens total

## 🆚 Versions

- **detective_game.py** - Rule-based version (no API needed)
- **detective_game_ai.py** - AI-powered version (requires Azure OpenAI)

## 🐛 Troubleshooting

**"Failed to connect to Azure OpenAI"**
- Check your API key is correct
- Verify your endpoint URL
- Ensure your deployment name matches your Azure resource

**"Rate limit exceeded"**
- Your Azure OpenAI quota may be reached
- Wait a moment and try again
- Check your Azure OpenAI usage in the portal

**"Deployment not found"**
- Verify your deployment name in Azure Portal
- Make sure the deployment is active
- Check you're using the correct resource

## 🔒 Security

- Never commit your `.env` file or API keys to version control
- Use environment variables for production
- Keep your Azure OpenAI keys secure

Have fun being a detective! 🕵️
