#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
from typing import Dict, List, Optional, Any
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from llm.common.base_client import BaseLLMClient, RateLimiter
from config.settings import config

class OpenAIClient(BaseLLMClient):
    """OpenAI API client"""
    
    MODELS = {
        # Latest GPT-4.1 family (April 2025)
        "gpt-4.1": "gpt-4.1",
        "gpt-4.1-mini": "gpt-4.1-mini", 
        "gpt-4.1-nano": "gpt-4.1-nano",
        
        # o-series reasoning models
        "o3": "o3",
        "o3-mini": "o3-mini", 
        "o3-pro": "o3-pro",
        "o4-mini": "o4-mini",
        "o1": "o1",
        "o1-mini": "o1-mini",
        
        # GPT-4 family
        "gpt-4": "gpt-4",
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4.5": "gpt-4.5-preview",
        
        # GPT-3.5 family  
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-3.5": "gpt-3.5-turbo"
    }
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4.1"):
        self.api_key = api_key or config.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        super().__init__(self.api_key, model)
        self.client = openai.OpenAI(api_key=self.api_key)
        self.rate_limiter = RateLimiter(calls_per_minute=50)  # Conservative limit
        
        # Validate model
        if model in self.MODELS:
            self.model = self.MODELS[model]
        else:
            self.model = model
    
    def send_message(self, message: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Send a single message to OpenAI"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        return self.send_messages(messages, **kwargs)
    
    def send_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send multiple messages to OpenAI"""
        self.rate_limiter.wait_if_needed()
        
        # Default parameters - handle o3 models differently
        params = {
            "model": self.model,
            "messages": messages,
        }
        
        # o3 models are very restrictive - only support basic parameters
        if "o3" in self.model or "o4" in self.model:
            params["max_completion_tokens"] = kwargs.get("max_completion_tokens", kwargs.get("max_tokens", 1000))
            # o3 models don't support temperature, top_p, etc.
        else:
            params["temperature"] = kwargs.get("temperature", 0.7)
            params["max_tokens"] = kwargs.get("max_tokens", 1000)
        
        # Add optional parameters
        if "top_p" in kwargs:
            params["top_p"] = kwargs["top_p"]
        if "frequency_penalty" in kwargs:
            params["frequency_penalty"] = kwargs["frequency_penalty"]
        if "presence_penalty" in kwargs:
            params["presence_penalty"] = kwargs["presence_penalty"]
        
        try:
            response = self.client.chat.completions.create(**params)
            
            # Add to history
            for msg in messages:
                if msg["role"] != "system":
                    self.add_to_history(msg["role"], msg["content"])
            
            assistant_response = response.choices[0].message.content
            self.add_to_history("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
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
    
    def get_models(self) -> List[str]:
        """Get available models"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if model.id.startswith('gpt')]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return list(self.MODELS.values()) 