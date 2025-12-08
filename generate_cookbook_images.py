#!/usr/bin/env python3
"""
Cookbook Image Generator
========================
High-quality 8x8 inch square images for cookbook pages.
Generates professional food photography style images for ingredients and final dishes.

Uses Google Gemini 3 Pro Image generation with intelligent color/appearance
analysis based on actual ingredients and their quantities.

Usage:
    from generate_cookbook_images import CookbookImageGenerator
    
    gen = CookbookImageGenerator()
    
    # Generate dish image with accurate colors from ingredients
    gen.generate_dish_image(
        dish_name="Mhamsa",
        description="Tunisian pearl couscous in tomato stew",
        ingredients=["2 tbsp sweet paprika", "1 tomato", "1 cup couscous"],
        output_path="mhamsa_dish.png"
    )
    
    # Generate ingredients image
    gen.generate_ingredients_image(
        dish_name="Mhamsa",
        ingredients=["semolina pearls", "tomato", "onion", "paprika"],
        output_path="mhamsa_ingredients.png"
    )
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AppearanceAnalyzer:
    """
    Analyzes ingredients to determine accurate dish appearance,
    color, and texture for realistic image generation.
    """
    
    # Color-influencing ingredients with their visual effects
    # Format: (color_description, intensity_multiplier)
    COLOR_INGREDIENTS = {
        # Red/Orange spectrum
        'paprika': ('warm orange-red', 1.5),
        'sweet paprika': ('warm orange-red', 1.5),
        'hot paprika': ('deep rusty red', 1.8),
        'tomato': ('tomato red', 1.0),
        'tomatoes': ('tomato red', 1.0),
        'tomato paste': ('deep concentrated red', 2.5),
        'tomato sauce': ('rich red', 1.8),
        'harissa': ('fiery deep red', 2.0),
        'red pepper': ('bright red', 1.2),
        'bell pepper': ('vibrant red/yellow/green', 0.8),
        'cayenne': ('reddish-brown heat', 1.0),
        
        # Yellow/Golden spectrum
        'turmeric': ('golden yellow', 2.0),
        'saffron': ('luxurious golden-orange', 2.5),
        'cumin': ('earthy tan-brown', 0.8),
        'curry': ('warm golden-yellow', 1.8),
        'egg': ('golden yellow', 1.0),
        'eggs': ('golden yellow', 1.0),
        'olive oil': ('golden sheen', 0.5),
        
        # Green spectrum
        'parsley': ('fresh green flecks', 0.6),
        'cilantro': ('bright green herbs', 0.6),
        'coriander': ('fresh green', 0.5),
        'mint': ('bright green accents', 0.5),
        'spinach': ('deep green', 1.5),
        'zucchini': ('pale green', 0.8),
        'peas': ('bright green dots', 0.7),
        'green beans': ('vibrant green', 1.0),
        
        # Brown spectrum
        'cinnamon': ('warm brown tones', 0.6),
        'meat': ('rich brown', 1.2),
        'beef': ('deep brown', 1.3),
        'lamb': ('rich reddish-brown', 1.2),
        'chicken': ('golden-brown', 1.0),
        'onion': ('caramelized golden-brown', 0.8),
        'onions': ('caramelized golden-brown', 0.8),
        'fried onion': ('deep golden-brown', 1.2),
        
        # White/Cream spectrum
        'cream': ('creamy white', 0.8),
        'milk': ('milky white', 0.6),
        'yogurt': ('creamy white', 0.7),
        'tahini': ('beige-cream', 0.8),
        'semolina': ('pale golden', 0.5),
        'couscous': ('pale golden grains', 0.6),
        'mhamsa': ('toasted golden pearls', 0.7),
        'rice': ('white/pale', 0.4),
        'potato': ('creamy pale', 0.5),
        'potatoes': ('creamy pale', 0.5),
        'chickpeas': ('beige-tan', 0.6),
        
        # Dark spectrum
        'black pepper': ('dark specks', 0.3),
        'olives': ('dark purple-black', 0.7),
        'raisins': ('dark brown accents', 0.5),
        'dates': ('dark caramel brown', 0.6),
    }
    
    # Liquid bases that affect overall dish appearance
    LIQUID_BASES = {
        'tomato': 'red tomato-based sauce',
        'water': 'clear light broth',
        'broth': 'golden clear broth',
        'stock': 'rich golden stock',
        'olive oil': 'glistening oil coating',
        'cream': 'creamy white sauce',
        'milk': 'milky white liquid',
    }
    
    # Quantity indicators for intensity
    QUANTITY_PATTERNS = {
        'large': 1.5,
        'generous': 1.5,
        'heaping': 1.4,
        '2': 1.5,
        '3': 2.0,
        '4': 2.5,
        'cup': 1.5,
        'cups': 2.0,
        'tbsp': 1.0,
        'tablespoon': 1.0,
        'tsp': 0.5,
        'teaspoon': 0.5,
        'pinch': 0.2,
        'dash': 0.3,
        'small': 0.6,
        'little': 0.4,
    }
    
    @classmethod
    def analyze_ingredients(cls, ingredients: List[str]) -> Dict:
        """
        Analyze a list of ingredients to determine visual appearance.
        
        Args:
            ingredients: List of ingredient strings with quantities
            
        Returns:
            Dict with color_description, dominant_colors, texture_notes
        """
        # Use dict to track best intensity per color (avoid duplicates)
        color_intensities: Dict[str, float] = {}
        liquid_base = None
        
        for ingredient in ingredients:
            ing_lower = ingredient.lower()
            
            # Check for quantity multipliers
            quantity_mult = 1.0
            for pattern, mult in cls.QUANTITY_PATTERNS.items():
                if pattern in ing_lower:
                    quantity_mult = max(quantity_mult, mult)
            
            # Track which ingredients matched to avoid double-counting
            # e.g., "sweet paprika" should only match once, not for both "sweet paprika" and "paprika"
            matched_keys = set()
            
            # Check for color-influencing ingredients (longer keys first for specificity)
            sorted_keys = sorted(cls.COLOR_INGREDIENTS.keys(), key=len, reverse=True)
            for key in sorted_keys:
                if key in ing_lower:
                    # Skip if a more specific key already matched
                    if any(key in mk or mk in key for mk in matched_keys if mk != key):
                        continue
                    
                    matched_keys.add(key)
                    color, intensity = cls.COLOR_INGREDIENTS[key]
                    final_intensity = intensity * quantity_mult
                    
                    # Keep the highest intensity for each color
                    if color not in color_intensities or final_intensity > color_intensities[color]:
                        color_intensities[color] = final_intensity
            
            # Check for liquid bases
            for key, description in cls.LIQUID_BASES.items():
                if key in ing_lower:
                    liquid_base = description
        
        # Convert to sorted list
        colors_found = sorted(
            [(color, intensity) for color, intensity in color_intensities.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Build color description
        if colors_found:
            dominant = colors_found[:3]  # Top 3 unique colors
            color_desc = cls._build_color_description(dominant, liquid_base)
        else:
            color_desc = "natural earthy tones"
        
        return {
            'color_description': color_desc,
            'dominant_colors': [c[0] for c in colors_found[:3]],
            'liquid_base': liquid_base,
            'all_colors': colors_found
        }
    
    @classmethod
    def _build_color_description(
        cls, 
        dominant_colors: List[Tuple[str, float]], 
        liquid_base: Optional[str]
    ) -> str:
        """Build a natural language color description."""
        
        if not dominant_colors:
            return "natural home-cooked appearance"
        
        # Get the primary color
        primary = dominant_colors[0][0]
        primary_intensity = dominant_colors[0][1]
        
        # Build description based on intensity
        # Avoid redundant adjectives if color already contains them
        color_has_adjective = any(
            primary.startswith(adj) 
            for adj in ['warm', 'rich', 'deep', 'bright', 'vibrant', 'pale', 'dark']
        )
        
        if color_has_adjective:
            # Color already has descriptor, just intensify if needed
            if primary_intensity > 2.0:
                intensity_prefix = "deeply saturated "
            elif primary_intensity > 1.5:
                intensity_prefix = "rich "
            else:
                intensity_prefix = ""
        else:
            if primary_intensity > 2.0:
                intensity_prefix = "deeply saturated "
            elif primary_intensity > 1.5:
                intensity_prefix = "rich "
            elif primary_intensity > 1.0:
                intensity_prefix = "warm "
            else:
                intensity_prefix = "subtle "
        
        desc_parts = [f"{intensity_prefix}{primary}".strip()]
        
        # Add secondary colors
        if len(dominant_colors) > 1:
            secondary = dominant_colors[1][0]
            desc_parts.append(f"with hints of {secondary}")
        
        if len(dominant_colors) > 2:
            tertiary = dominant_colors[2][0]
            desc_parts.append(f"and accents of {tertiary}")
        
        # Add liquid base context
        if liquid_base:
            desc_parts.append(f"in a {liquid_base}")
        
        return " ".join(desc_parts)
    
    @classmethod
    def get_texture_description(cls, ingredients: List[str], cooking_method: str = "") -> str:
        """Analyze ingredients for texture description."""
        textures = []
        
        cooking_lower = cooking_method.lower()
        
        # Cooking method textures
        if 'fry' in cooking_lower or 'fried' in cooking_lower:
            textures.append("crispy golden edges")
        if 'stew' in cooking_lower or 'simmer' in cooking_lower:
            textures.append("tender slow-cooked")
        if 'bake' in cooking_lower or 'roast' in cooking_lower:
            textures.append("beautifully caramelized")
        if 'boil' in cooking_lower:
            textures.append("soft and tender")
        
        # Ingredient-based textures
        for ing in ingredients:
            ing_lower = ing.lower()
            if 'couscous' in ing_lower or 'mhamsa' in ing_lower:
                textures.append("fluffy pearled grains")
            if 'meat' in ing_lower or 'lamb' in ing_lower or 'beef' in ing_lower:
                textures.append("succulent braised meat")
            if 'crisp' in ing_lower or 'crunch' in ing_lower:
                textures.append("satisfying crunch")
        
        return ", ".join(textures) if textures else "appetizing home-cooked texture"


class CookbookImageGenerator:
    """
    Generates high-quality cookbook images using Gemini 3 Pro Image.
    
    All images are 1:1 square aspect ratio at 2K resolution,
    optimized for 8x8 inch print at 300dpi.
    """
    
    # Image settings for print cookbook
    ASPECT_RATIO = "1:1"  # Square for 8x8 inch
    RESOLUTION = "2K"     # High quality for print
    MODEL = "gemini-3-pro-image-preview"
    
    # Style prompts for consistent cookbook aesthetic
    DISH_STYLE = """Professional food photography, top-down or 45-degree angle view, 
    natural soft lighting from window, shallow depth of field, 
    rustic ceramic plate on weathered wooden table, 
    Mediterranean color palette, appetizing and inviting,
    styled with fresh herbs and olive oil drizzle,
    high-end cookbook quality, 8K detail, photorealistic"""
    
    INGREDIENTS_STYLE = """Professional food photography, overhead flat lay composition,
    fresh raw ingredients arranged artistically on rustic wooden surface,
    soft natural window lighting, Mediterranean color palette,
    cookware and linens as subtle props, cookbook quality,
    vibrant colors, 8K detail, photorealistic"""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the image generator.
        
        Args:
            output_dir: Directory to save generated images. 
                       Defaults to data/images/generated
        """
        self._client = None
        self._genai = None
        self._types = None
        
        # Set output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent / "data" / "images" / "generated"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
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
    
    def generate_dish_image(
        self,
        dish_name: str,
        description: str,
        ingredients: Optional[List[str]] = None,
        output_path: Optional[str] = None,
        cultural_context: str = "Tunisian Jewish Djerban",
        cooking_method: str = "",
        additional_styling: str = ""
    ) -> Path:
        """
        Generate a high-quality image of a finished dish with accurate colors.
        
        Args:
            dish_name: Name of the dish (e.g., "Mhamsa", "Couscous")
            description: Brief description of the dish
            ingredients: List of ingredients with quantities for color accuracy
            cultural_context: Cultural origin for authentic styling
            cooking_method: How it's cooked (fried, stewed, etc.)
            output_path: Optional custom output path
            additional_styling: Extra styling instructions
            
        Returns:
            Path to the saved image
        """
        client = self._get_client()
        
        # Analyze ingredients for accurate appearance
        appearance_desc = ""
        if ingredients:
            analysis = AppearanceAnalyzer.analyze_ingredients(ingredients)
            color_desc = analysis['color_description']
            texture_desc = AppearanceAnalyzer.get_texture_description(
                ingredients, cooking_method
            )
            
            appearance_desc = f"""
CRITICAL COLOR AND APPEARANCE REQUIREMENTS (based on actual ingredients):
- The dish MUST have {color_desc} coloring
- Texture should show {texture_desc}
- These colors come from the actual spices and ingredients used:
  {', '.join(ingredients[:8])}
  
Do NOT make the dish look generic. Match the specific color profile above."""
        
        # Build the prompt
        prompt = f"""Create a stunning photograph of {dish_name}, 
a traditional {cultural_context} dish: {description}
{appearance_desc}

Style requirements:
{self.DISH_STYLE}

{additional_styling}

The dish should look authentic, homemade yet beautifully presented,
as if photographed for a high-end heritage cookbook."""

        # Determine output path
        if output_path:
            save_path = Path(output_path)
        else:
            safe_name = dish_name.lower().replace(" ", "_").replace("'", "")
            save_path = self.output_dir / f"{safe_name}_dish.png"
        
        return self._generate_and_save(prompt, save_path)
    
    def generate_ingredients_image(
        self,
        dish_name: str,
        ingredients: List[str],
        output_path: Optional[str] = None,
        additional_styling: str = ""
    ) -> Path:
        """
        Generate a flat-lay image of ingredients for a dish.
        
        Args:
            dish_name: Name of the dish
            ingredients: List of ingredient names
            output_path: Optional custom output path
            additional_styling: Extra styling instructions
            
        Returns:
            Path to the saved image
        """
        client = self._get_client()
        
        # Format ingredients list
        ingredients_text = ", ".join(ingredients)
        
        # Build the prompt
        prompt = f"""Create a beautiful flat-lay photograph showing the raw ingredients 
for making {dish_name}:

Ingredients to show: {ingredients_text}

Style requirements:
{self.INGREDIENTS_STYLE}

{additional_styling}

Arrange ingredients in an artistic, balanced composition
that showcases the fresh, quality ingredients used in this traditional recipe."""

        # Determine output path
        if output_path:
            save_path = Path(output_path)
        else:
            safe_name = dish_name.lower().replace(" ", "_").replace("'", "")
            save_path = self.output_dir / f"{safe_name}_ingredients.png"
        
        return self._generate_and_save(prompt, save_path)
    
    def generate_custom_image(
        self,
        prompt: str,
        output_path: str,
        add_cookbook_style: bool = True
    ) -> Path:
        """
        Generate a custom image with optional cookbook styling.
        
        Args:
            prompt: The generation prompt
            output_path: Path to save the image
            add_cookbook_style: Whether to append cookbook styling
            
        Returns:
            Path to the saved image
        """
        if add_cookbook_style:
            full_prompt = f"""{prompt}

Additional style: Professional food photography, natural lighting,
high-end cookbook quality, 8K detail, photorealistic."""
        else:
            full_prompt = prompt
        
        return self._generate_and_save(full_prompt, Path(output_path))
    
    def _generate_and_save(self, prompt: str, save_path: Path) -> Path:
        """
        Internal method to generate image and save it.
        
        Args:
            prompt: The generation prompt
            save_path: Path to save the image
            
        Returns:
            Path to the saved image
        """
        client = self._get_client()
        types = self._types
        
        print(f"🎨 Generating image: {save_path.name}")
        print(f"   Prompt preview: {prompt[:100]}...")
        
        try:
            response = client.models.generate_content(
                model=self.MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=self.ASPECT_RATIO,
                        image_size=self.RESOLUTION
                    ),
                )
            )
            
            # Process response
            image_saved = False
            for part in response.parts:
                if part.text is not None:
                    print(f"   Model note: {part.text[:100]}...")
                elif image := part.as_image():
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(str(save_path))
                    image_saved = True
                    print(f"✅ Image saved: {save_path}")
            
            if not image_saved:
                raise RuntimeError("No image was generated in the response")
            
            return save_path
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            raise
    
    def generate_recipe_images(
        self,
        recipe_data: dict,
        generate_dish: bool = True,
        generate_ingredients: bool = True
    ) -> dict:
        """
        Generate all images for a recipe from its JSON data.
        Uses ingredients to determine accurate dish colors.
        
        Args:
            recipe_data: Recipe dictionary with 'name', 'description', 'ingredients'
            generate_dish: Whether to generate the dish image
            generate_ingredients: Whether to generate ingredients image
            
        Returns:
            Dict with paths to generated images
        """
        results = {}
        
        # Get English name and description
        name = recipe_data.get('name', {})
        if isinstance(name, dict):
            dish_name = name.get('en', name.get('he', 'dish'))
        else:
            dish_name = str(name)
        
        description = recipe_data.get('description', {})
        if isinstance(description, dict):
            dish_desc = description.get('en', '')
        else:
            dish_desc = str(description)
        
        # Get ingredients list (English)
        ingredients = recipe_data.get('ingredients', {})
        if isinstance(ingredients, dict):
            ingredients_list = ingredients.get('en', [])
        else:
            ingredients_list = ingredients if isinstance(ingredients, list) else []
        
        # Try to detect cooking method from steps/instructions
        cooking_method = self._detect_cooking_method(recipe_data)
        
        recipe_id = recipe_data.get('id', dish_name.lower().replace(" ", "_"))
        
        # Generate dish image with ingredient-accurate colors
        if generate_dish:
            dish_path = self.output_dir / f"{recipe_id}_dish.png"
            results['dish'] = self.generate_dish_image(
                dish_name=dish_name,
                description=dish_desc,
                ingredients=ingredients_list,
                cooking_method=cooking_method,
                output_path=str(dish_path)
            )
        
        # Generate ingredients image
        if generate_ingredients and ingredients_list:
            ing_path = self.output_dir / f"{recipe_id}_ingredients.png"
            results['ingredients'] = self.generate_ingredients_image(
                dish_name=dish_name,
                ingredients=ingredients_list,
                output_path=str(ing_path)
            )
        
        return results
    
    def _detect_cooking_method(self, recipe_data: dict) -> str:
        """Extract cooking method from recipe steps if available."""
        cooking_keywords = []
        
        # Check variants for steps
        variants = recipe_data.get('variants', [])
        for variant in variants:
            steps = variant.get('steps', {})
            if isinstance(steps, dict):
                en_steps = steps.get('en', [])
            else:
                en_steps = steps if isinstance(steps, list) else []
            
            for step in en_steps:
                step_lower = step.lower()
                if 'fry' in step_lower or 'sauté' in step_lower:
                    cooking_keywords.append('fried')
                if 'simmer' in step_lower or 'stew' in step_lower:
                    cooking_keywords.append('stewed')
                if 'bake' in step_lower or 'roast' in step_lower:
                    cooking_keywords.append('baked')
                if 'boil' in step_lower:
                    cooking_keywords.append('boiled')
        
        # Also check direct steps field
        steps = recipe_data.get('steps', {})
        if isinstance(steps, dict):
            en_steps = steps.get('en', [])
        elif isinstance(steps, list):
            en_steps = steps
        else:
            en_steps = []
            
        for step in en_steps:
            if isinstance(step, str):
                step_lower = step.lower()
                if 'fry' in step_lower or 'sauté' in step_lower:
                    cooking_keywords.append('fried')
                if 'simmer' in step_lower or 'stew' in step_lower:
                    cooking_keywords.append('stewed')
        
        return ' '.join(set(cooking_keywords))


def analyze_recipe_colors(recipe_path: str) -> None:
    """
    Preview the color analysis for a recipe without generating an image.
    Useful for debugging and understanding color decisions.
    """
    import json
    
    with open(recipe_path, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    # Get ingredients
    ingredients = recipe.get('ingredients', {})
    if isinstance(ingredients, dict):
        ingredients_list = ingredients.get('en', [])
    else:
        ingredients_list = ingredients if isinstance(ingredients, list) else []
    
    print(f"\n🔍 Color Analysis for: {recipe.get('name', {}).get('en', 'Unknown')}")
    print("=" * 60)
    print(f"\nIngredients analyzed:")
    for ing in ingredients_list:
        print(f"  • {ing}")
    
    analysis = AppearanceAnalyzer.analyze_ingredients(ingredients_list)
    
    print(f"\n🎨 Color Analysis Results:")
    print(f"   Primary description: {analysis['color_description']}")
    print(f"   Dominant colors: {', '.join(analysis['dominant_colors']) if analysis['dominant_colors'] else 'None detected'}")
    print(f"   Liquid base: {analysis['liquid_base'] or 'Not detected'}")
    
    if analysis['all_colors']:
        print(f"\n   All detected colors (by intensity):")
        for color, intensity in analysis['all_colors'][:8]:
            bar = "█" * int(intensity * 5)
            print(f"      {color:<30} {bar} ({intensity:.1f})")
    
    print()


def main():
    """Demo and testing entry point."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(
        description="Generate cookbook images using Gemini 3 Pro"
    )
    parser.add_argument(
        "--dish",
        help="Generate a dish image with this name"
    )
    parser.add_argument(
        "--description",
        default="A traditional Mediterranean dish",
        help="Description of the dish"
    )
    parser.add_argument(
        "--ingredients",
        nargs="+",
        help="List of ingredients (used for both flat-lay and color analysis)"
    )
    parser.add_argument(
        "--recipe-json",
        help="Path to recipe JSON file to generate images from"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for images"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a test generation with sample ingredients"
    )
    parser.add_argument(
        "--analyze",
        help="Analyze colors from recipe JSON without generating (preview mode)"
    )
    parser.add_argument(
        "--dish-only",
        action="store_true",
        help="Only generate dish image, skip ingredients"
    )
    parser.add_argument(
        "--ingredients-only",
        action="store_true",
        help="Only generate ingredients image, skip dish"
    )
    
    args = parser.parse_args()
    
    # Analyze mode - preview colors without generating
    if args.analyze:
        analyze_recipe_colors(args.analyze)
        return
    
    # Initialize generator
    gen = CookbookImageGenerator(output_dir=args.output_dir)
    
    if args.test:
        print("🧪 Running test generation with ingredient-based colors...")
        
        # Test ingredients that should produce specific colors
        test_ingredients = [
            "2 tbsp sweet paprika",
            "1 large tomato, chopped",
            "1 small onion, diced",
            "1 cup mhamsa (pearl couscous)",
            "1 tsp cumin",
            "black pepper to taste",
            "2 cups water"
        ]
        
        # Show color analysis first
        analysis = AppearanceAnalyzer.analyze_ingredients(test_ingredients)
        print(f"\n🎨 Detected colors: {analysis['color_description']}")
        print(f"   Dominant: {', '.join(analysis['dominant_colors'])}\n")
        
        result = gen.generate_dish_image(
            dish_name="Mhamsa",
            description="Tunisian pearl couscous in a rich tomato stew with vegetables",
            ingredients=test_ingredients,
            cooking_method="stewed simmered",
            output_path=str(gen.output_dir / "test_mhamsa_accurate.png")
        )
        print(f"✅ Test complete: {result}")
        return
    
    if args.recipe_json:
        # Load recipe from JSON and generate images
        with open(args.recipe_json, 'r', encoding='utf-8') as f:
            recipe_data = json.load(f)
        
        # Show color analysis
        ingredients = recipe_data.get('ingredients', {})
        if isinstance(ingredients, dict):
            ing_list = ingredients.get('en', [])
        else:
            ing_list = ingredients if isinstance(ingredients, list) else []
        
        if ing_list:
            analysis = AppearanceAnalyzer.analyze_ingredients(ing_list)
            print(f"\n🎨 Detected colors: {analysis['color_description']}")
        
        results = gen.generate_recipe_images(
            recipe_data,
            generate_dish=not args.ingredients_only,
            generate_ingredients=not args.dish_only
        )
        print(f"\n✅ Generated {len(results)} images:")
        for key, path in results.items():
            print(f"   {key}: {path}")
        return
    
    if args.dish:
        # Generate dish image with optional ingredients for color accuracy
        if args.ingredients:
            analysis = AppearanceAnalyzer.analyze_ingredients(args.ingredients)
            print(f"🎨 Detected colors: {analysis['color_description']}")
        
        result = gen.generate_dish_image(
            dish_name=args.dish,
            description=args.description,
            ingredients=args.ingredients
        )
        print(f"✅ Generated dish image: {result}")
    
    if args.ingredients and not args.dish_only:
        # Generate ingredients image
        dish_name = args.dish or "Recipe"
        result = gen.generate_ingredients_image(
            dish_name=dish_name,
            ingredients=args.ingredients
        )
        print(f"✅ Generated ingredients image: {result}")
    
    if not any([args.dish, args.ingredients, args.recipe_json, args.test, args.analyze]):
        parser.print_help()


if __name__ == "__main__":
    main()

