#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

class Config:
    """Configuration management for LLM scripts"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "src" / "data"
        self.config_dir = self.project_root / "src" / "config"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        
        # Load environment variables from .env files
        self._load_env_files()
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment"""
        return os.getenv("OPENAI_API_KEY")
    
    @property
    def perplexity_api_key(self) -> Optional[str]:
        """Get Perplexity API key from environment"""
        return os.getenv("PERPLEXITY_API_KEY")
    
    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Get Anthropic API key from environment"""
        return os.getenv("ANTHROPIC_API_KEY")
    
    def _load_env_files(self):
        """Load environment variables from .env files in order of priority"""
        # Load from multiple possible locations in order of priority
        env_files = [
            self.config_dir / ".env",  # src/config/.env (highest priority)
            self.project_root / ".env",  # project root .env
            Path.home() / ".djerba.env"  # user home directory
        ]
        
        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file, override=False)  # Don't override already set variables
                print(f"Loaded environment from: {env_file}")
    
    def validate_api_keys(self) -> dict:
        """Validate that required API keys are present"""
        keys = {
            "openai": self.openai_api_key,
            "perplexity": self.perplexity_api_key,
            "anthropic": self.anthropic_api_key
        }
        
        missing = [provider for provider, key in keys.items() if not key]
        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "available": [provider for provider, key in keys.items() if key]
        }

# Global config instance
config = Config() 