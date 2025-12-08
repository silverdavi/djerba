#!/usr/bin/env python3
"""
Batch Research All Recipes
Run comprehensive research on all 35 recipes using Perplexity Pro Search
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

class BatchRecipeResearch:
    def __init__(self):
        """Initialize the batch research interface"""
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        self.api_url = "https://api.perplexity.ai/chat/completions"
        
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        
        self.recipes_dir = "data/safed_recipes_en"
        self.research_output_dir = "data/recipe_research"
        Path(self.research_output_dir).mkdir(parents=True, exist_ok=True)
        
        self.successful = 0
        self.failed = 0
        self.start_time = None
    
    def load_recipe(self, recipe_file: str):
        """Load a recipe from JSON file"""
        file_path = Path(self.recipes_dir) / recipe_file
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_recipes(self):
        """List all available recipes"""
        return sorted([f for f in os.listdir(self.recipes_dir) if f.endswith('.json')])
    
    def research_recipe_history(self, recipe_name: str, recipe_data: dict) -> str:
        """Research the historical and cultural background of a recipe"""
        
        prompt = f"""Conduct a focused research on the recipe "{recipe_data['name_english']}" ({recipe_data['name_hebrew']}).

Please provide concise findings on:

1. **Historical Origins**: Where and when did this dish originate? Connection to Tunisian-Djerban Jewish culture?
2. **Cultural Significance**: Why is it important? When is it traditionally served?
3. **Etymology**: What does the name mean?
4. **Regional Variations**: How do different regions prepare this dish?

Keep the response well-structured, informative, and cite sources."""

        return self._send_pro_search_query(prompt, recipe_name, "history", recipe_data)
    
    def _send_pro_search_query(self, prompt: str, recipe_name: str, research_type: str, recipe_data: dict) -> str:
        """Send a Pro Search query to Perplexity API with streaming"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True,
            "web_search_options": {
                "search_type": "pro"
            }
        }
        
        full_response = ""
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code != 200:
                print(f"  ❌ API Error: {response.status_code}")
                return ""
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    
                    if data_str == '[DONE]':
                        break
                    
                    try:
                        data = json.loads(data_str)
                        
                        if 'choices' in data and data['choices']:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            
                            if content:
                                full_response += content
                    
                    except json.JSONDecodeError:
                        continue
            
            # Save research to file
            self._save_research(recipe_name, research_type, full_response, recipe_data)
            
            return full_response
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return ""
    
    def _save_research(self, recipe_name: str, research_type: str, content: str, recipe_data: dict):
        """Save research results to a file"""
        
        safe_name = recipe_data.get('name_english', recipe_name).lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        filename = f"{safe_name}_{research_type}.md"
        file_path = Path(self.research_output_dir) / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {recipe_data.get('name_english', recipe_name).upper()} - {research_type.upper()}\n\n")
            f.write(f"**Hebrew Name:** {recipe_data.get('name_hebrew', 'N/A')}\n\n")
            f.write("---\n\n")
            f.write(content)
    
    def run_batch_research(self):
        """Run batch research on all recipes"""
        
        self.start_time = time.time()
        recipes = self.list_recipes()
        total = len(recipes)
        
        print("\n" + "=" * 80)
        print("BATCH RESEARCH - ALL RECIPES")
        print("=" * 80)
        print(f"\nTotal recipes to research: {total}")
        print(f"Research type: Historical & Cultural Background")
        print(f"Output directory: {self.research_output_dir}")
        print("\n" + "=" * 80 + "\n")
        
        for i, recipe_file in enumerate(recipes, 1):
            recipe_data = self.load_recipe(recipe_file)
            if not recipe_data:
                print(f"[{i:2d}/{total}] ❌ Failed to load {recipe_file}")
                self.failed += 1
                continue
            
            recipe_name = recipe_data.get('name_english', 'Unknown')
            print(f"[{i:2d}/{total}] 🔍 Researching: {recipe_name:<40}", end=" ", flush=True)
            
            try:
                self.research_recipe_history(recipe_file, recipe_data)
                print("✓ Done")
                self.successful += 1
            except Exception as e:
                print(f"✗ Error: {e}")
                self.failed += 1
            
            # Add delay to avoid rate limiting (be respectful to the API)
            if i < total:
                time.sleep(2)
        
        self._print_summary()
    
    def _print_summary(self):
        """Print completion summary"""
        
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        print("\n" + "=" * 80)
        print("BATCH RESEARCH COMPLETE")
        print("=" * 80)
        print(f"\n✓ Successful: {self.successful} recipes")
        print(f"✗ Failed: {self.failed} recipes")
        print(f"⏱ Time elapsed: {minutes}m {seconds}s")
        print(f"📁 Output directory: {self.research_output_dir}/")
        print(f"\nAll research files have been saved as markdown with citations!")
        print("\n" + "=" * 80 + "\n")


def main():
    """Main entry point"""
    
    try:
        batch = BatchRecipeResearch()
        print("\n✓ Batch Research Interface Initialized")
        print(f"  API Key: {batch.api_key[:20]}...")
        
        batch.run_batch_research()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

