# MyNoCompany AI Project

> Multi-agent AI system using Microsoft AutoGen for collaborative scenario simulations.

## Features

- **Novel Writing Mode** - AI agents debate and develop story plots
- **Website Sales Pitch Mode** - Simulate student presentations to local businesses
- **Infinite Fallback** - Automatic model rotation when quotas hit
- **Dual Logging** - Colored terminal output + clean file logs

## Quick Start

```bash
# Activate virtual environment
.\venv\Scripts\python.exe Studio.py
```

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file:
```env
GOOGLE_API_KEY_1=your_key_here
GOOGLE_API_KEY_2=your_key_here
GOOGLE_API_KEY_3=your_key_here
GOOGLE_API_KEY_4=your_key_here
```

Get API keys from: https://aistudio.google.com/app/apikey

## Project Structure

```
├── Studio.py      # Main entry point
├── Config.py      # API keys, model config, utilities
├── Agents.py      # Agent definitions
├── .env           # API keys (gitignored)
└── AboutCheck/    # Debug scripts
```

## Modes

### Novel Writing Mode
Originally for collaborative story development with 4 AI agents.

### Website Sales Pitch Mode
Simulate students pitching website services to bubble tea shop owners.

---

## Configuration

### Models (Config.py)
Edit `MODEL_PRIORITY_LIST` to change model preference order.

### Agent Personalities (Agents.py)
Modify `system_message` for each agent to customize behavior.

### Temperature Settings (Config.py)
- `config_research` - Low creativity (0.3)
- `config_editor` - Balanced (0.7)
- `config_writer` - High creativity (0.9)

## Troubleshooting

**Program stuck at "Cooling down..."?**
- Normal - waiting for quota reset
- Press Ctrl+C to exit

**Need to add more API keys?**
- Add more to `.env` as `GOOGLE_API_KEY_5`, etc.

---

## License

MIT
