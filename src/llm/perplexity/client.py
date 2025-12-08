#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import Dict, List, Optional, Any
import json
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from llm.common.base_client import BaseLLMClient, RateLimiter
from config.settings import config

class PerplexityClient(BaseLLMClient):
    """Perplexity API client"""
    
    MODELS = {
        # Latest Sonar models (2025)
        "sonar": "sonar",
        "sonar-pro": "sonar-pro", 
        "sonar-reasoning": "sonar-reasoning",
        "sonar-deep-research": "sonar-deep-research",
        
        # Legacy models (may be deprecated)
        "llama-3.1-sonar-small-128k-online": "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-large-128k-online": "llama-3.1-sonar-large-128k-online", 
        "llama-3.1-sonar-huge-128k-online": "llama-3.1-sonar-huge-128k-online",
        "llama-3.1-8b-instruct": "llama-3.1-8b-instruct",
        "llama-3.1-70b-instruct": "llama-3.1-70b-instruct"
    }
    
    def __init__(self, api_key: Optional[str] = None, model: str = "sonar"):
        self.api_key = api_key or config.perplexity_api_key
        if not self.api_key:
            raise ValueError("Perplexity API key not provided")
        
        super().__init__(self.api_key, model)
        self.base_url = "https://api.perplexity.ai"
        self.rate_limiter = RateLimiter(calls_per_minute=20)  # Conservative limit
        
        # Validate model
        if model in self.MODELS:
            self.model = self.MODELS[model]
        else:
            self.model = model
    
    def send_message(self, message: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Send a single message to Perplexity"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        return self.send_messages(messages, **kwargs)
    
    def send_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send multiple messages to Perplexity"""
        self.rate_limiter.wait_if_needed()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Default parameters
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
            "max_tokens": kwargs.get("max_tokens", 1000),
            "top_p": kwargs.get("top_p", 0.9),
            "search_domain_filter": kwargs.get("search_domain_filter", ["perplexity.ai"]),
            "return_images": kwargs.get("return_images", False),
            "return_related_questions": kwargs.get("return_related_questions", False),
            "search_recency_filter": kwargs.get("search_recency_filter", "month"),
            "top_k": kwargs.get("top_k", 0),
            "stream": False,
            "presence_penalty": kwargs.get("presence_penalty", 0),
            "frequency_penalty": kwargs.get("frequency_penalty", 1)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Add to history
            for msg in messages:
                if msg["role"] != "system":
                    self.add_to_history(msg["role"], msg["content"])
            
            assistant_response = result["choices"][0]["message"]["content"]
            self.add_to_history("assistant", assistant_response)
            
            return assistant_response
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Perplexity API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def continue_conversation(self, new_message: str, **kwargs) -> str:
        """Continue existing conversation"""
        # Build messages from history
        messages = []
        for msg in self.conversation_history:
            if msg["role"] in ["user", "assistant", "system"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add new message
        messages.append({"role": "user", "content": new_message})
        
        return self.send_messages(messages, **kwargs)
    
    def search_web(self, query: str, **kwargs) -> str:
        """Use Perplexity's web search capabilities"""
        system_prompt = "You are a helpful assistant that provides accurate, up-to-date information from the web."
        
        # Extract search-specific kwargs to avoid duplicates
        search_kwargs = {
            "search_domain_filter": kwargs.pop("search_domain_filter", []),
            "search_recency_filter": kwargs.pop("search_recency_filter", "month"), 
            "return_related_questions": kwargs.pop("return_related_questions", True)
        }
        
        # Merge with remaining kwargs
        search_kwargs.update(kwargs)
        
        return self.send_message(
            query, 
            system_prompt=system_prompt,
            **search_kwargs
        ) 