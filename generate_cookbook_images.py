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
    # NOTE: Longer/more specific keys should be checked first (sorted by length)
    COLOR_INGREDIENTS = {
        # Red/Orange spectrum - Spices
        'paprika': ('warm orange-red', 1.5),
        'sweet paprika': ('warm orange-red', 1.5),
        'hot paprika': ('deep rusty red', 1.8),
        'smoked paprika': ('smoky brick red', 1.6),
        'cayenne pepper': ('reddish heat specks', 0.8),
        'cayenne': ('reddish heat specks', 0.8),
        'chili flakes': ('red pepper flakes', 0.7),
        'red pepper flakes': ('red pepper flakes', 0.7),
        
        # Red/Orange spectrum - Tomatoes
        'tomato': ('tomato red', 1.0),
        'tomatoes': ('tomato red', 1.0),
        'cherry tomatoes': ('bright red cherry tomatoes', 1.2),
        'tomato paste': ('deep concentrated red', 2.5),
        'tomato sauce': ('rich red', 1.8),
        'sun-dried tomatoes': ('deep burgundy red', 1.4),
        
        # Red/Orange spectrum - Hot peppers/chilies
        'harissa': ('fiery deep red', 2.0),
        'hot pepper': ('bright red/green chili', 1.0),
        'chili pepper': ('bright red/green chili', 1.0),
        'chili': ('bright red/green chili', 0.8),
        'jalapeño': ('bright green chili', 0.9),
        'jalapeno': ('bright green chili', 0.9),
        'serrano': ('bright green chili', 0.9),
        'red chili': ('bright red chili', 1.2),
        'green chili': ('bright green chili', 1.0),
        'dried chili': ('dark red dried chili', 0.8),
        'long pepper': ('long thin chili', 0.9),
        'hot green pepper': ('long bright green chili', 1.0),
        'hot red pepper': ('long bright red chili', 1.2),
        
        # Bell peppers (sweet peppers) - distinct from hot peppers
        'bell pepper': ('chunky sweet pepper pieces', 0.8),
        'red bell pepper': ('vibrant red bell pepper chunks', 1.2),
        'green bell pepper': ('bright green bell pepper chunks', 1.0),
        'yellow bell pepper': ('sunny yellow bell pepper chunks', 1.0),
        'orange bell pepper': ('orange bell pepper chunks', 1.0),
        'sweet pepper': ('colorful sweet pepper chunks', 0.9),
        'roasted pepper': ('charred roasted pepper strips', 1.0),
        'roasted red pepper': ('charred red pepper strips', 1.2),
        
        # Yellow/Golden spectrum
        'turmeric': ('golden yellow', 2.0),
        'saffron': ('luxurious golden-orange', 2.5),
        'cumin': ('earthy tan-brown', 0.8),
        'ground cumin': ('earthy tan-brown', 0.8),
        'curry': ('warm golden-yellow', 1.8),
        'curry powder': ('warm golden-yellow', 1.8),
        'egg': ('golden yellow', 1.0),
        'eggs': ('golden yellow', 1.0),
        'egg yolk': ('rich golden yellow', 1.3),
        'olive oil': ('golden sheen', 0.5),
        'lemon': ('bright yellow citrus', 0.6),
        'lemon juice': ('no visible color', 0.1),
        
        # Green spectrum - Herbs
        'parsley': ('fresh green herb flecks', 0.6),
        'fresh parsley': ('bright green herb flecks', 0.7),
        'cilantro': ('bright green herb leaves', 0.6),
        'fresh cilantro': ('bright green herb leaves', 0.7),
        'coriander': ('fresh green', 0.5),
        'fresh coriander': ('bright green leaves', 0.6),
        'mint': ('bright green mint leaves', 0.5),
        'fresh mint': ('bright green mint leaves', 0.6),
        'basil': ('deep green basil leaves', 0.6),
        'dill': ('feathery green dill', 0.5),
        
        # Green spectrum - Vegetables
        'spinach': ('deep green leaves', 1.5),
        'zucchini': ('pale green with white flesh', 0.8),
        'peas': ('bright green dots', 0.7),
        'green beans': ('vibrant green beans', 1.0),
        'green onion': ('green and white scallion', 0.6),
        'scallion': ('green and white scallion', 0.6),
        'celery': ('pale green celery', 0.5),
        'cucumber': ('green with pale interior', 0.6),
        'asparagus': ('green asparagus spears', 0.8),
        'broccoli': ('dark green florets', 1.0),
        'cabbage': ('pale green leaves', 0.6),
        'artichoke': ('pale green artichoke', 0.7),
        
        # Brown spectrum - Spices
        'cinnamon': ('warm brown tones', 0.6),
        'ground cinnamon': ('warm brown powder', 0.6),
        'cinnamon stick': ('brown cinnamon sticks', 0.5),
        'allspice': ('brown spice specks', 0.4),
        'nutmeg': ('brown specks', 0.3),
        'cardamom': ('brown-green pods', 0.4),
        'cloves': ('dark brown cloves', 0.4),
        'caraway': ('brown caraway seeds', 0.4),
        
        # Brown spectrum - Proteins (VEGAN COOKBOOK - all proteins are plant-based)
        'meat': ('rich brown seitan pieces', 1.2),
        'beef': ('deep brown seitan', 1.3),
        'ground beef': ('crumbly brown TVP/seitan crumbles', 1.2),
        'lamb': ('rich brown seitan pieces', 1.2),
        'ground lamb': ('crumbly brown TVP crumbles', 1.2),
        'chicken': ('golden-brown tofu or seitan pieces', 1.0),
        'chicken breast': ('sliced white tofu or seitan', 0.9),
        'chicken thigh': ('golden-brown seitan pieces', 1.1),
        'fish': ('white tofu or plant-based fish', 0.8),
        'salmon': ('orange-pink plant-based fish', 0.9),
        'tuna': ('plant-based tuna', 0.7),
        
        # Vegan proteins (explicit)
        'tofu': ('white/golden tofu cubes', 0.8),
        'firm tofu': ('golden-brown seared tofu', 0.9),
        'seitan': ('brown chewy seitan pieces', 1.1),
        'tempeh': ('brown tempeh slices', 1.0),
        'tvp': ('brown TVP crumbles', 0.9),
        'textured vegetable protein': ('brown TVP crumbles', 0.9),
        'plant-based': ('plant-based protein', 0.8),
        'vegan meat': ('brown plant-based meat', 1.0),
        'beyond': ('plant-based meat crumbles', 1.0),
        'impossible': ('plant-based meat', 1.0),
        
        # Brown spectrum - Aromatics
        'onion': ('caramelized golden-brown', 0.8),
        'onions': ('caramelized golden-brown', 0.8),
        'fried onion': ('deep golden-brown crispy onion', 1.2),
        'caramelized onion': ('dark golden caramelized onion', 1.3),
        'shallot': ('golden-brown shallot', 0.7),
        'garlic': ('golden garlic bits', 0.5),
        'roasted garlic': ('golden roasted garlic', 0.6),
        
        # White/Cream spectrum
        'cream': ('creamy white', 0.8),
        'heavy cream': ('rich creamy white', 0.9),
        'milk': ('milky white', 0.6),
        'yogurt': ('creamy white', 0.7),
        'tahini': ('beige-cream tahini', 0.8),
        'semolina': ('pale golden', 0.5),
        'couscous': ('pale golden grains', 0.6),
        'mhamsa': ('toasted golden pearls', 0.7),
        'rice': ('white/pale rice', 0.4),
        'white rice': ('white rice grains', 0.4),
        'basmati': ('long white rice grains', 0.4),
        'potato': ('creamy pale potato', 0.5),
        'potatoes': ('creamy pale potato', 0.5),
        'mashed potato': ('creamy white mash', 0.6),
        'chickpeas': ('beige-tan chickpeas', 0.6),
        'white beans': ('creamy white beans', 0.5),
        'cannellini': ('creamy white beans', 0.5),
        'cauliflower': ('white cauliflower florets', 0.5),
        'tofu': ('white tofu cubes', 0.5),
        'feta': ('white crumbly cheese', 0.6),
        'mozzarella': ('white melted cheese', 0.6),
        
        # Dark spectrum - Spices
        'black pepper': ('tiny dark specks', 0.3),
        'ground black pepper': ('tiny dark specks', 0.3),
        'whole black pepper': ('black peppercorns', 0.3),
        'white pepper': ('no visible color', 0.1),
        
        # Dark spectrum - Other
        'olives': ('dark purple-black olives', 0.7),
        'black olives': ('black olives', 0.8),
        'kalamata': ('dark purple kalamata olives', 0.8),
        'green olives': ('green olives', 0.7),
        'raisins': ('dark brown raisins', 0.5),
        'dates': ('dark caramel brown dates', 0.6),
        'prunes': ('dark purple prunes', 0.5),
        'soy sauce': ('dark brown sauce', 0.6),
        'balsamic': ('dark brown glaze', 0.5),
        
        # Orange/Root vegetables
        'carrot': ('bright orange carrot', 1.0),
        'carrots': ('bright orange carrots', 1.0),
        'sweet potato': ('orange sweet potato', 1.0),
        'butternut squash': ('orange squash', 0.9),
        'pumpkin': ('orange pumpkin', 1.0),
        
        # Purple/Red vegetables
        'eggplant': ('dark purple eggplant', 0.8),
        'aubergine': ('dark purple eggplant', 0.8),
        'red cabbage': ('purple-red cabbage', 0.9),
        'beet': ('deep magenta beet', 1.5),
        'beetroot': ('deep magenta beet', 1.5),
        'red onion': ('purple-red onion rings', 0.8),
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


class DishResearcher:
    """
    Researches dish visual appearance using Perplexity API to improve
    image generation accuracy. Caches results to avoid repeated API calls.
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize the researcher.
        
        Args:
            cache_dir: Directory for caching research results.
                      Defaults to data/image_research_cache
        """
        self._client = None
        
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(__file__).parent / "data" / "image_research_cache"
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_client(self):
        """Lazy load the Perplexity client."""
        if self._client is None:
            try:
                from perplexipy import PerplexityClient
            except ImportError:
                print("❌ PerplexiPy package not installed.")
                print("Install with: pip install perplexipy")
                sys.exit(1)
            
            api_key = os.getenv('PERPLEXITY_API_KEY')
            if not api_key or api_key == 'your_perplexity_api_key_here':
                raise ValueError(
                    "PERPLEXITY_API_KEY not found in environment. "
                    "Please set it in your .env file."
                )
            
            self._client = PerplexityClient(key=api_key)
        
        return self._client
    
    def _get_cache_path(self, dish_name: str) -> Path:
        """Get the cache file path for a dish."""
        safe_name = dish_name.lower().replace(" ", "_").replace("'", "").replace("/", "_")
        return self.cache_dir / f"{safe_name}.json"
    
    def _load_cache(self, dish_name: str) -> Optional[Dict]:
        """Load cached research if available."""
        cache_path = self._get_cache_path(dish_name)
        if cache_path.exists():
            try:
                import json
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Warning: Could not load cache for {dish_name}: {e}")
        return None
    
    def _save_cache(self, dish_name: str, research: Dict) -> None:
        """Save research to cache."""
        cache_path = self._get_cache_path(dish_name)
        try:
            import json
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(research, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Warning: Could not save cache for {dish_name}: {e}")
    
    def research_dish(self, dish_name: str, description: str = "") -> Dict:
        """
        Research a dish's visual appearance using Perplexity API.
        
        Args:
            dish_name: Name of the dish
            description: Optional description for context
            
        Returns:
            Dict with keys: visual_description, consistency, protein_size,
            serving_style, research_date
        """
        # Check cache first
        cached = self._load_cache(dish_name)
        if cached:
            print(f"📚 Using cached research for {dish_name}")
            return cached
        
        print(f"🔍 Researching visual appearance of {dish_name}...")
        
        # Build research query
        query = f"""What does {dish_name} look like? 
Describe the visual appearance, consistency (soupy/stew/solid), 
serving style (bowl/plate), typical presentation, and size of protein pieces.
Focus on how it appears when served, not just ingredients.
{dish_name} is a Tunisian Jewish Djerban dish. {description}"""
        
        try:
            client = self._get_client()
            response = client.query(query)
            
            # Parse response to extract key information
            research = self._parse_research_response(dish_name, response, description)
            
            # Save to cache
            self._save_cache(dish_name, research)
            
            return research
            
        except Exception as e:
            print(f"⚠️  Research failed for {dish_name}: {e}")
            # Return default research based on description
            return self._default_research(dish_name, description)
    
    def _parse_research_response(self, dish_name: str, response: str, description: str) -> Dict:
        """
        Parse Perplexity response to extract structured research data.
        
        Args:
            dish_name: Name of the dish
            response: Raw response from Perplexity
            description: Original description for fallback
            
        Returns:
            Structured research dict
        """
        from datetime import datetime
        import re
        
        response_lower = response.lower()
        
        # Extract consistency
        consistency = "stew"  # default
        if any(word in response_lower for word in ["soup", "soupy", "broth", "liquid", "soup-like"]):
            consistency = "soupy stew"
        elif any(word in response_lower for word in ["solid", "casserole", "baked", "firm"]):
            consistency = "solid"
        elif any(word in response_lower for word in ["stew", "simmered", "braised"]):
            consistency = "stew"
        
        # Extract serving style
        serving_style = "bowl"  # default
        if "plate" in response_lower or "served on" in response_lower:
            serving_style = "plate"
        elif "bowl" in response_lower or "soup" in response_lower:
            serving_style = "bowl with broth"
        
        # Extract protein size hints
        protein_size = "small pieces"  # default
        if any(word in response_lower for word in ["cubes", "cubed", "diced"]):
            protein_size = "small cubes (1-2cm)"
        elif any(word in response_lower for word in ["chunks", "large pieces"]):
            protein_size = "medium chunks"
        elif any(word in response_lower for word in ["sliced", "strips"]):
            protein_size = "thin slices"
        
        # Create visual description (first 200 chars of response)
        visual_description = response[:300].strip()
        if len(response) > 300:
            visual_description += "..."
        
        return {
            "dish_name": dish_name,
            "visual_description": visual_description,
            "consistency": consistency,
            "protein_size": protein_size,
            "serving_style": serving_style,
            "research_date": datetime.now().strftime("%Y-%m-%d"),
            "raw_response": response[:500]  # Keep first 500 chars for reference
        }
    
    def _default_research(self, dish_name: str, description: str) -> Dict:
        """Generate default research when API call fails."""
        from datetime import datetime
        
        # Infer from description
        desc_lower = description.lower()
        consistency = "stew"
        if "soup" in desc_lower or "broth" in desc_lower:
            consistency = "soupy stew"
        elif "baked" in desc_lower or "casserole" in desc_lower:
            consistency = "solid"
        
        serving_style = "bowl with broth" if "soup" in desc_lower or "broth" in desc_lower else "plate"
        
        return {
            "dish_name": dish_name,
            "visual_description": description[:200] if description else f"{dish_name} dish",
            "consistency": consistency,
            "protein_size": "small pieces",
            "serving_style": serving_style,
            "research_date": datetime.now().strftime("%Y-%m-%d"),
            "raw_response": "",
            "note": "Default research (API call failed)"
        }


class CookbookImageGenerator:
    """
    Generates high-quality cookbook images using Gemini 3 Pro Image.
    
    All images are 1:1 square aspect ratio at 2K resolution,
    optimized for 8x8 inch print at 300dpi.
    
    All photos are set in the same Safed house from the early 1900s.
    """
    
    # Image settings for print cookbook
    ASPECT_RATIO = "1:1"  # Square for 8x8 inch
    RESOLUTION = "2K"     # High quality for print
    MODEL = "gemini-3-pro-image-preview"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THE SAFED HOUSE - Consistent setting for all cookbook images
    # ═══════════════════════════════════════════════════════════════════════════
    # A spacious stone house in Safed (Tzfat), Israel, built in the early 1900s.
    # High ceilings, thick whitewashed walls, touches of Safed light blue.
    # Sturdy but humble furniture - the home of modest, hardworking people.
    # ═══════════════════════════════════════════════════════════════════════════
    
    SAFED_HOUSE_BASE = """
    Setting: A kitchen in an old Safed stone house, early 1900s architecture.
    - Thick whitewashed walls with subtle texture, some showing aged stone beneath
    - Touches of the famous "Safed light blue" (pale sky blue) on window frames or accents
    - High ceilings with deep-set windows letting in soft Mediterranean light
    - Humble but sturdy furniture - worn wood, simple craftsmanship, well-used
    - The feeling of a modest Jewish home, lived-in and loved
    """
    
    # Different surfaces/spots in the house for variety
    SAFED_SURFACES = [
        "a thick wooden table, dark and worn smooth from decades of use, with visible grain",
        "a pale stone countertop near the window, smooth from years of kneading dough",
        "an old wooden cutting board placed on a simple kitchen table",
        "a weathered wooden tray on a faded blue-painted side table",
        "a large ceramic tile surface, cream-colored with hand-painted blue edge patterns",
        "a heavy oak table with turned legs, the wood darkened with age",
        "a simple pine board across two sawhorses, covered with a clean cotton cloth",
        "the cool stone ledge of a deep window alcove",
    ]
    
    # Different lighting conditions (all natural light)
    SAFED_LIGHTING = [
        "soft morning light streaming through a deep-set window, creating gentle shadows",
        "warm afternoon Mediterranean sun filtering through thin cotton curtains",
        "diffused daylight from a high window, even and soft",
        "golden hour light casting long shadows, the warmth of late afternoon",
        "bright midday light softened by the thick stone walls",
        "gentle overcast light, soft and shadowless, from the Galilee sky",
    ]
    
    # Subtle background elements (never the focus, just atmosphere)
    SAFED_BACKGROUND_HINTS = [
        "a glimpse of whitewashed wall with a small blue-framed window",
        "the corner of an old wooden shelf with stacked ceramic bowls",
        "a blur of pale blue painted wood in the background",
        "thick stone wall texture fading into soft focus",
        "a hint of a worn copper pot hanging on the wall",
        "the edge of a simple wooden chair with a faded cushion",
        "a stack of old plates on a shelf, slightly out of focus",
        "a cotton towel draped over the back of a simple chair",
    ]
    
    # Humble props that might appear (used sparingly)
    SAFED_PROPS = [
        "a well-worn wooden spoon",
        "a simple ceramic olive oil cruet",
        "a small brass mortar and pestle, darkened with use",
        "a folded cotton napkin in faded blue and white stripes",
        "a chipped but beloved ceramic bowl",
        "a worn brass serving tray",
        "a simple glass bottle of oil",
        "a small clay pot for salt",
    ]
    
    # Style prompts incorporating the Safed house
    DISH_STYLE = """Professional food photography, photorealistic, 8K detail.
    Shot in an early 1900s Safed stone house kitchen.
    Thick whitewashed walls, high ceilings, touches of famous Safed light blue.
    Humble but sturdy furniture - the home of modest, traditional people.
    Natural Mediterranean light from deep-set windows.
    The food is the hero - styled simply, no elaborate garnishes.
    Top-down or 45-degree angle, shallow depth of field.
    Appetizing, inviting, authentic home cooking."""
    
    INGREDIENTS_STYLE = """Professional food photography, overhead flat lay.
    Shot in an early 1900s Safed stone house kitchen.
    Thick whitewashed walls, subtle Safed light blue accents visible.
    Ingredients arranged on worn wooden surface or pale stone.
    Natural Mediterranean light, soft and diffused.
    Fresh raw ingredients, nothing overly styled or artificial.
    The feeling of preparing a meal in grandmother's kitchen.
    Photorealistic, 8K detail, cookbook quality."""
    
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
        self._researcher = None
        
        # Set output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent / "data" / "images" / "generated"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_researcher(self):
        """Lazy load the dish researcher."""
        if self._researcher is None:
            self._researcher = DishResearcher()
        return self._researcher
    
    def _get_scene_variation(self, seed: Optional[str] = None) -> str:
        """
        Get a unique scene variation for the Safed house setting.
        Uses the dish name as a seed for consistent but varied results.
        
        Args:
            seed: Optional string to seed the selection (e.g., dish name)
            
        Returns:
            Scene description string with specific surface, lighting, and props
        """
        import hashlib
        
        # Use seed to get consistent but varied selections
        if seed:
            # Create a hash from the seed for pseudo-random but reproducible selection
            hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
        else:
            import random
            hash_val = random.randint(0, 1000000)
        
        # Select elements based on hash
        surface = self.SAFED_SURFACES[hash_val % len(self.SAFED_SURFACES)]
        lighting = self.SAFED_LIGHTING[(hash_val >> 4) % len(self.SAFED_LIGHTING)]
        background = self.SAFED_BACKGROUND_HINTS[(hash_val >> 8) % len(self.SAFED_BACKGROUND_HINTS)]
        
        # Only sometimes include a prop (about 60% of images)
        include_prop = (hash_val % 10) < 6
        prop = self.SAFED_PROPS[(hash_val >> 12) % len(self.SAFED_PROPS)] if include_prop else None
        
        scene = f"""
=== SCENE: THE SAFED HOUSE ===
All photos are taken in the same early 1900s Safed stone house.
This specific shot:
- Surface: {surface}
- Lighting: {lighting}
- Background: {background}"""
        
        if prop:
            scene += f"\n- A subtle prop nearby: {prop}"
        
        scene += """

IMPORTANT: Keep the Safed house atmosphere consistent but this exact scene unique.
The house has thick whitewashed stone walls, high ceilings, touches of Safed light blue.
Humble, sturdy furniture. A modest Jewish home, well-loved and lived-in."""
        
        return scene
        
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
        additional_styling: str = "",
        recipe_id: Optional[str] = None
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
        
        # Clean description - remove references to other dishes that might confuse
        clean_desc = self._clean_description(description)
        
        # Detect dish category for appropriate styling
        category = self._detect_dish_category(dish_name, clean_desc, recipe_id)
        category_styling = self._get_category_styling(category)
        
        # Research dish visual appearance
        researcher = self._get_researcher()
        research = researcher.research_dish(dish_name, clean_desc)
        
        # Use provided recipe_id or extract from output_path
        recipe_id_for_corrections = recipe_id
        if not recipe_id_for_corrections and output_path:
            recipe_id_for_corrections = Path(output_path).stem.replace("_dish", "")
        
        # Apply recipe-specific corrections/overrides
        recipe_corrections = self._get_recipe_specific_corrections(dish_name, recipe_id=recipe_id_for_corrections)
        if recipe_corrections:
            # Override research with specific corrections
            for key, value in recipe_corrections.items():
                if key in research and key != "specific_instructions":
                    research[key] = value
        
        # Build research-based visual requirements
        research_section = f"""
=== RESEARCH-BASED VISUAL REQUIREMENTS ===
Based on research of traditional {dish_name}:
- Consistency: This is a {research['consistency']} dish, NOT a {self._get_opposite_consistency(research['consistency'])}
- Protein size: {self._get_protein_guidance(ingredients, research['protein_size'])}
- Serving: {research['serving_style']}
- Visual appearance: {research['visual_description'][:200]}"""
        
        # Add recipe-specific corrections if any
        if recipe_corrections and recipe_corrections.get('specific_instructions'):
            research_section += f"\n\n=== SPECIFIC CORRECTIONS ===\n{recipe_corrections['specific_instructions']}"
        
        # Build ingredient requirements
        ingredient_section = ""
        excluded_section = ""
        
        if ingredients:
            analysis = AppearanceAnalyzer.analyze_ingredients(ingredients)
            color_desc = analysis['color_description']
            texture_desc = AppearanceAnalyzer.get_texture_description(
                ingredients, cooking_method
            )
            
            # Identify main components for explicit inclusion
            main_components = self._identify_main_components(ingredients)
            
            # Identify what should NOT appear (common confusions)
            excluded_items = self._get_exclusions(ingredients)
            
            ingredient_section = f"""
=== EXACT INGREDIENTS (ONLY show these) ===
The dish contains ONLY these ingredients:
{chr(10).join(f'• {ing}' for ing in ingredients)}

Main visible components: {', '.join(main_components)}

=== COLOR REQUIREMENTS ===
Based on the spices and liquids above, the dish MUST show:
- Color: {color_desc}
- Texture: {texture_desc}"""

            if excluded_items:
                excluded_section = f"""

=== DO NOT INCLUDE (not in this recipe) ===
{', '.join(excluded_items)}
These are NOT part of this dish - do not add them!"""
        
        # Get unique scene variation for this dish
        scene_variation = self._get_scene_variation(seed=dish_name)
        
        # Build the prompt
        prompt = f"""Create a photograph of {dish_name}, a {cultural_context} dish.

*** THIS IS A 100% VEGAN COOKBOOK ***
All proteins shown must be plant-based alternatives:
- Any "meat" = seitan or firm tofu pieces
- Any "chicken" = golden tofu or seitan
- Any "fish" = plant-based fish or marinated tofu
- Any "egg" = tofu scramble

Brief description: {clean_desc}
{category_styling}
{research_section}
{ingredient_section}
{excluded_section}

=== DO NOT SHOW ANY ANIMAL PRODUCTS ===
No real meat, chicken, fish, eggs, or dairy. All proteins are plant-based.

{scene_variation}

=== PHOTOGRAPHY STYLE ===
{self.DISH_STYLE}

{additional_styling}

IMPORTANT: Show ONLY the ingredients listed above. Do not add any ingredients 
that are not in the list. The dish should look authentic and homemade.
This is VEGAN food - no animal products whatsoever."""

        # Determine output path
        if output_path:
            save_path = Path(output_path)
        else:
            safe_name = dish_name.lower().replace(" ", "_").replace("'", "")
            save_path = self.output_dir / f"{safe_name}_dish.png"
        
        return self._generate_and_save(prompt, save_path)
    
    def _clean_description(self, description: str) -> str:
        """Remove references to other dishes that might confuse the model."""
        # Remove "similar to X" phrases
        import re
        cleaned = re.sub(r'similar to \w+', '', description, flags=re.IGNORECASE)
        cleaned = re.sub(r'like \w+ but', 'but', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'resembles \w+', '', cleaned, flags=re.IGNORECASE)
        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def _identify_main_components(self, ingredients: List[str]) -> List[str]:
        """Identify the main visible components from ingredients."""
        main_items = []
        
        for ing in ingredients:
            ing_lower = ing.lower()
            component = self._parse_ingredient_component(ing_lower)
            if component:
                main_items.append(component)
        
        return list(set(main_items)) if main_items else ['the ingredients listed']
    
    def _parse_ingredient_component(self, ing_lower: str) -> Optional[str]:
        """
        Parse a single ingredient and return its visual description.
        Handles ambiguous terms like 'pepper' by checking context.
        """
        # Check specific terms first (longer/more specific before generic)
        # Order matters - check most specific first
        
        # === PEPPER disambiguation (critical!) ===
        # Black pepper (ground spice - not visible as main component)
        if 'black pepper' in ing_lower or 'ground pepper' in ing_lower:
            return None  # Not a main visible component
        if 'white pepper' in ing_lower:
            return None  # Not visible
        
        # Bell peppers (sweet, chunky)
        if 'bell pepper' in ing_lower:
            if 'red' in ing_lower:
                return 'red bell pepper chunks'
            elif 'green' in ing_lower:
                return 'green bell pepper chunks'
            elif 'yellow' in ing_lower:
                return 'yellow bell pepper chunks'
            return 'colorful bell pepper chunks'
        
        # Hot peppers / Chilies
        if any(x in ing_lower for x in ['hot pepper', 'chili', 'chilli', 'jalapeño', 'jalapeno', 'serrano']):
            if 'green' in ing_lower or 'jalapeño' in ing_lower or 'jalapeno' in ing_lower:
                return 'green hot chili peppers'
            elif 'red' in ing_lower or 'dried' in ing_lower:
                return 'red hot chili peppers'
            return 'hot chili peppers (red or green)'
        
        # Harissa (paste, not whole pepper)
        if 'harissa' in ing_lower:
            return None  # It's a paste that colors the dish, not visible chunks
        
        # Generic "pepper" - try to determine from context
        if 'pepper' in ing_lower and 'pepper' not in ['paprika']:
            # Check for color hints
            if 'red' in ing_lower and 'flakes' not in ing_lower:
                return 'red peppers'
            elif 'green' in ing_lower:
                return 'green peppers'
            elif 'sweet' in ing_lower:
                return 'sweet pepper pieces'
            elif 'hot' in ing_lower or 'spicy' in ing_lower:
                return 'hot chili peppers'
            # If just "pepper" with quantity like "1 pepper", likely a whole pepper
            elif any(x in ing_lower for x in ['1 ', '2 ', '3 ', 'one ', 'two ']):
                return 'whole peppers (chili or bell)'
            # Otherwise might be black pepper to taste
            return None
        
        # === Other main components ===
        component_map = [
            # Pasta/Grains (check specific before generic)
            ('spaghetti', 'broken spaghetti strands'),
            ('linguine', 'linguine pasta'),
            ('penne', 'penne pasta'),
            ('pasta', 'pasta'),
            ('noodle', 'noodles'),
            ('couscous', 'couscous grains'),
            ('mhamsa', 'pearl couscous (mhamsa)'),
            ('ptitim', 'pearl couscous'),
            ('rice', 'rice grains'),
            ('bulgur', 'bulgur wheat'),
            ('quinoa', 'quinoa'),
            ('bread', 'bread'),
            
            # Proteins - VEGAN ALTERNATIVES (this is a 100% vegan cookbook)
            ('chicken', 'golden tofu or seitan pieces'),
            ('lamb', 'brown seitan pieces'),
            ('beef', 'seitan pieces'),
            ('meat', 'seitan or tofu pieces'),
            ('fish', 'plant-based fish or firm tofu'),
            ('salmon', 'plant-based salmon or marinated tofu'),
            ('tuna', 'plant-based tuna or chickpea mash'),
            ('shrimp', 'plant-based shrimp or king oyster mushroom'),
            ('egg', 'tofu scramble or vegan egg'),
            
            # Explicit vegan proteins
            ('tofu', 'tofu cubes'),
            ('seitan', 'seitan pieces'),
            ('tempeh', 'tempeh slices'),
            ('tvp', 'TVP crumbles'),
            
            # Vegetables
            ('tomato', 'tomato'),
            ('onion', 'onion'),
            ('garlic', None),  # Usually not visible as main component
            ('potato', 'potato pieces'),
            ('carrot', 'carrot pieces'),
            ('zucchini', 'zucchini'),
            ('eggplant', 'eggplant'),
            ('aubergine', 'eggplant'),
            ('spinach', 'spinach leaves'),
            ('chickpea', 'chickpeas'),
            ('bean', 'beans'),
            ('lentil', 'lentils'),
            ('pea', 'peas'),
            ('corn', 'corn kernels'),
            ('mushroom', 'mushrooms'),
            ('olive', 'olives'),
            ('artichoke', 'artichoke hearts'),
            ('cabbage', 'cabbage'),
            ('cauliflower', 'cauliflower'),
            ('broccoli', 'broccoli'),
            ('squash', 'squash'),
            ('pumpkin', 'pumpkin'),
            ('celery', 'celery'),
            ('leek', 'leeks'),
            ('fennel', 'fennel'),
            ('beet', 'beets'),
            ('turnip', 'turnips'),
        ]
        
        for keyword, display in component_map:
            if keyword in ing_lower:
                return display
        
        return None
    
    def _get_exclusions(self, ingredients: List[str]) -> List[str]:
        """
        Identify common ingredients that should NOT appear based on what IS included.
        Prevents model from adding stereotypical ingredients.
        
        NOTE: This is a 100% VEGAN cookbook - always exclude real animal products.
        """
        exclusions = []
        ingredients_lower = ' '.join(ingredients).lower()
        
        # === VEGAN COOKBOOK: Always exclude real animal products ===
        # Even if recipe mentions "chicken" or "meat", we mean vegan alternatives
        exclusions.extend([
            'real meat', 'real chicken', 'real fish', 'real beef', 'real lamb',
            'animal meat', 'animal protein', 'raw meat', 'cooked meat',
            'chicken breast (real)', 'fish fillet (real)',
            'dairy', 'milk', 'cream', 'butter', 'cheese', 'yogurt',
            'real eggs', 'fried eggs', 'poached eggs', 'scrambled eggs',
            'honey',  # Often not vegan
        ])
        
        # === Check for specific pepper types to exclude others ===
        has_bell_pepper = 'bell pepper' in ingredients_lower
        has_hot_pepper = any(x in ingredients_lower for x in ['hot pepper', 'chili', 'jalapeño', 'jalapeno', 'serrano', 'harissa'])
        has_black_pepper = 'black pepper' in ingredients_lower or 'ground pepper' in ingredients_lower
        
        # If only black pepper, exclude visible peppers
        if has_black_pepper and not has_bell_pepper and not has_hot_pepper:
            exclusions.extend(['bell peppers', 'chili peppers', 'hot peppers', 'jalapeños'])
        
        # If no peppers at all mentioned
        if not has_bell_pepper and not has_hot_pepper and not has_black_pepper:
            # Check for generic "pepper" that might mean black pepper
            if 'pepper' in ingredients_lower:
                # Likely black pepper to taste
                exclusions.extend(['bell peppers', 'chili peppers', 'hot peppers'])
            else:
                exclusions.extend(['bell peppers', 'chili peppers', 'black pepper'])
        
        # === Common confusions to exclude ===
        confusion_map = {
            # If no chickpeas mentioned, exclude them (common in Mediterranean)
            'chickpea': ['chickpeas', 'garbanzo beans'],
            # If no couscous/rice, exclude
            'couscous': ['couscous grains'],
            'mhamsa': ['pearl couscous'],
            'rice': ['rice grains'],
            # If no beans
            'bean': ['beans', 'white beans', 'kidney beans'],
            # If no specific vegetables
            'olive': ['olives'],
            'mushroom': ['mushrooms'],
            'corn': ['corn kernels'],
            'pea': ['peas', 'green peas'],
            # Common garnishes that might be added incorrectly
            'parsley': ['parsley garnish'],
            'cilantro': ['cilantro', 'coriander leaves'],
            'lemon': ['lemon slices', 'lemon wedges'],
            'lime': ['lime slices', 'lime wedges'],
            'nut': ['pine nuts', 'almonds', 'walnuts'],
        }
        
        for key, to_exclude in confusion_map.items():
            if key not in ingredients_lower:
                exclusions.extend(to_exclude)
        
        # Remove duplicates and limit
        return list(set(exclusions))[:20]
    
    def _get_opposite_consistency(self, consistency: str) -> str:
        """Get the opposite consistency for contrast in prompt."""
        opposites = {
            "soupy stew": "solid casserole",
            "stew": "dry baked dish",
            "solid": "soupy liquid dish",
            "soup": "solid meal"
        }
        return opposites.get(consistency, "different consistency")
    
    def _detect_dish_category(self, dish_name: str, description: str = "", recipe_id: Optional[str] = None) -> str:
        """
        Detect the category of dish (dessert, main, dressing, bread, etc.)
        to apply appropriate styling.
        
        Returns:
            Category string: "dessert", "dressing", "bread", "main", "appetizer", etc.
        """
        dish_lower = dish_name.lower()
        desc_lower = description.lower()
        combined = f"{dish_lower} {desc_lower}"
        
        # Dessert keywords
        dessert_keywords = [
            'cake', 'cookie', 'crumble', 'biscotti', 'muffin', 'brownie',
            'sufganiyot', 'sfenj', 'sfinj', 'donut', 'doughnut', 'sweet',
            'chocolate', 'honey', 'fudge', 'nougat', 'granola', 'balls',
            'dessert', 'treat', 'pastry', 'pie', 'tart'
        ]
        
        # Dressing/sauce keywords
        dressing_keywords = [
            'dressing', 'sauce', 'dip', 'marinade', 'vinaigrette',
            'caesar', 'tahini', 'mayonnaise', 'aioli'
        ]
        
        # Bread keywords
        bread_keywords = [
            'bread', 'hallah', 'challah', 'khobz', 'sfenj', 'pita',
            'loaf', 'roll', 'bun', 'bagel'
        ]
        
        # Appetizer/salad keywords
        appetizer_keywords = [
            'salad', 'appetizer', 'kemia', 'mezze', 'hummus', 'dip',
            'pickle', 'msayer', 'msiyer'
        ]
        
        # Check categories in order of specificity
        if any(kw in combined for kw in dessert_keywords):
            return "dessert"
        elif any(kw in combined for kw in dressing_keywords):
            return "dressing"
        elif any(kw in combined for kw in bread_keywords):
            return "bread"
        elif any(kw in combined for kw in appetizer_keywords):
            return "appetizer"
        else:
            return "main"
    
    def _get_category_styling(self, category: str) -> str:
        """
        Get category-specific styling instructions for image generation.
        
        Args:
            category: Dish category (dessert, dressing, bread, main, appetizer)
            
        Returns:
            Styling instructions string
        """
        styling_map = {
            "dessert": """=== DESSERT STYLING ===
CRITICAL: This is a DESSERT/SWEET TREAT, NOT a main dish or stew!
- Show on a dessert plate, cake stand, or small serving dish
- Should look sweet, appetizing, and dessert-like
- If it's a cake/cookie: show slices or individual pieces, golden-brown baked appearance
- If it's fried (like sfenj): show golden-brown, dusted with sugar
- NO bowls of liquid, NO stew-like appearance
- Should look like something you'd serve after a meal, not as a main course""",
            
            "dressing": """=== DRESSING/SAUCE STYLING ===
CRITICAL: This is a DRESSING or SAUCE, NOT a soup or main dish!
- Show in a small bowl, jar, or drizzled over salad/greens
- Should be a CONDIMENT, not a meal
- If it's a dressing: show it in a small bowl or being drizzled
- If it's a sauce: show it in a small serving dish or on the side
- NO large bowls, NO main dish presentation
- Should look like something you'd use to flavor other foods""",
            
            "bread": """=== BREAD STYLING ===
CRITICAL: This is BREAD, NOT a main dish!
- Show whole loaves, rolls, or individual pieces
- Should look baked, golden-brown, with proper bread texture
- Can be on a bread board, basket, or plate
- NO bowls, NO stew-like appearance
- Should look like bread you'd serve with a meal""",
            
            "appetizer": """=== APPETIZER/SALAD STYLING ===
- Show in a small serving dish or on a plate
- Should look fresh, colorful, and appetizing
- Can be part of a mezze/kemia spread
- Portion should be smaller than a main dish""",
            
            "main": """=== MAIN DISH STYLING ===
- Show as a complete main course
- Can be in a bowl, on a plate, or in a serving dish
- Should look substantial and satisfying
- Portion should be appropriate for a main meal"""
        }
        
        return styling_map.get(category, styling_map["main"])
    
    def _get_recipe_specific_corrections(self, dish_name: str, recipe_id: Optional[str] = None) -> Dict:
        """
        Get recipe-specific corrections/overrides for image generation.
        These override the research findings for known issues.
        
        Args:
            dish_name: Name of the dish
            recipe_id: Optional recipe ID for lookup
            
        Returns:
            Dict with corrections or empty dict
        """
        corrections = {}
        dish_lower = dish_name.lower()
        
        # Adafina: potatoes should be sliced, not unpeeled
        if dish_lower == "adafina" or (recipe_id and recipe_id == "adafina"):
            corrections.update({
                "specific_instructions": """CRITICAL: Potatoes must be SLICED (cut into rounds or chunks), 
NOT whole unpeeled potatoes. The dish shows layers of sliced potatoes, chickpeas, and seitan/tofu. 
Potatoes are peeled and sliced before cooking."""
            })
        
        # Apple crumble: should be cake-like/baked, not soupy
        if "apple crumble" in dish_lower or (recipe_id and recipe_id == "apple_crumble"):
            corrections.update({
                "consistency": "baked dessert",
                "specific_instructions": """CRITICAL: This is a BAKED DESSERT with a CRISP CRUMBLE TOPPING, 
NOT a soupy liquid. The apples should be soft and cooked, but the dish is SOLID with a golden-brown 
crumbly topping. It's served as a sliceable cake-like dessert, not a liquid soup."""
            })
        
        # Artichoke mushroom stew: whole portobello/baby mushrooms, mostly dominant
        if ("artichoke" in dish_lower and "mushroom" in dish_lower) or (recipe_id and recipe_id == "artichoke_mushroom_stew"):
            corrections.update({
                "specific_instructions": """CRITICAL: Mushrooms should be WHOLE portobello or baby portobello mushrooms, 
NOT sliced. Mushrooms are the MOST DOMINANT visible ingredient - they should be the main feature of the dish, 
larger and more prominent than the artichoke hearts. Show whole mushrooms as the star of the dish."""
            })
        
        return corrections
    
    def _get_protein_guidance(self, ingredients: Optional[List[str]], research_size: str) -> str:
        """Build protein sizing guidance based on research and ingredients."""
        if not ingredients:
            return research_size
        
        # Check if recipe has protein
        has_protein = any(
            word in ' '.join(ingredients).lower() 
            for word in ['tofu', 'seitan', 'meat', 'chicken', 'fish', 'lamb', 'beef']
        )
        
        if not has_protein:
            return "No protein pieces (vegetable-based dish)"
        
        # Determine protein type
        ing_lower = ' '.join(ingredients).lower()
        if 'tofu' in ing_lower:
            protein_type = "Tofu"
        elif 'seitan' in ing_lower:
            protein_type = "Seitan"
        else:
            protein_type = "Plant-based protein"
        
        # Combine with research
        if "cubes" in research_size or "1-2cm" in research_size:
            return f"{protein_type} pieces should be small 1-2cm cubes, NOT large chunks"
        elif "chunks" in research_size:
            return f"{protein_type} pieces should be medium-sized chunks, NOT oversized"
        elif "slices" in research_size:
            return f"{protein_type} should be thin slices, NOT thick pieces"
        else:
            return f"{protein_type} pieces: {research_size}, NOT oversized"
    
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
        
        # Get unique scene variation for this dish (use dish name + "_ing" for different but related scene)
        scene_variation = self._get_scene_variation(seed=f"{dish_name}_ingredients")
        
        # Build the prompt
        prompt = f"""Create a beautiful flat-lay photograph showing the raw ingredients 
for making {dish_name}:

Ingredients to show: {ingredients_text}

*** THIS IS A 100% VEGAN COOKBOOK ***
If any ingredient mentions meat/chicken/fish, show the vegan alternative instead.

{scene_variation}

Style requirements:
{self.INGREDIENTS_STYLE}

{additional_styling}

Arrange ingredients in an artistic, balanced composition
that showcases the fresh, quality ingredients used in this traditional recipe.
This is VEGAN food - no animal products whatsoever."""

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
        
        If recipe_data contains 'image_prompt' field, it will be used
        as a custom prompt override for dish image generation.
        
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
            
            # Check for custom image_prompt override
            custom_prompt = recipe_data.get('image_prompt')
            if custom_prompt:
                # Use custom prompt directly
                print(f"📝 Using custom image_prompt for {recipe_id}")
                results['dish'] = self._generate_and_save(custom_prompt, dish_path)
            else:
                # Use standard generation
                results['dish'] = self.generate_dish_image(
                    dish_name=dish_name,
                    description=dish_desc,
                    ingredients=ingredients_list,
                    cooking_method=cooking_method,
                    output_path=str(dish_path),
                    recipe_id=recipe_id  # Pass recipe_id for corrections
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

