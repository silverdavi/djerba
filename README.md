# RecipeDjerba Python Environment

This repository contains a Python virtual environment with essential AI and data science libraries.

## Installed Packages

- **pandas**: Data manipulation and analysis library
- **openai**: Official OpenAI Python client
- **google-generativeai**: Google's Gemini AI Python client
- **PerplexiPy**: Perplexity AI Python client

## Setup Instructions

### Activate the Virtual Environment

```bash
source venv/bin/activate
```

### Install from Requirements (Alternative Setup)

If you need to recreate this environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage Examples

### Using Pandas
```python
import pandas as pd

# Create a simple DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df)
```

### Using OpenAI
```python
import openai

# Set your API key
client = openai.OpenAI(api_key="your-api-key-here")

# Make a chat completion request
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Using Google Generative AI (Gemini)
```python
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="your-api-key-here")

# Use Gemini model
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Hello!")
print(response.text)
```

### Using Perplexity AI
```python
from perplexipy import PerplexityClient

# Set up client with API key
client = PerplexityClient(api_key="your-api-key-here")

# Make a query
result = client.query("What is machine learning?")
print(result)
```

## API Keys Setup

You'll need to set up API keys for the AI services:

1. **OpenAI GPT-4o-mini**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Google Gemini 2.5**: Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. **Perplexity Sonar Pro**: Get your API key from [Perplexity API](https://docs.perplexity.ai/guides/getting-started)

### Environment Variables Setup

1. Copy the template file `env_template.txt` to create your `.env` file:

```bash
cp env_template.txt .env
```

2. Edit the `.env` file and replace the placeholder values with your actual API keys:

```bash
# API Keys for AI Services
OPENAI_API_KEY=your_actual_openai_key_here
GOOGLE_API_KEY=your_actual_google_key_here  
PERPLEXITY_API_KEY=your_actual_perplexity_key_here
```

3. **Important**: Never commit your `.env` file to version control!

### Testing Your API Keys

Run the included test script to verify all your API keys are working:

```bash
source venv/bin/activate
python test_api_keys.py
```

The script will test:
- **OpenAI GPT-4o-mini**: Latest efficient model from OpenAI
- **Google Gemini 2.5 Flash**: Google's latest multimodal model  
- **Perplexity Sonar Pro**: Search-enhanced AI with real-time information

### Loading API Keys in Python Code

```python
import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')
google_key = os.getenv('GOOGLE_API_KEY')
perplexity_key = os.getenv('PERPLEXITY_API_KEY')
```

## Deactivate Virtual Environment

When you're done working:

```bash
deactivate
```

## Testing Script

The repository includes a comprehensive API testing script (`test_api_keys.py`) that:

- ✅ Tests all AI services with real API calls (GPT-4o-mini, Gemini 2.5, Perplexity Sonar Pro)
- 🎨 Tests DALL-E 3 image generation and saves generated images locally
- ⏱️ Measures response times for all services
- 🔍 Validates API key authentication
- 📊 Provides detailed success/failure reporting
- 💡 Offers troubleshooting tips for common issues

### Running the Tests

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Create .env file from template
cp env_template.txt .env

# Edit .env file with your actual API keys
# Then run the test script
python test_api_keys.py
```

## Files in this Repository

- `README.md` - This documentation file
- `requirements.txt` - Python package dependencies
- `env_template.txt` - Template for environment variables
- `test_api_keys.py` - Comprehensive API testing script
- `venv/` - Python virtual environment directory

## Notes

- The virtual environment is located in the `venv/` directory
- All dependencies are listed in `requirements.txt`
- Python version: 3.11+ (recommended)
- Keep your `.env` file private and never commit it to version control 