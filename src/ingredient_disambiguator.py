#!/usr/bin/env python3
"""
Ingredient and Recipe Disambiguator
====================================

Uses Gemini to resolve ambiguous ingredients and recipe names in Hebrew recipes.
Particularly useful for:
1. Ambiguous "pepper" mentions (bell pepper vs hot pepper vs black pepper)
2. Hebrew words with implied vowels (עג׳ה vs ג׳ה)
3. Traditional Tunisian/Djerban dish variants

Example:
    disambiguator = RecipeDisambiguator()
    
    # Resolve ambiguous ingredient
    clarified = disambiguator.clarify_ingredient(
        ingredient="פלפל",
        recipe_context="עם עגבניות וטופו",
        recipe_name="מרק אדום"
    )
    # Returns: "bell pepper" or "hot green pepper" based on context
    
    # Resolve ambiguous recipe name
    dish = disambiguator.clarify_recipe_name(
        hebrew_name="עג׳ה",
        recipe_ingredients=["עדשים", "בצל", "שום"]
    )
    # Returns: "Eeja" (lentil dish) with confidence score
"""

import os
import re
import json
from typing import Dict, Optional, Tuple, List
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Configure Gemini
if GEMINI_AVAILABLE:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class RecipeDisambiguator:
    """
    Disambiguates ambiguous ingredients and recipe names using Gemini.
    Specialized for Tunisian Djerban Jewish cuisine.
    """
    
    # Known ambiguous ingredients and their clarifications
    AMBIGUOUS_INGREDIENTS = {
        'pepper': {
            'alternatives': ['bell pepper', 'hot green pepper', 'hot red pepper', 'black pepper'],
            'common_tunisian': ['long hot green pepper', 'hot red pepper'],
        },
        'פפר': {
            'alternatives': ['פלפל כל' , 'פפר חריף ירוק ארוך', 'פפר שחור'],
            'common_tunisian': ['פפר חריף ירוק ארוך', 'פפר אדום חריף'],
        },
        'עגבנייה': {
            'alternatives': ['עגבניה אדומה', 'עגבנייה שרופה'],
            'common_tunisian': ['עגבניה אדומה טרייה'],
        },
    }
    
    # Hebrew recipes with vowel ambiguity
    HEBREW_DISH_VARIANTS = {
        'עג׳ה': {
            'variants': ['Eeja', 'Aja'],
            'description_en': 'Lentil or chickpea stew, sometimes with spinach or other greens',
            'color_profile': 'reddish-brown stew base',
        },
        'דביח': {
            'variants': ['Dbeekh', 'Dbaakh'],
            'description_en': 'Meat or vegetable stew, can be plain or festive',
            'color_profile': 'brown savory stew',
        },
    }
    
    def __init__(self, model: str = "gemini-3-pro-preview"):
        """Initialize disambiguator with Gemini model."""
        self.model = model
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Install with: pip install google-generativeai")
    
    def clarify_ingredient(
        self,
        ingredient: str,
        recipe_name: str = "",
        other_ingredients: Optional[List[str]] = None,
        max_retries: int = 3
    ) -> Dict:
        """
        Clarify an ambiguous ingredient using recipe context.
        
        Args:
            ingredient: The ambiguous ingredient (e.g., "pepper", "פפר")
            recipe_name: Name of the recipe for context
            other_ingredients: Other ingredients in the recipe for context
            max_retries: Number of retries on API failure
            
        Returns:
            Dict with:
                - 'ingredient': Original ingredient
                - 'clarified': Most likely clarification (e.g., "hot green pepper")
                - 'alternatives': List of possible interpretations
                - 'confidence': 0.0-1.0 confidence score
                - 'reasoning': Explanation of the clarification
        """
        
        if not GEMINI_AVAILABLE:
            return {
                'ingredient': ingredient,
                'clarified': ingredient,
                'alternatives': [],
                'confidence': 0.0,
                'reasoning': 'Gemini API not available (google-generativeai not installed)'
            }
        
        # Build context from recipe
        context_parts = []
        if recipe_name:
            context_parts.append(f"In recipe: {recipe_name}")
        if other_ingredients:
            context_parts.append(f"With: {', '.join(other_ingredients[:3])}")
        context = "\n".join(context_parts) if context_parts else ""
        
        # Gemini 3 Pro user prompt
        user_prompt = f"""Classify this ingredient in context of Tunisian Djerban cuisine.

Ingredient: {ingredient}
{context}

Return valid JSON with exactly these fields (no markdown, no extra text):
{{"clarified": "specific type", "alternatives": ["alt1", "alt2"], "confidence": 0.8, "reasoning": "explanation"}}"""
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel(self.model)
                
                response = model.generate_content(
                    user_prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.1,
                        max_output_tokens=200,
                    )
                )
                
                # Get the actual text from response
                response_text = None
                if response.candidates:
                    cand = response.candidates[0]
                    # Check finish reason (1 = STOP = good)
                    if hasattr(cand, 'finish_reason') and cand.finish_reason == 1:
                        # Try to get text
                        if cand.content and cand.content.parts:
                            response_text = cand.content.parts[0].text
                
                if response_text:
                    # Parse JSON response
                    json_str = response_text.strip()
                    if json_str.startswith("```"):
                        json_str = re.sub(r'^```(?:json)?\n?', '', json_str)
                        json_str = re.sub(r'\n?```$', '', json_str)
                    
                    result = json.loads(json_str)
                    result['ingredient'] = ingredient
                    return result
                    
            except Exception:
                pass
        
        return {
            'ingredient': ingredient,
            'clarified': ingredient,
            'alternatives': [],
            'confidence': 0.0,
            'reasoning': 'Could not clarify ingredient'
        }
    
    def clarify_recipe_name(
        self,
        hebrew_name: str,
        english_name: Optional[str] = None,
        ingredients: Optional[List[str]] = None,
        max_retries: int = 2
    ) -> Dict:
        """
        Clarify an ambiguous Hebrew recipe name, especially those with vowel ambiguity.
        
        Args:
            hebrew_name: Hebrew name of the recipe
            english_name: Known English transliteration (if any)
            ingredients: Ingredients list for context
            max_retries: Number of retries on API failure
            
        Returns:
            Dict with:
                - 'hebrew_name': Original Hebrew name
                - 'canonical_name': Standard English name
                - 'transliterations': List of acceptable transliterations
                - 'confidence': 0.0-1.0 confidence score
                - 'description': English description
                - 'color_profile': Visual description for image generation
                - 'reasoning': Explanation
        """
        
        if not GEMINI_AVAILABLE:
            return {
                'hebrew_name': hebrew_name,
                'canonical_name': english_name or hebrew_name,
                'transliterations': [],
                'confidence': 0.0,
                'description': '',
                'color_profile': '',
                'reasoning': 'Gemini API not available'
            }
        
        # Simple system prompt to avoid safety filters
        system_prompt = """Respond with JSON about traditional dishes."""
        
        context_parts = []
        if english_name:
            context_parts.append(f"Also called: {english_name}")
        if ingredients:
            ingredients_str = ", ".join(ingredients[:3])
            context_parts.append(f"Contains: {ingredients_str}")
        context_str = " ".join(context_parts) if context_parts else ""
        
        # Simpler prompt
        user_prompt = f"""Dish info:
Name (Hebrew): {hebrew_name}
{context_str}

Return JSON: {{"canonical_name": "English name", "transliterations": ["trans1"], "description": "What it is", "color_profile": "Visual", "confidence": 0.7, "reasoning": "Context"}}"""
        
        # All recipe name disambiguation goes through Gemini API
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel(self.model)
                
                response = model.generate_content(
                    user_prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.05,
                        max_output_tokens=300,
                    )
                )
                
                # Check response
                if response.candidates and response.candidates[0].finish_reason == 1:
                    cand = response.candidates[0]
                    if cand.content and cand.content.parts:
                        response_text = cand.content.parts[0].text
                        
                        # Parse JSON
                        json_str = response_text.strip()
                        if json_str.startswith("```"):
                            json_str = re.sub(r'^```(?:json)?\n?', '', json_str)
                            json_str = re.sub(r'\n?```$', '', json_str)
                        
                        result = json.loads(json_str)
                        result['hebrew_name'] = hebrew_name
                        return result
                    
            except Exception:
                pass
        
        return {
            'hebrew_name': hebrew_name,
            'canonical_name': english_name or hebrew_name,
            'transliterations': [],
            'description': '',
            'color_profile': '',
            'confidence': 0.0,
            'reasoning': 'Could not clarify recipe name'
        }
    
    def enhance_ingredient_list(
        self,
        ingredients: List[str],
        recipe_name: str = ""
    ) -> Dict[str, str]:
        """
        Enhance a list of ingredients by clarifying all with Gemini API.
        
        Args:
            ingredients: List of ingredient strings
            recipe_name: Name of recipe for context
            
        Returns:
            Dict mapping original -> clarified ingredient
        """
        clarifications = {}
        
        for ingredient in ingredients:
            result = self.clarify_ingredient(
                ingredient,
                recipe_name=recipe_name,
                other_ingredients=[i for i in ingredients if i != ingredient]
            )
            if result['confidence'] >= 0.5:
                clarifications[ingredient] = result['clarified']
        
        return clarifications


# Example usage and testing
if __name__ == "__main__":
    if not GEMINI_AVAILABLE:
        print("❌ google-generativeai not installed")
        print("Install with: pip install google-generativeai")
        exit(1)
    
    disambiguator = RecipeDisambiguator()
    
    # Test 1: Clarify ambiguous ingredient
    print("=" * 60)
    print("Test 1: Clarifying ambiguous ingredient 'pepper'")
    print("=" * 60)
    result = disambiguator.clarify_ingredient(
        ingredient="pepper",
        recipe_name="Harimi",
        other_ingredients=["tomatoes", "garlic", "olive oil", "tofu"]
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test 2: Clarify Hebrew recipe name
    print("\n" + "=" * 60)
    print("Test 2: Clarifying ambiguous Hebrew recipe name 'עג׳ה'")
    print("=" * 60)
    result = disambiguator.clarify_recipe_name(
        hebrew_name="עג׳ה",
        ingredients=["עדשים", "בצל", "שום", "שמן", "מים"]
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n✅ Disambiguation tests complete!")
