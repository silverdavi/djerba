#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import unicodedata
from typing import List, Dict, Optional, Union
import tiktoken

def clean_text(text: str, remove_extra_whitespace: bool = True, 
               normalize_unicode: bool = True) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Normalize unicode
    if normalize_unicode:
        text = unicodedata.normalize('NFKC', text)
    
    # Remove extra whitespace
    if remove_extra_whitespace:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
    
    return text

def split_text_by_tokens(text: str, max_tokens: int = 2000, 
                        model: str = "gpt-4") -> List[str]:
    """Split text into chunks based on token count"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")  # Default encoding
    
    tokens = encoding.encode(text)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks

def split_text_by_paragraphs(text: str, max_paragraphs: int = 10) -> List[str]:
    """Split text by paragraphs"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    
    for paragraph in paragraphs:
        current_chunk.append(paragraph)
        if len(current_chunk) >= max_paragraphs:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))

def extract_hebrew_text(text: str) -> str:
    """Extract Hebrew characters from text"""
    hebrew_pattern = r'[\u0590-\u05FF\u200f\u200e\s]+'
    hebrew_matches = re.findall(hebrew_pattern, text)
    return ''.join(hebrew_matches).strip()

def is_hebrew(text: str) -> bool:
    """Check if text contains Hebrew characters"""
    hebrew_pattern = r'[\u0590-\u05FF]'
    return bool(re.search(hebrew_pattern, text))

def format_recipe_content(content: str) -> Dict[str, str]:
    """Format recipe content into structured sections"""
    sections = {
        'name': '',
        'ingredients': '',
        'instructions': '',
        'notes': ''
    }
    
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('שם המתכון:'):
            sections['name'] = line.replace('שם המתכון:', '').strip()
            current_section = 'name'
        elif line.startswith('רשימת מצרכים:'):
            current_section = 'ingredients'
        elif line.startswith('אופן ההכנה:'):
            current_section = 'instructions'
        elif current_section == 'ingredients':
            if sections['ingredients']:
                sections['ingredients'] += '\n'
            sections['ingredients'] += line
        elif current_section == 'instructions':
            if sections['instructions']:
                sections['instructions'] += '\n'
            sections['instructions'] += line
        else:
            if sections['notes']:
                sections['notes'] += '\n'
            sections['notes'] += line
    
    return sections

def create_summary_prompt(text: str, max_length: int = 200) -> str:
    """Create a prompt for summarizing text"""
    return f"""Please provide a concise summary of the following text in {max_length} words or less:

{text}

Summary:"""

def create_translation_prompt(text: str, target_language: str = "English") -> str:
    """Create a prompt for translating text"""
    return f"""Please translate the following text to {target_language}. Maintain the original meaning and context:

{text}

Translation:""" 