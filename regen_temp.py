#!/usr/bin/env python3
import json, os, glob
from concurrent.futures import ThreadPoolExecutor, as_completed
from generate_cookbook_images import CookbookImageGenerator

os.environ['GEMINI_API_KEY'] = open('.env').read().split('GEMINI_API_KEY=')[1].split('\n')[0].strip()

for f in glob.glob("data/images/generated/pizza_v*_dish.png"):
    os.remove(f)

# v17 prompt was the 45-degree angle one - replicate with minor variations
base = """Photo of homemade pizza in a large rectangular metal baking tray.

THE PIZZA:
- THICK bread-like golden dough (NOT burnt, just nicely golden-brown)
- GENEROUS layer of tomato sauce covering most of the surface (more sauce than usual)
- Small scattered pieces of CANNED TUNA on top (not chickpeas!) - just a moderate amount, not too much
- Green olive RINGS (sliced circles) scattered on top
- A few capers here and there
- NOT BURNT - just perfectly baked golden, the sauce is red-dark but not black
- The crust edges are light golden, puffy, bread-like

COLOR: warm golden crust, rich red (not black) tomato sauce, light tuna pieces, green olive rings
NOT: charred, blackened, overcooked, or raw

45-degree angle. Thick puffy golden bread crust, red sauce, scattered tuna and green olives. Warm kitchen light. 8K."""

variations = [
    " Slightly closer shot, showing texture of the bread crust.",
    " The tray is on a rustic wooden table.",
    " Steam slightly visible rising from the fresh pizza.",
    " One corner piece slightly separated from the rest.",
    " Natural afternoon light from a window.",
    " A knife resting next to the tray.",
    " The pizza fills the entire large tray edge to edge.",
    " Slightly more overhead angle, about 50 degrees.",
    " A cloth napkin visible at the edge of frame.",
    " Shallow depth of field, focus on the center of the pizza.",
]

def gen(v, prompt):
    r = {"id": f"pizza_v{v}", "name": {"en": "Pizza"}, "description": {"en": ""},
         "ingredients": {"en": []}, "steps": {"en": []}, "image_prompt": prompt}
    g = CookbookImageGenerator()
    res = g.generate_recipe_images(r, generate_dish=True, generate_ingredients=False)
    if 'dish' in res:
        return (v, True, res['dish'])
    return (v, False, 'Failed')

print("Generating 10 Pizza variants based on v17 with minor variations...")
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(gen, v, base + var): v for v, var in zip(range(21, 31), variations)}
    for f in as_completed(futs):
        v, ok, path = f.result()
        print(f"  {'✅' if ok else '❌'} v{v}: {path}")

print("\nDone!")
