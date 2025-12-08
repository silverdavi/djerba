#!/usr/bin/env python3
"""
Process All Recipes with Status Tracking - PARALLEL VERSION
Systematically processes every recipe in the CSV with detailed status tracking using multiple threads
"""

import pandas as pd
import csv
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from cookbook_pipeline import CookbookPipeline

class ParallelRecipeProcessor:
    def __init__(self, num_workers=30):
        self.num_workers = num_workers
        self.status_file = "recipe_processing_status.csv"
        self.progress_file = "recipe_processing_progress.json"
        self.results_df = None
        self.current_index = 0
        self.lock = threading.Lock()  # For thread-safe operations
        
        # Create pipeline instances for each worker (thread-safe)
        self.pipelines = {}
        
    def get_pipeline(self):
        """Get or create a pipeline instance for the current thread"""
        thread_id = threading.current_thread().ident
        if thread_id not in self.pipelines:
            self.pipelines[thread_id] = CookbookPipeline()
        return self.pipelines[thread_id]
        
    def load_recipes(self):
        """Load all recipes from CSV into DataFrame"""
        print("📋 Loading recipes from CSV...")
        
        # Load the CSV file
        df = pd.read_csv("RecipesDjerba.csv")
        
        # Clean up and filter valid recipes
        df = df.dropna(subset=['SOURCE', 'Dish (Hebrew)'])  # Remove empty rows
        df = df[df['SOURCE'].str.strip() != '']  # Remove rows with empty source
        df = df[df['Dish (Hebrew)'].str.strip() != '']  # Remove rows with empty Hebrew name
        
        # Create processing status columns with proper dtypes
        df['processing_status'] = 'PENDING'
        df['processing_timestamp'] = ''
        df['error_message'] = ''
        df['files_generated'] = ''
        df['processing_duration'] = ''
        df['worker_thread'] = ''
        
        # Ensure string columns are object dtype to avoid pandas warnings
        for col in ['processing_status', 'processing_timestamp', 'error_message', 
                   'files_generated', 'processing_duration', 'worker_thread']:
            df[col] = df[col].astype('object')
        
        print(f"✅ Loaded {len(df)} valid recipes for processing")
        return df
    
    def save_status(self):
        """Save current status to CSV (thread-safe)"""
        with self.lock:
            if self.results_df is not None:
                self.results_df.to_csv(self.status_file, index=False)
                print(f"💾 Status saved to {self.status_file}")
    
    def save_progress(self):
        """Save progress metadata to JSON (thread-safe)"""
        with self.lock:
            if self.results_df is None:
                return
                
            progress_data = {
                "last_updated": datetime.now().isoformat(),
                "total_recipes": int(len(self.results_df)),
                "current_index": int(self.current_index),
                "completed": int(len(self.results_df[self.results_df['processing_status'] == 'SUCCESS'])),
                "failed": int(len(self.results_df[self.results_df['processing_status'] == 'ERROR'])),
                "pending": int(len(self.results_df[self.results_df['processing_status'] == 'PENDING'])),
                "workers": int(self.num_workers)
            }
            
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
    
    def process_single_recipe_with_tracking(self, recipe_data):
        """Process a single recipe and track its status (thread-safe)"""
        index, row = recipe_data
        thread_id = threading.current_thread().ident
        
        recipe = {
            'source': row['SOURCE'],
            'hebrew_name': row['Dish (Hebrew)'],
            'description': row['Dish description'],
            'english_name': row['Dish (English)'],
            'native_name': row['Dish native name (Tunisia, Morocco, Israel)'],
            'type': row['Type (Main/Side/Dip/Soup/Snack)'],
            'served': row['Served (Hot/Cold)'],
            'flavor': row['Flavor (Sweet/Savory)'],
            'notes': row['Notes']
        }
        
        english_name = recipe['english_name'] if recipe['english_name'] else f"Recipe_{index}"
        hebrew_name = recipe['hebrew_name']
        
        print(f"🧵 Thread-{thread_id % 1000:03d} | 📖 Recipe {index + 1}/{len(self.results_df)} | 🍽️  {english_name} ({hebrew_name})")
        
        start_time = time.time()
        
        try:
            # Get thread-specific pipeline
            pipeline = self.get_pipeline()
            
            # Process the recipe through the pipeline
            result = pipeline.process_single_recipe(recipe)
            
            with self.lock:  # Thread-safe DataFrame updates
                if result:
                    # Success - update status
                    duration = time.time() - start_time
                    files_generated = self.get_generated_files(english_name)
                    
                    self.results_df.at[index, 'processing_status'] = 'SUCCESS'
                    self.results_df.at[index, 'processing_timestamp'] = datetime.now().isoformat()
                    self.results_df.at[index, 'files_generated'] = ', '.join(files_generated)
                    self.results_df.at[index, 'processing_duration'] = f"{duration:.1f}s"
                    self.results_df.at[index, 'worker_thread'] = f"thread-{thread_id % 1000:03d}"
                    
                    print(f"✅ Thread-{thread_id % 1000:03d} | {english_name} completed successfully! ({duration:.1f}s, {len(files_generated)} files)")
                    
                else:
                    # Failed but no exception
                    self.results_df.at[index, 'processing_status'] = 'ERROR'
                    self.results_df.at[index, 'processing_timestamp'] = datetime.now().isoformat()
                    self.results_df.at[index, 'error_message'] = 'Pipeline returned None'
                    self.results_df.at[index, 'worker_thread'] = f"thread-{thread_id % 1000:03d}"
                    print(f"❌ Thread-{thread_id % 1000:03d} | {english_name} failed - pipeline returned None")
                    
        except Exception as e:
            # Exception occurred
            error_msg = str(e)
            with self.lock:  # Thread-safe DataFrame updates
                self.results_df.at[index, 'processing_status'] = 'ERROR'
                self.results_df.at[index, 'processing_timestamp'] = datetime.now().isoformat()
                self.results_df.at[index, 'error_message'] = error_msg
                self.results_df.at[index, 'worker_thread'] = f"thread-{thread_id % 1000:03d}"
            print(f"❌ Thread-{thread_id % 1000:03d} | {english_name} failed with error: {error_msg}")
        
        return index, self.results_df.at[index, 'processing_status'] == 'SUCCESS'
    
    def get_generated_files(self, recipe_name):
        """Check what files were generated for a recipe"""
        pipeline = self.get_pipeline()
        safe_name = pipeline.safe_filename(recipe_name)
        files = []
        
        # Check for main recipe file
        recipe_file = Path(f"data/recipes/markdown/{safe_name}.md")
        if recipe_file.exists():
            files.append("recipe.md")
        
        # Check for translations
        for lang in ['hebrew', 'spanish', 'arabic']:
            trans_file = Path(f"data/recipes/translations/{safe_name}_{lang}.md")
            if trans_file.exists():
                files.append(f"trans_{lang}.md")
        
        # Check for research files
        for research_type in ['etymology', 'vegan', 'synthesis']:
            research_file = Path(f"data/research/{safe_name}_{research_type}.txt")
            if research_file.exists():
                files.append(f"research_{research_type}.txt")
        
        # Check for image
        image_file = Path(f"data/images/generated/{safe_name}.png")
        if image_file.exists():
            files.append("image.png")
        
        return files
    
    def load_existing_progress(self):
        """Load existing progress if available"""
        if Path(self.status_file).exists():
            print(f"📄 Loading existing progress from {self.status_file}")
            self.results_df = pd.read_csv(self.status_file)
            
            # Add worker_thread column if not present (for backwards compatibility)
            if 'worker_thread' not in self.results_df.columns:
                self.results_df['worker_thread'] = ''
            
            # Find where to resume
            pending_recipes = self.results_df[self.results_df['processing_status'] == 'PENDING']
            if len(pending_recipes) > 0:
                self.current_index = pending_recipes.index[0]
                print(f"🔄 Resuming from recipe {self.current_index + 1}")
            else:
                print("✅ All recipes already processed!")
                return True
        else:
            print("🆕 Starting fresh processing")
            self.results_df = self.load_recipes()
            self.current_index = 0
        
        return False
    
    def print_summary(self):
        """Print processing summary"""
        if self.results_df is None:
            return
            
        total = len(self.results_df)
        success = len(self.results_df[self.results_df['processing_status'] == 'SUCCESS'])
        failed = len(self.results_df[self.results_df['processing_status'] == 'ERROR'])
        pending = len(self.results_df[self.results_df['processing_status'] == 'PENDING'])
        
        print("\n" + "=" * 60)
        print("📊 PARALLEL PROCESSING SUMMARY")
        print("=" * 60)
        print(f"📋 Total Recipes: {total}")
        print(f"✅ Successful: {success}")
        print(f"❌ Failed: {failed}")
        print(f"⏳ Pending: {pending}")
        print(f"📈 Success Rate: {(success/total)*100:.1f}%")
        print(f"🧵 Workers Used: {self.num_workers}")
        
        if success > 0:
            # Calculate average processing time
            successful_recipes = self.results_df[self.results_df['processing_status'] == 'SUCCESS']
            durations = successful_recipes['processing_duration'].str.replace('s', '').astype(float)
            avg_duration = durations.mean()
            print(f"⏱️  Average Duration: {avg_duration:.1f}s per recipe")
        
        if failed > 0:
            print(f"\n❌ Failed Recipes:")
            failed_recipes = self.results_df[self.results_df['processing_status'] == 'ERROR']
            for idx, row in failed_recipes.iterrows():
                recipe_name = row['Dish (English)'] or f"Recipe_{idx}"
                error = row['error_message'][:50] + "..." if len(str(row['error_message'])) > 50 else row['error_message']
                thread = row.get('worker_thread', 'unknown')
                print(f"   • {recipe_name} ({thread}): {error}")
        
        print(f"\n📁 Results saved to:")
        print(f"   • {self.status_file} - Detailed status tracking")
        print(f"   • {self.progress_file} - Progress metadata")
    
    def run_all_parallel(self, start_from=None, limit=None):
        """Process all recipes with parallel execution and status tracking"""
        print("🚀 STARTING PARALLEL RECIPE PROCESSING")
        print("=" * 60)
        print(f"🧵 Using {self.num_workers} worker threads")
        print("Status will be tracked in real-time")
        print("=" * 60)
        
        # Load existing progress or start fresh
        all_done = self.load_existing_progress()
        if all_done:
            self.print_summary()
            return
        
        # Override start position if specified
        if start_from is not None:
            self.current_index = start_from
            print(f"🎯 Starting from recipe {start_from + 1}")
        
        # Determine recipes to process
        total_recipes = len(self.results_df)
        end_index = min(total_recipes, self.current_index + limit) if limit else total_recipes
        
        # Get pending recipes to process
        recipes_to_process = []
        for index in range(self.current_index, end_index):
            row = self.results_df.iloc[index]
            if row['processing_status'] == 'PENDING':
                recipes_to_process.append((index, row))
            else:
                print(f"⏭️  Skipping {row['Dish (English)']} - already {row['processing_status']}")
        
        if not recipes_to_process:
            print("✅ No pending recipes to process!")
            self.print_summary()
            return
        
        print(f"📋 Processing {len(recipes_to_process)} recipes with {self.num_workers} workers")
        print(f"🎯 Recipe range: {self.current_index + 1} to {end_index} of {total_recipes}")
        
        # Process recipes in parallel
        start_time = time.time()
        completed_count = 0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            # Submit all recipes to the thread pool
            future_to_recipe = {
                executor.submit(self.process_single_recipe_with_tracking, recipe_data): recipe_data
                for recipe_data in recipes_to_process
            }
            
            # Process completed futures as they finish
            for future in as_completed(future_to_recipe):
                recipe_data = future_to_recipe[future]
                index, recipe_name = recipe_data[0], recipe_data[1]['Dish (English)']
                
                try:
                    result_index, success = future.result()
                    if success:
                        completed_count += 1
                    else:
                        failed_count += 1
                    
                    # Save progress every 5 completed recipes
                    if (completed_count + failed_count) % 5 == 0:
                        self.save_status()
                        self.save_progress()
                        
                        # Print progress update
                        processed = completed_count + failed_count
                        total_to_process = len(recipes_to_process)
                        elapsed = time.time() - start_time
                        rate = processed / elapsed if elapsed > 0 else 0
                        eta = (total_to_process - processed) / rate if rate > 0 else 0
                        
                        print(f"📊 Progress: {processed}/{total_to_process} ({(processed/total_to_process)*100:.1f}%) | "
                              f"✅ {completed_count} success | ❌ {failed_count} failed | "
                              f"⏱️  {elapsed:.0f}s elapsed | ETA: {eta:.0f}s")
                
                except Exception as exc:
                    print(f"❌ Recipe {recipe_name} generated an exception: {exc}")
                    failed_count += 1
        
        # Final save and summary
        self.save_status()
        self.save_progress()
        
        total_time = time.time() - start_time
        print(f"\n🎉 Parallel processing completed!")
        print(f"⏱️  Total time: {total_time:.1f} seconds")
        print(f"🚀 Average rate: {len(recipes_to_process)/total_time:.1f} recipes/second")
        
        self.print_summary()

def main():
    """Main execution with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process all recipes with parallel execution and status tracking')
    parser.add_argument('--workers', type=int, default=30,
                       help='Number of worker threads (default: 30)')
    parser.add_argument('--start-from', type=int, 
                       help='Start from specific recipe index (0-based)')
    parser.add_argument('--limit', type=int, 
                       help='Limit number of recipes to process')
    parser.add_argument('--resume', action='store_true', 
                       help='Resume from last unprocessed recipe')
    parser.add_argument('--status-only', action='store_true', 
                       help='Show current status without processing')
    
    args = parser.parse_args()
    
    processor = ParallelRecipeProcessor(num_workers=args.workers)
    
    if args.status_only:
        if Path(processor.status_file).exists():
            processor.results_df = pd.read_csv(processor.status_file)
            processor.print_summary()
        else:
            print("❌ No status file found. Run processing first.")
        return
    
    if args.resume:
        processor.run_all_parallel()
    else:
        processor.run_all_parallel(start_from=args.start_from, limit=args.limit)

if __name__ == "__main__":
    main() 