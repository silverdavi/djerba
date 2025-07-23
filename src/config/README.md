# Configuration Directory

This directory contains configuration files and settings for the LLM scripts.

## Files

### `.env`
Your private API keys and configuration settings. **Never commit this file to version control!**

To set up:
1. Copy `.env.example` to `.env`
2. Edit `.env` with your actual API keys
3. The file is automatically loaded by `settings.py`

### `.env.example`
Template file showing all available configuration options.

### `settings.py`
Python configuration manager that loads environment variables from multiple sources.

### `.gitignore`
Protects sensitive files from being committed to git.

## Environment Loading Priority

The configuration system loads environment variables in this order (highest to lowest priority):

1. **`src/config/.env`** - Project-specific config (highest priority)
2. **Project root `.env`** - Alternative location
3. **`~/.djerba.env`** - User home directory config
4. **System environment variables** - OS-level variables

## Available Configuration

### Required API Keys
```bash
OPENAI_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here  
ANTHROPIC_API_KEY=your_key_here
```

### Optional Settings
```bash
# Default models
DEFAULT_OPENAI_MODEL=gpt-4.1-mini
DEFAULT_PERPLEXITY_MODEL=sonar

# Rate limiting
OPENAI_RATE_LIMIT=50
PERPLEXITY_RATE_LIMIT=20

# Debug mode
DEBUG=true
```

## Security

- ✅ `.env` files are ignored by git
- ✅ Multiple secure storage locations supported
- ✅ No default values for API keys in code
- ✅ Clear separation between example and actual config

## Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Perplexity**: https://www.perplexity.ai/settings/api  
- **Anthropic**: https://console.anthropic.com/ 