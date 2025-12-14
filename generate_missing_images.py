#!/usr/bin/env python3
"""
Generate images for recipes that are missing them.
Uses the image generation prompts from canonical recipes.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

CANONICAL_DIR = Path("data/recipes_canonical")
IMAGES_DIR = Path("data/images/current")
MULTILINGUAL_DIR = Path("data/recipes_multilingual_v2")

# Recipes that need images (from recipe_image_index.json)
MISSING_RECIPES = [
    "chicken_fricassee_stew",
]

def get_next_index():
    """Get the next available index for image folders."""
    existing = list(IMAGES_DIR.iterdir())
    max_idx = 0
    for d in existing:
        if d.is_dir():
            parts = d.name.split("_", 1)
            if len(parts) >= 1 and parts[0].isdigit():
                max_idx = max(max_idx, int(parts[0]))
    return max_idx + 1

def generate_image_for_recipe(recipe_id: str, index: int, generator) -> dict:
    """Generate image for a single recipe."""
    # Find the canonical file
    canonical_path = CANONICAL_DIR / f"{recipe_id}.json"
    if not canonical_path.exists():
        return {"recipe": recipe_id, "success": False, "error": "Canonical file not found"}
    
    with open(canonical_path) as f:
        recipe = json.load(f)
    
    # Get the generation prompt
    image_data = recipe.get("image", {})
    prompt = image_data.get("generation_prompt")
    
    if not prompt:
        return {"recipe": recipe_id, "success": False, "error": "No generation prompt found"}
    
    # Create output folder
    folder_name = f"{index:03d}_{recipe_id}"
    output_dir = IMAGES_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "dish.png"
    
    try:
        # Generate the image
        print(f"  🎨 Generating: {recipe.get('name', recipe_id)}")
        
        result = generator.generate_custom_image(
            prompt=prompt,
            output_path=str(output_path),
            add_cookbook_style=False  # Prompt already has full styling
        )
        
        if result and output_path.exists():
            # Update canonical with new image path
            relative_path = f"images/current/{folder_name}/dish.png"
            recipe["image"]["filename"] = relative_path
            
            with open(canonical_path, "w") as f:
                json.dump(recipe, f, indent=2, ensure_ascii=False)
            
            return {
                "recipe": recipe_id,
                "success": True,
                "path": relative_path,
                "folder": folder_name
            }
        else:
            return {"recipe": recipe_id, "success": False, "error": "Generation failed"}
            
    except Exception as e:
        return {"recipe": recipe_id, "success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Generate missing recipe images")
    parser.add_argument("--workers", type=int, default=30, help="Number of parallel workers")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--single", help="Generate for a single recipe ID")
    args = parser.parse_args()
    
    # Import generator
    from generate_cookbook_images import CookbookImageGenerator
    
    # Determine which recipes to process
    if args.single:
        recipes_to_process = [args.single]
    else:
        recipes_to_process = MISSING_RECIPES
    
    print("=" * 60)
    print("🎨 GENERATING MISSING RECIPE IMAGES")
    print("=" * 60)
    print(f"\n📋 Recipes to process: {len(recipes_to_process)}")
    print(f"👷 Workers: {args.workers}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN - Would generate:")
        for r in recipes_to_process:
            canonical = CANONICAL_DIR / f"{r}.json"
            if canonical.exists():
                with open(canonical) as f:
                    data = json.load(f)
                prompt = data.get("image", {}).get("generation_prompt", "")[:100]
                print(f"  ✓ {r}: {prompt}...")
            else:
                print(f"  ✗ {r}: Canonical file not found")
        return
    
    # Get starting index
    start_index = get_next_index()
    print(f"\n🔢 Starting at index: {start_index}")
    
    # Create generator (each thread will use its own client)
    generator = CookbookImageGenerator()
    
    # Process recipes in PARALLEL
    results = []
    total = len(recipes_to_process)
    
    print(f"\n🚀 Starting PARALLEL generation with {args.workers} workers...\n")
    
    # Create tasks with pre-assigned indices
    tasks = [(recipe_id, start_index + i) for i, recipe_id in enumerate(recipes_to_process)]
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        future_to_recipe = {
            executor.submit(generate_image_for_recipe, recipe_id, idx, generator): recipe_id
            for recipe_id, idx in tasks
        }
        
        # Collect results as they complete
        completed = 0
        for future in as_completed(future_to_recipe):
            recipe_id = future_to_recipe[future]
            completed += 1
            try:
                result = future.result()
                results.append(result)
                if result["success"]:
                    print(f"✅ [{completed}/{total}] {recipe_id} -> {result['folder']}")
                else:
                    print(f"❌ [{completed}/{total}] {recipe_id}: {result.get('error', 'Unknown error')}")
            except Exception as e:
                results.append({"recipe": recipe_id, "success": False, "error": str(e)})
                print(f"❌ [{completed}/{total}] {recipe_id}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 GENERATION SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if failed:
        print("\nFailed recipes:")
        for r in failed:
            print(f"  - {r['recipe']}: {r.get('error', 'Unknown')}")
    
    # Save results
    with open("image_generation_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: image_generation_results.json")

if __name__ == "__main__":
    main()

