#!/usr/bin/env python3
import json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from generate_cookbook_images import CookbookImageGenerator

os.environ['GEMINI_API_KEY'] = open('.env').read().split('GEMINI_API_KEY=')[1].split('\n')[0].strip()

prompts = [
    # v6: emphasize thin round dough folded in half
    """Photo of Tunisian Brik pastry (בריקות). A ROUND thin translucent dough sheet (malsouka) with a small amount of filling (mashed potato, parsley) placed ONLY in the CENTER, then the round sheet is FOLDED IN HALF to make a half-moon. Deep fried golden. The dough is paper-thin, you can almost see through it. Most of the pastry is just empty thin dough with filling only in the middle bulge. 3 brikot on a plate. Photorealistic food photography.""",

    # v7: focus on the thinness and transparency
    """Tunisian Brik - crispy fried half-moon pastry. Made from a SINGLE ROUND paper-thin malsouka sheet folded in half over a SMALL mound of potato filling in the center. The pastry is extremely thin and TRANSLUCENT - mostly flat crispy dough with a slight bump where the filling is. Golden-brown, oil-glistening surface. NOT stuffed full like an empanada - the filling is minimal, just a thin layer in the center. Show on a wire rack or plate. Professional food photography, natural light.""",

    # v8: emphasize it's NOT stuffed
    """בריק תוניסאי - צילום אוכל מקצועי. עלה מלסוקה עגול דק כנייר, מקופל לחצי עם מעט מילוי (תפוח אדמה מרוסק ופטרוזיליה) רק במרכז. הבצק שקוף כמעט, רואים דרכו. הבריק שטוח ברובו עם בליטה קטנה במרכז מהמילוי. מטוגן עמוק עד זהוב ופריך. 3-4 בריקות על צלחת. לא ממולא כמו אמפנדה - רוב הבריק הוא בצק ריק!""",

    # v9: describe the frying process look
    """Brik pastry fresh from the fryer. Half-circle shape made from one round tissue-thin malsouka leaf folded over. The key visual: the pastry is 90% thin crispy golden dough, with only a small central area where you see the potato-parsley filling creating a slight raised area. The edges are thin, crispy, and slightly wavy/bubbly from frying. Some parts of the dough are so thin they're almost transparent showing greenish filling underneath. Served on a simple plate with lemon wedge. Photorealistic 8K.""",

    # v10: comparison to help the model
    """Food photo of Tunisian Brik (NOT empanada, NOT samosa, NOT spring roll). Think of it like a CREPE folded in half with a tiny bit of filling. A single round sheet of paper-thin dough (thinner than phyllo), with 2-3 tablespoons of mashed potato placed in center, then folded into half-moon and deep fried. Result: flat, crispy, golden half-circle. The filling barely shows - it's mostly just crispy thin fried dough. Show 3 on a plate, one broken open to reveal the thin layer of filling inside. Professional cookbook photography.""",
]

def gen(v, prompt):
    r = {"id": f"brikot_v{v}", "name": {"en": "Brikot"}, "description": {"en": ""}, 
         "ingredients": {"en": []}, "steps": {"en": []}, "image_prompt": prompt}
    g = CookbookImageGenerator()
    res = g.generate_recipe_images(r, generate_dish=True, generate_ingredients=False)
    if 'dish' in res:
        return (v, True, res['dish'])
    return (v, False, 'Failed')

print("Generating 5 new Brikot variants (v6-v10) with varied prompts...")
with ThreadPoolExecutor(max_workers=5) as ex:
    futs = {ex.submit(gen, v, p): v for v, p in zip(range(6, 11), prompts)}
    for f in as_completed(futs):
        v, ok, path = f.result()
        print(f"  {'✅' if ok else '❌'} v{v}: {path}")

print("\nDone! Check data/images/generated/brikot_v6-v10_dish.png")
