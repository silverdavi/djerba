#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recipe Processing Pipeline
Processes recipes through multiple stages using LLM clients
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import asyncio

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from llm.openai.client import OpenAIClient
from llm.perplexity.client import PerplexityClient
from utils.text_processing import clean_text, is_hebrew, format_recipe_content

class RecipePipeline:
    """Recipe processing pipeline manager"""
    
    STAGES = {
        "1_original_hebrew": "Original Hebrew recipe",
        "2_cleaned_hebrew": "Cleaned and structured Hebrew",
        "3_translated_english": "English translation", 
        "4_enhanced_content": "Enhanced with tips and context",
        "5_final_formatted": "Final formatted version"
    }
    
    def __init__(self):
        self.openai_client = None
        self.perplexity_client = None
        self.project_root = Path(__file__).parent.parent.parent
        self.recipes_dir = self.project_root / "recipes"
    
    def initialize_clients(self):
        """Initialize LLM clients"""
        try:
            self.openai_client = OpenAIClient(model="gpt-4.1-mini")
            print("✅ OpenAI client initialized")
        except Exception as e:
            print(f"⚠️  OpenAI client failed: {e}")
        
        try:
            self.perplexity_client = PerplexityClient(model="sonar")
            print("✅ Perplexity client initialized")
        except Exception as e:
            print(f"⚠️  Perplexity client failed: {e}")
    
    def get_recipe_folders(self) -> List[Path]:
        """Get all recipe folders"""
        if not self.recipes_dir.exists():
            return []
        
        folders = [d for d in self.recipes_dir.iterdir() if d.is_dir()]
        folders.sort()
        return folders
    
    def load_pipeline_metadata(self, recipe_folder: Path) -> Dict:
        """Load pipeline metadata for a recipe"""
        metadata_file = recipe_folder / "pipeline_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_pipeline_metadata(self, recipe_folder: Path, metadata: Dict):
        """Save pipeline metadata for a recipe"""
        metadata_file = recipe_folder / "pipeline_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def process_stage_2_cleaned_hebrew(self, recipe_folder: Path) -> bool:
        """Stage 2: Clean and structure Hebrew content"""
        try:
            # Read original Hebrew
            original_file = recipe_folder / "1_original_hebrew" / "1_original_hebrew.md"
            if not original_file.exists():
                print(f"❌ Original Hebrew file not found: {original_file}")
                return False
            
            with open(original_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Clean and structure using OpenAI
            if not self.openai_client:
                print("❌ OpenAI client not available for Hebrew cleaning")
                return False
            
            system_prompt = """אתה עוזר מטבח מומחה. המטרה שלך היא לנקות ולארגן מתכונים בעברית.
            
            הוראות:
            1. שמור על הטקסט בעברית
            2. ארגן את המתכון בפורמט אחיד: שם המתכון, רכיבים, הוראות הכנה
            3. תקן שגיאות כתיב קלות אם יש
            4. ודא שהרשימות מסודרות היטב
            5. שמור על כל המידע המקורי
            
            החזר רק את המתכון המתוקן בפורמט markdown."""
            
            cleaned_content = self.openai_client.send_message(
                f"נקה וארגן את המתכון הזה:\n\n{original_content}",
                system_prompt=system_prompt
            )
            
            # Save cleaned version
            cleaned_file = recipe_folder / "2_cleaned_hebrew" / "2_cleaned_hebrew.md"
            with open(cleaned_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ Stage 2 completed: {recipe_folder.name}")
            return True
            
        except Exception as e:
            print(f"❌ Stage 2 failed for {recipe_folder.name}: {e}")
            return False
    
    def process_stage_3_translated_english(self, recipe_folder: Path) -> bool:
        """Stage 3: Translate to English"""
        try:
            # Read cleaned Hebrew
            cleaned_file = recipe_folder / "2_cleaned_hebrew" / "2_cleaned_hebrew.md"
            if not cleaned_file.exists():
                print(f"❌ Cleaned Hebrew file not found: {cleaned_file}")
                return False
            
            with open(cleaned_file, 'r', encoding='utf-8') as f:
                hebrew_content = f.read()
            
            if not self.openai_client:
                print("❌ OpenAI client not available for translation")
                return False
            
            system_prompt = """You are a professional culinary translator specializing in Middle Eastern cuisine.
            
            Instructions:
            1. Translate the Hebrew recipe to clear, natural English
            2. Maintain the recipe structure: title, ingredients, instructions
            3. Use appropriate culinary terminology
            4. Keep measurements and cooking terms accurate
            5. Preserve all original information
            6. Format as clean markdown
            
            Return only the translated recipe in markdown format."""
            
            english_content = self.openai_client.send_message(
                f"Translate this Hebrew recipe to English:\n\n{hebrew_content}",
                system_prompt=system_prompt
            )
            
            # Save English version
            english_file = recipe_folder / "3_translated_english" / "3_translated_english.md"
            with open(english_file, 'w', encoding='utf-8') as f:
                f.write(english_content)
            
            print(f"✅ Stage 3 completed: {recipe_folder.name}")
            return True
            
        except Exception as e:
            print(f"❌ Stage 3 failed for {recipe_folder.name}: {e}")
            return False
    
    def process_stage_4_enhanced_content(self, recipe_folder: Path) -> bool:
        """Stage 4: Enhance with tips and context"""
        try:
            # Read English translation
            english_file = recipe_folder / "3_translated_english" / "3_translated_english.md"
            if not english_file.exists():
                print(f"❌ English translation not found: {english_file}")
                return False
            
            with open(english_file, 'r', encoding='utf-8') as f:
                english_content = f.read()
            
            # Use Perplexity to research and enhance
            if not self.perplexity_client:
                print("❌ Perplexity client not available for enhancement")
                return False
            
            # Extract recipe name for research
            recipe_name = english_content.split('\n')[0].replace('#', '').strip()
            
            # Research the dish
            research_query = f"Traditional Middle Eastern {recipe_name} recipe history, cooking tips, variations, cultural significance"
            research_results = self.perplexity_client.search_web(research_query)
            
            # Enhance with OpenAI
            if not self.openai_client:
                print("❌ OpenAI client not available for content enhancement")
                return False
            
            system_prompt = """You are a professional food writer and Middle Eastern cuisine expert.
            
            Instructions:
            1. Take the provided recipe and research information
            2. Enhance the recipe with:
               - Brief cultural background
               - Cooking tips and techniques
               - Ingredient substitutions
               - Serving suggestions
               - Storage recommendations
            3. Keep the original recipe intact but add valuable context
            4. Write in an engaging, informative style
            5. Format as clean markdown with clear sections
            
            Return the enhanced recipe with all additions clearly organized."""
            
            enhanced_content = self.openai_client.send_message(
                f"Enhance this recipe with the research information:\n\nRECIPE:\n{english_content}\n\nRESEARCH:\n{research_results}",
                system_prompt=system_prompt
            )
            
            # Save enhanced version
            enhanced_file = recipe_folder / "4_enhanced_content" / "4_enhanced_content.md"
            with open(enhanced_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            print(f"✅ Stage 4 completed: {recipe_folder.name}")
            return True
            
        except Exception as e:
            print(f"❌ Stage 4 failed for {recipe_folder.name}: {e}")
            return False
    
    def process_single_recipe(self, recipe_folder: Path, target_stage: Optional[str] = None):
        """Process a single recipe through the pipeline"""
        print(f"\n🍽️  Processing recipe: {recipe_folder.name}")
        
        # Load metadata
        metadata = self.load_pipeline_metadata(recipe_folder)
        pipeline_status = metadata.get("pipeline_status", {})
        
        # Determine which stages to run
        stages_to_run = []
        for stage_key in self.STAGES.keys():
            if target_stage and stage_key != target_stage:
                continue
            
            if pipeline_status.get(stage_key) != "completed":
                stages_to_run.append(stage_key)
            
            if target_stage and stage_key == target_stage:
                break
        
        # Process stages
        for stage in stages_to_run:
            print(f"  Running stage: {stage}")
            
            success = False
            if stage == "2_cleaned_hebrew":
                success = self.process_stage_2_cleaned_hebrew(recipe_folder)
            elif stage == "3_translated_english":
                success = self.process_stage_3_translated_english(recipe_folder)
            elif stage == "4_enhanced_content":
                success = self.process_stage_4_enhanced_content(recipe_folder)
            
            # Update metadata
            if success:
                pipeline_status[stage] = "completed"
            else:
                pipeline_status[stage] = "failed"
                break  # Stop on failure
        
        # Save updated metadata
        metadata["pipeline_status"] = pipeline_status
        self.save_pipeline_metadata(recipe_folder, metadata)
    
    def run_pipeline(self, recipe_filter: Optional[str] = None, target_stage: Optional[str] = None):
        """Run the pipeline on recipes"""
        print("🚀 Starting Recipe Processing Pipeline")
        print("=" * 50)
        
        self.initialize_clients()
        
        recipe_folders = self.get_recipe_folders()
        if not recipe_folders:
            print("❌ No recipe folders found. Run reorganize_recipes.py first.")
            return
        
        # Filter recipes if specified
        if recipe_filter:
            recipe_folders = [f for f in recipe_folders if recipe_filter in f.name]
        
        print(f"📋 Found {len(recipe_folders)} recipes to process")
        
        for recipe_folder in recipe_folders:
            try:
                self.process_single_recipe(recipe_folder, target_stage)
            except Exception as e:
                print(f"❌ Error processing {recipe_folder.name}: {e}")
        
        print("\n🎉 Pipeline processing completed!")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Recipe Processing Pipeline")
    parser.add_argument("--recipe", help="Process specific recipe (partial name match)")
    parser.add_argument("--stage", help="Process only specific stage", 
                       choices=list(RecipePipeline.STAGES.keys()))
    parser.add_argument("--list", action="store_true", help="List available recipes")
    
    args = parser.parse_args()
    
    pipeline = RecipePipeline()
    
    if args.list:
        folders = pipeline.get_recipe_folders()
        print(f"Available recipes ({len(folders)}):")
        for folder in folders:
            print(f"  - {folder.name}")
        return
    
    pipeline.run_pipeline(args.recipe, args.stage)

if __name__ == "__main__":
    main() 