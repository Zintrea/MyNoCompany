# MyNoCompany AI Project

> Multi-agent AI system using Microsoft AutoGen for collaborative scenario simulations.

## Features

- **Novel Writing Mode** - AI agents debate and develop story plots
- **Website Sales Pitch Mode** - Simulate student presentations to local businesses
- **Infinite Fallback** - Automatic model rotation when quotas hit
- **Dual Logging** - Colored terminal output + clean file logs

## Quick Start

```bash
.\venv\Scripts\python.exe Studio.py
```

---

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add API Keys

**File location:** `.env` (in project root)

**How to edit:**
1. Open Notepad
2. Open file: `C:\Host\03 Projects\03 AIAgent\MyNoCompanyTryMakeAIAgent\.env`
3. Replace `YOUR_API_KEY_HERE` with your real keys

**Get keys from:** https://platform.deepseek.com/

**Format:**
```env
DEEPSEEK_API_KEY_1=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_KEY_2=sk-yyyyyyyyyyyyyyyyyyyyyy
DEEPSEEK_API_KEY_3=sk-zzzzzzzzzzzzzzzzzzzzzz
DEEPSEEK_API_KEY_4=sk-aaaaaaaaaaaaaaaaaaaaa
```

You need at least 1 API key. Add more keys (up to 9) for better reliability.

---

## Run the Program

```bash
.\venv\Scripts\python.exe Studio.py
```

Follow the prompts:
1. Enter shop name (for sales pitch mode)
2. Enter shop location
3. Watch the AI agents interact
4. At the end, choose to save or discard the conversation

---

## Project Structure

```
├── Studio.py      # Main entry point
├── Config.py      # API keys, model config, utilities
├── Agents.py      # Agent definitions
├── .env           # API keys (DO NOT COMMIT)
├── README.md     # This file
└── AboutCheck/   # Debug scripts
```

---

## Configuration

### Models (Config.py)
Edit `MODEL_PRIORITY_LIST` to change model preference order.

Current models:
- `deepseek-chat` - General conversation
- `deepseek-coder` - Code-focused tasks

### Agent Personalities (Agents.py)
Modify `system_message` for each agent to customize behavior.

### Temperature Settings (Config.py)
- `config_research` - Low creativity (0.3)
- `config_editor` - Balanced (0.7)
- `config_writer` - High creativity (0.9)

---

## Troubleshooting

**"No module named 'autogen'"**
```bash
pip install pyautogen
```

**API Error**
- Your DeepSeek API key is invalid or missing
- Edit `.env` file and add real API keys

**Program stuck**
- Press Ctrl+C to exit

**UnicodeEncodeError**
- This is a Windows console issue, already fixed in code

---

## License

MIT
