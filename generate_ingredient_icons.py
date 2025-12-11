#!/usr/bin/env python3
"""
Ingredient Icon Generator
=========================
Generates abstract flowing geometric representations of cooking ingredients
using Gemini 3 Pro Image generation, then removes backgrounds with rembg.

Uses 40 parallel workers for fast generation.

Usage:
    python generate_ingredient_icons.py
    python generate_ingredient_icons.py --dry-run  # Preview ingredients without generating
    python generate_ingredient_icons.py --ingredient "Tomatoes"  # Generate single ingredient
"""

import os
import sys
import csv
import asyncio
import hashlib
from pathlib import Path
from typing import List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

# Number of parallel workers
MAX_WORKERS = 40

# Thread-safe counter for progress
progress_lock = threading.Lock()
completed_count = 0
total_count = 0


def get_ingredient_color(ingredient: str) -> str:
    """
    Get the primary ink color based on the ingredient type.
    """
    ingredient_lower = ingredient.lower()
    
    # Reds/Oranges
    if any(x in ingredient_lower for x in ['tomato', 'paprika', 'harissa', 'chili', 'pepper', 'hot']):
        return "deep crimson red and burnt orange ink"
    
    # Yellows/Golds
    if any(x in ingredient_lower for x in ['turmeric', 'saffron', 'cumin', 'curry', 'lemon', 'banana', 'corn', 'mustard']):
        return "warm golden yellow and amber ink"
    
    # Greens
    if any(x in ingredient_lower for x in ['parsley', 'cilantro', 'dill', 'mint', 'basil', 'spinach', 'chard', 'green bean', 'zucchini', 'artichoke', 'olive', 'oregano', 'pea']):
        return "rich emerald green and sage ink"
    
    # Browns/Earthy
    if any(x in ingredient_lower for x in ['cinnamon', 'coffee', 'chocolate', 'cocoa', 'bread', 'wheat', 'barley', 'oat', 'nut', 'almond', 'peanut', 'date', 'raisin', 'seitan', 'mushroom']):
        return "warm sienna brown and caramel ink"
    
    # Creams/Tans (avoid pure white)
    if any(x in ingredient_lower for x in ['rice', 'milk', 'cream', 'tofu', 'coconut', 'semolina', 'couscous', 'garlic', 'onion', 'potato', 'cauliflower', 'flour']):
        return "warm tan, beige, and soft ochre ink"
    
    # Purples/Deep colors
    if any(x in ingredient_lower for x in ['eggplant', 'beet', 'wine', 'grape', 'plum']):
        return "deep purple and burgundy ink"
    
    # Orange/Warm
    if any(x in ingredient_lower for x in ['carrot', 'pumpkin', 'sweet potato', 'orange', 'apricot', 'mango', 'amba']):
        return "vibrant orange and terracotta ink"
    
    # Blues (for water, seaweed)
    if any(x in ingredient_lower for x in ['water', 'seaweed', 'wakame']):
        return "deep blue and teal ink"
    
    # Default - warm Mediterranean palette
    return "warm terracotta and olive green ink"


def generate_ingredient_prompt(ingredient: str) -> str:
    """
    Generate a prompt for creating a clean flowing pen illustration of an ingredient.
    """
    ink_color = get_ingredient_color(ingredient)
    
    prompt = f"""Create a clean, elegant hand-drawn illustration of "{ingredient}" with flowing colored pen strokes.

=== WHAT TO DRAW ===
Draw ONLY the {ingredient} itself - nothing else!
- The ingredient should be immediately recognizable
- Simple, clean composition - just the ingredient
- No extra decorative elements, no flourishes around it, no ornamental borders

=== ARTISTIC STYLE ===
- Clean hand-drawn illustration with flowing pen strokes
- Beautiful linework with varying thickness
- Elegant and simple - like a high-quality botanical illustration
- Confident, smooth pen lines
- Natural shading with pen strokes

=== INK COLORS ===
{ink_color}
Rich, saturated colored ink. Natural, realistic coloring for the ingredient.

=== COMPOSITION ===
- ONLY {ingredient} - centered, clean, simple
- NO decorative elements around it
- NO arabesques, NO flourishes, NO patterns
- NO extra objects or garnishes
- Just the beautiful ingredient itself
- PURE WHITE BACKGROUND

=== TECHNICAL REQUIREMENTS ===
- Square format (1:1 aspect ratio)
- PURE WHITE BACKGROUND (#FFFFFF)
- No text, no labels, no words
- High contrast between the drawing and white background

=== CRITICAL ===
CLEAN and SIMPLE! Just {ingredient} drawn beautifully with colored pen/ink.
No noise, no extra elements, no decorative patterns.
Think: elegant botanical illustration, clean and minimal.
"""
    return prompt


class IngredientIconGenerator:
    """
    Generates abstract geometric icons for cooking ingredients using Gemini,
    then removes backgrounds with rembg.
    """
    
    MODEL = "gemini-3-pro-image-preview"
    ASPECT_RATIO = "1:1"
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the generator.
        
        Args:
            output_dir: Directory to save generated images.
                       Defaults to data/images/ingredients
        """
        self._client = None
        self._genai = None
        self._types = None
        self._rembg_session = None
        
        # Set output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent / "data" / "images" / "ingredients"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Also create raw and final subdirectories
        (self.output_dir / "raw").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "final").mkdir(parents=True, exist_ok=True)
    
    def _get_client(self):
        """Lazy load the genai client."""
        if self._client is None:
            try:
                from google import genai
                from google.genai import types
                self._genai = genai
                self._types = types
            except ImportError:
                print("❌ google-genai package not installed.")
                print("Install with: pip install google-genai")
                sys.exit(1)
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key or api_key == 'your_google_api_key_here':
                raise ValueError(
                    "GOOGLE_API_KEY not found in environment. "
                    "Please set it in your .env file."
                )
            
            self._client = genai.Client(api_key=api_key)
        
        return self._client
    
    def _get_rembg_session(self):
        """Lazy load rembg session for background removal."""
        if self._rembg_session is None:
            try:
                from rembg import new_session
                # Use u2net model which works well for objects
                self._rembg_session = new_session("u2net")
            except ImportError:
                print("❌ rembg package not installed.")
                print("Install with: pip install rembg[gpu]")
                sys.exit(1)
        return self._rembg_session
    
    def _safe_filename(self, ingredient: str) -> str:
        """Convert ingredient name to safe filename."""
        # Replace special characters
        safe = ingredient.lower()
        safe = safe.replace(" ", "_")
        safe = safe.replace("/", "_")
        safe = safe.replace(",", "")
        safe = safe.replace("(", "")
        safe = safe.replace(")", "")
        safe = safe.replace("'", "")
        safe = safe.replace("-", "_")
        # Remove multiple underscores
        while "__" in safe:
            safe = safe.replace("__", "_")
        return safe
    
    def generate_icon(self, ingredient: str, force: bool = False) -> Tuple[bool, str]:
        """
        Generate an abstract icon for a single ingredient.
        
        Args:
            ingredient: Name of the ingredient
            force: Force regeneration even if file exists
            
        Returns:
            Tuple of (success, message)
        """
        global completed_count
        
        safe_name = self._safe_filename(ingredient)
        raw_path = self.output_dir / "raw" / f"{safe_name}.png"
        final_path = self.output_dir / "final" / f"{safe_name}.png"
        
        # Check if already exists
        if not force and final_path.exists():
            with progress_lock:
                completed_count += 1
                progress = f"[{completed_count}/{total_count}]"
            return True, f"{progress} ⏭️  Skipped (exists): {ingredient}"
        
        try:
            client = self._get_client()
            types = self._types
            
            # Generate the prompt
            prompt = generate_ingredient_prompt(ingredient)
            
            # Generate image
            response = client.models.generate_content(
                model=self.MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=self.ASPECT_RATIO,
                    ),
                )
            )
            
            # Save raw image
            image_saved = False
            for part in response.parts:
                if hasattr(part, 'as_image'):
                    image = part.as_image()
                    if image:
                        image.save(str(raw_path))
                        image_saved = True
                        break
            
            if not image_saved:
                with progress_lock:
                    completed_count += 1
                    progress = f"[{completed_count}/{total_count}]"
                return False, f"{progress} ❌ No image generated: {ingredient}"
            
            # Remove background using rembg
            self._remove_background(raw_path, final_path)
            
            with progress_lock:
                completed_count += 1
                progress = f"[{completed_count}/{total_count}]"
            
            return True, f"{progress} ✅ Generated: {ingredient}"
            
        except Exception as e:
            with progress_lock:
                completed_count += 1
                progress = f"[{completed_count}/{total_count}]"
            return False, f"{progress} ❌ Error ({ingredient}): {str(e)[:100]}"
    
    def _remove_background(self, input_path: Path, output_path: Path):
        """Remove white background from image, making it transparent."""
        try:
            from PIL import Image
            import numpy as np
            
            # Read input image
            input_image = Image.open(input_path).convert('RGBA')
            data = np.array(input_image)
            
            # Find white/near-white pixels and make them transparent
            # White is (255, 255, 255) - we'll catch near-white too (threshold)
            r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
            
            # Threshold for "white" - pixels where all RGB channels are > 240
            white_threshold = 240
            white_mask = (r > white_threshold) & (g > white_threshold) & (b > white_threshold)
            
            # Also catch light gray backgrounds (all channels similar and > 220)
            light_gray_mask = (r > 220) & (g > 220) & (b > 220) & (np.abs(r.astype(int) - g.astype(int)) < 15) & (np.abs(g.astype(int) - b.astype(int)) < 15)
            
            # Combine masks
            background_mask = white_mask | light_gray_mask
            
            # Set alpha to 0 for background pixels
            data[:, :, 3] = np.where(background_mask, 0, 255)
            
            # Create output image
            output_image = Image.fromarray(data, 'RGBA')
            
            # Save with transparent background
            output_image.save(output_path, format='PNG')
            
        except Exception as e:
            # Fallback to rembg if simple white removal fails
            try:
                from rembg import remove
                from PIL import Image
                
                input_image = Image.open(input_path)
                output_image = remove(input_image, session=self._get_rembg_session())
                output_image.save(output_path, format='PNG')
            except Exception as e2:
                # If all fails, just copy the original
                import shutil
                shutil.copy(input_path, output_path)
                print(f"⚠️  Background removal failed for {input_path.name}: {e2}")
    
    def generate_all(self, ingredients: List[str], force: bool = False, max_workers: int = MAX_WORKERS):
        """
        Generate icons for all ingredients in parallel.
        
        Args:
            ingredients: List of ingredient names
            force: Force regeneration even if files exist
            max_workers: Number of parallel workers
        """
        global completed_count, total_count
        completed_count = 0
        total_count = len(ingredients)
        
        print(f"\n🎨 Generating {total_count} ingredient icons with {max_workers} parallel workers...")
        print(f"📁 Output directory: {self.output_dir}")
        print("=" * 60)
        
        results = {"success": 0, "skipped": 0, "failed": 0}
        failed_ingredients = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_ingredient = {
                executor.submit(self.generate_icon, ingredient, force): ingredient
                for ingredient in ingredients
            }
            
            # Process results as they complete
            for future in as_completed(future_to_ingredient):
                ingredient = future_to_ingredient[future]
                try:
                    success, message = future.result()
                    print(message)
                    
                    if success:
                        if "Skipped" in message:
                            results["skipped"] += 1
                        else:
                            results["success"] += 1
                    else:
                        results["failed"] += 1
                        failed_ingredients.append(ingredient)
                        
                except Exception as e:
                    print(f"❌ Exception ({ingredient}): {e}")
                    results["failed"] += 1
                    failed_ingredients.append(ingredient)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"✅ Generated: {results['success']}")
        print(f"⏭️  Skipped (already exist): {results['skipped']}")
        print(f"❌ Failed: {results['failed']}")
        
        if failed_ingredients:
            print(f"\n❌ Failed ingredients:")
            for ing in failed_ingredients:
                print(f"   - {ing}")
        
        print(f"\n📁 Final icons saved to: {self.output_dir / 'final'}")


def load_ingredients_from_csv(csv_path: str) -> List[str]:
    """
    Load ingredient names from the first row of the CSV file.
    
    Args:
        csv_path: Path to the recipes_ingredients_matrix.csv file
        
    Returns:
        List of ingredient names
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
    
    # Skip first two columns (recipe_id, recipe_name)
    ingredients = header[2:]
    
    # Clean up ingredient names
    ingredients = [ing.strip() for ing in ingredients if ing.strip()]
    
    return ingredients


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate abstract geometric ingredient icons"
    )
    parser.add_argument(
        "--csv",
        default="recipes_ingredients_matrix.csv",
        help="Path to the ingredients CSV file"
    )
    parser.add_argument(
        "--ingredient",
        help="Generate icon for a single ingredient"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List ingredients without generating"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration even if files exist"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Number of parallel workers (default: {MAX_WORKERS})"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for generated icons"
    )
    
    args = parser.parse_args()
    
    # Handle single ingredient
    if args.ingredient:
        gen = IngredientIconGenerator(output_dir=args.output_dir)
        success, message = gen.generate_icon(args.ingredient, force=args.force)
        print(message)
        return 0 if success else 1
    
    # Load ingredients from CSV
    csv_path = Path(args.csv)
    if not csv_path.exists():
        csv_path = Path(__file__).parent / args.csv
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {args.csv}")
        return 1
    
    ingredients = load_ingredients_from_csv(csv_path)
    
    if args.dry_run:
        print(f"\n📋 Found {len(ingredients)} ingredients:")
        print("=" * 60)
        for i, ing in enumerate(ingredients, 1):
            print(f"  {i:3}. {ing}")
        print("=" * 60)
        print(f"\n💡 Run without --dry-run to generate icons")
        return 0
    
    # Generate all icons
    gen = IngredientIconGenerator(output_dir=args.output_dir)
    gen.generate_all(ingredients, force=args.force, max_workers=args.workers)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
