#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import json
import time
from datetime import datetime

class BaseLLMClient(ABC):
    """Base class for LLM clients"""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
        self.conversation_history = []
        
    @abstractmethod
    def send_message(self, message: str, **kwargs) -> str:
        """Send a message to the LLM and get response"""
        pass
    
    @abstractmethod
    def send_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send multiple messages (conversation) to the LLM"""
        pass
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def save_conversation(self, filepath: str):
        """Save conversation history to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
    
    def load_conversation(self, filepath: str):
        """Load conversation history from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.conversation_history = json.load(f)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        if not self.conversation_history:
            return {"total_messages": 0, "user_messages": 0, "assistant_messages": 0}
        
        user_count = sum(1 for msg in self.conversation_history if msg["role"] == "user")
        assistant_count = sum(1 for msg in self.conversation_history if msg["role"] == "assistant")
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": user_count,
            "assistant_messages": assistant_count,
            "first_message": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "last_message": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.call_times = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if now - t < 60]
        
        if len(self.call_times) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.call_times[0])
            if sleep_time > 0:
                print(f"Rate limit reached, waiting {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
        
        self.call_times.append(now) 