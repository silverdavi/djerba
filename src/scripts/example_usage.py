#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example script showing how to use the LLM clients
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from llm.openai.client import OpenAIClient
from llm.perplexity.client import PerplexityClient
from config.settings import config
from utils.text_processing import clean_text, count_tokens, is_hebrew

def test_openai():
    """Test OpenAI client"""
    print("Testing OpenAI client...")
    
    try:
        client = OpenAIClient(model="gpt-4.1-mini")
        
        # Simple question
        response = client.send_message(
            "What are the key ingredients in Middle Eastern cuisine?",
            temperature=0.7
        )
        print(f"OpenAI Response: {response[:200]}...")
        
        # Continue conversation
        follow_up = client.continue_conversation(
            "Can you give me a recipe using those ingredients?"
        )
        print(f"Follow-up Response: {follow_up[:200]}...")
        
        # Show conversation summary
        summary = client.get_conversation_summary()
        print(f"Conversation Summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"OpenAI test failed: {e}")
        return False

def test_perplexity():
    """Test Perplexity client"""
    print("\nTesting Perplexity client...")
    
    try:
        client = PerplexityClient()
        
        # Web search question
        response = client.search_web(
            "What are the latest trends in Middle Eastern cooking in 2024?",
            search_recency_filter="month"
        )
        print(f"Perplexity Response: {response[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"Perplexity test failed: {e}")
        return False

def test_recipe_processing():
    """Test processing Hebrew recipes"""
    print("\nTesting recipe processing...")
    
    # Sample Hebrew recipe text
    sample_text = """
    שם המתכון: חומוס
    רשימת מצרכים:
    חומוס יבש
    טחינה
    שום
    מיץ לימון
    אופן ההכנה:
    לשרות את החומוס במים
    לבשל עד שמתרכך
    להוסיף טחינה ותבלינים
    """
    
    cleaned = clean_text(sample_text)
    print(f"Cleaned text: {cleaned}")
    
    print(f"Is Hebrew: {is_hebrew(sample_text)}")
    print(f"Token count: {count_tokens(sample_text)}")

def main():
    """Main function"""
    print("LLM Client Examples")
    print("=" * 50)
    
    # Check API keys
    validation = config.validate_api_keys()
    print(f"API Key Status: {validation}")
    
    if not validation['valid']:
        print("Warning: Some API keys are missing. Set environment variables:")
        for provider in validation['missing']:
            print(f"  export {provider.upper()}_API_KEY='your_key_here'")
        print()
    
    # Test available clients
    if "openai" in validation['available']:
        test_openai()
    else:
        print("Skipping OpenAI test - API key not available")
    
    if "perplexity" in validation['available']:
        test_perplexity()
    else:
        print("Skipping Perplexity test - API key not available")
    
    # Test text processing (always available)
    test_recipe_processing()

if __name__ == "__main__":
    main() 