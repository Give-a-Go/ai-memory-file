# File Memory Travel Assistant

A Python-based travel assistant application that uses Google's Agent Development Kit (ADK) to provide personalized travel recommendations. The assistant remembers user preferences and can help with flight searches.

## Features

- 🤖 AI-powered travel assistant using Google Gemini
- 💾 Persistent memory system for user preferences
- ✈️ Flight search functionality with preference matching
- 💬 Interactive chat interface
- 🔄 Session management

## Requirements

- Python 3.10 or higher
- Google API Key (for Gemini AI)

## Setup Instructions

Choose one of the following setup methods:

### Option 1: Setup with uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver. It's recommended for its speed and reliability.

#### 1. Install uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

#### 2. Create and activate a virtual environment

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### 3. Install dependencies

```bash
# Install project dependencies
uv pip install -e .
```

#### 4. Setup environment variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Google API key to the `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

#### 5. Run the application

```bash
python main.py
```

### Option 2: Setup with pip (Traditional)

#### 1. Create and activate a virtual environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### 2. Install dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install project dependencies
pip install -e .

# Or install dependencies directly:
pip install "google-adk>=1.5.0" "python-dotenv>=1.0.0"
```

#### 3. Setup environment variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Google API key to the `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

#### 4. Run the application

```bash
python main.py
```

## Getting a Google API Key

1. Go to the [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API key" or "Create API key"
4. Follow the instructions to create a new API key
5. Copy the API key and add it to your `.env` file

## Environment Variables

The application requires the following environment variable:

- `GOOGLE_API_KEY`: Your Google API key for accessing Gemini AI services

## Usage

1. Make sure your virtual environment is activated
2. Ensure your `.env` file contains your Google API key
3. Run the application: `python main.py`
4. Start chatting with the travel assistant!
5. Type 'quit' or 'exit' to end the session

### Example Conversation

```
> Hi
<<< Assistant: Hello! I'm your friendly travel assistant. I'm here to help make booking your travel as easy as possible by remembering your preferences. How can I assist with your travel plans today?

> I want to fly to Tokyo next week
<<< Assistant: That sounds exciting! I'd be happy to help you find flights to Tokyo for next week. Let me check if I have any of your travel preferences saved and then search for available flights...
```

## Project Structure

```
.
├── README.md                 # This file
├── main.py                   # Main application file
├── pyproject.toml           # Project configuration and dependencies
├── .env                     # Environment variables (create this)
├── .venv/                   # Virtual environment (created during setup)
└── travel_agent_memory.json # Memory storage file (created automatically)
```

## Features Overview

- **Memory System**: The assistant remembers your travel preferences across sessions
- **Flight Search**: Mock flight search functionality that considers your preferences
- **Interactive Chat**: Natural language conversation interface
- **Preference Learning**: The assistant learns and saves your airline preferences

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not set" error**

   - Make sure you've created a `.env` file in the project root
   - Verify your API key is correctly added to the `.env` file
   - Ensure there are no extra spaces or quotes around the API key

2. **Import errors**

   - Make sure your virtual environment is activated
   - Verify all dependencies are installed with `pip list` or `uv pip list`

3. **Python version issues**
   - This project requires Python 3.10 or higher
   - Check your Python version: `python --version`

### Virtual Environment Commands

```bash
# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Check if virtual environment is active
which python  # Should show path to .venv/bin/python
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a virtual environment using either uv or pip method above
3. Install dependencies in development mode: `pip install -e .`
4. Make your changes
5. Test your changes by running the application
6. Submit a pull request
