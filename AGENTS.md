# AGENTS.md - AI Agent Guidelines for This Project

## Project Overview

**MyNoCompany AI Novel Studio** - A multi-agent AI system using Microsoft AutoGen for collaborative scenario simulations (originally novel writing, now also website sales pitch scenarios).

- **Language:** Python 3.12
- **Framework:** Microsoft AutoGen (pyautogen)
- **AI Models:** Google Gemini API (via google-generativeai)
- **Key Dependencies:** FLAML, google-cloud-aiplatform, vertexai

---

## Build & Run Commands

### Run the Application
```bash
# Activate virtual environment first
.\venv\Scripts\python.exe Studio.py

# Or with virtual env activated
python Studio.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Setup
1. Copy `.env.example` to `.env` (if exists) or create `.env`
2. Add your Google API keys:
   ```
   GOOGLE_API_KEY_1=your_key_here
   GOOGLE_API_KEY_2=your_key_here
   ```
3. API keys are loaded via `python-dotenv` in `Config.py`

---

## Code Style Guidelines

### Imports
- Standard library imports first
- Third-party imports second
- Local imports last
- Group by category with blank lines between groups
- Use explicit relative imports for local modules

```python
# Good
import sys
import re
import time
import os

from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions

import Config
import Agents
```

### Formatting
- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)
- Use blank lines sparingly to separate logical sections
- Remove trailing whitespace

### Naming Conventions
- **Variables:** `snake_case` (e.g., `config_list`, `api_keys`)
- **Functions:** `snake_case` (e.g., `get_fallback_config_list`)
- **Classes:** `PascalCase` (e.g., `UserProxyAgent`, `Logger`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MODEL_PRIORITY_LIST`)
- **Private functions:** prefix with `_` (e.g., `_retry_on_quota_error`)

### Type Hints
- Use type hints for function parameters and return values
- Use `typing` module for complex types

```python
def get_fallback_config_list() -> list[dict]:
    ...
```

### Docstrings
- Use triple quotes `"""..."""`
- Include brief description on first line
- Add more details after blank line if needed

```python
def load_company_memory() -> str:
    """Load past project history from database file."""
    ...
```

### Error Handling
- Use specific exception types
- Let exceptions propagate when appropriate
- Use try/except for expected failures with graceful degradation
- Log errors before re-raising

```python
try:
    return _original_generate_content(self, *args, **kwargs)
except exceptions.ResourceExhausted as e:
    # Handle quota error with fallback logic
    raise e
```

### Language
- Code comments: English or Thai (match project language)
- User-facing messages: Thai (based on project context)
- Variable/function names: English

---

## File Structure

```
MyNoCompanyTryMakeAIAgent/
├── Studio.py          # Main entry point
├── Config.py          # API keys, model config, utilities
├── Agents.py          # Agent definitions
├── .env               # API keys (DO NOT COMMIT)
├── requirements.txt   # Dependencies
├── .gitignore         # Git exclusions
├── AGENTS.md          # This file
└── AboutCheck/        # Debug/testing scripts
```

---

## Important Patterns

### AutoGen Agent Configuration
- Use `llm_config` from `Config.py` for consistent model settings
- Configure `human_input_mode` appropriately:
  - `NEVER` for automated agents
  - `ALWAYS` for user proxy agents requiring input
- Set `max_consecutive_auto_reply` to prevent infinite loops

### API Key Management
- Store in `.env` file (already in `.gitignore`)
- Load with `load_dotenv()` from python-dotenv
- Access via `os.getenv()` in `Config.py`

### Logging System
- Uses custom `Logger` class in `Config.py`
- Terminal output: colored
- File output (`meeting_log.txt`): clean text (ANSI codes stripped)

---

## Testing

Currently no formal test suite exists. For debugging:
- Check `AboutCheck/` directory for manual test scripts
- Run individual files directly: `python AboutCheck/DebugEnv.py`

---

## Security Notes

- **NEVER commit API keys** - Keep in `.env` which is gitignored
- **NEVER commit secrets** to GitHub
- Review `Config.py` before sharing code

---

## Notes for AI Agents

1. This project uses monkey patching in `Config.py` to handle API quotas - be careful when modifying `genai.GenerativeModel.generate_content`
2. The fallback system rotates through multiple models and API keys - understand this before making changes
3. Thai language is used throughout the user-facing output
4. Files use UTF-8 encoding (required for Thai characters)
