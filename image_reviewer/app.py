#!/usr/bin/env python3
"""
Image Reviewer - Review cookbook images and rate them
"""

import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file

app = Flask(__name__)

# Paths
ROOT = Path(__file__).parent.parent
RECIPES_DIR = ROOT / "data" / "recipes_multilingual"
IMAGES_DIR = ROOT / "data" / "images" / "current"
REVIEWS_FILE = Path(__file__).parent / "reviews.json"

def load_reviews():
    if REVIEWS_FILE.exists():
        with open(REVIEWS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_reviews(reviews):
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

def get_all_recipes():
    """Load all recipes with their images."""
    recipes = []
    reviews = load_reviews()
    
    for path in sorted(RECIPES_DIR.glob("*.json")):
        with open(path, 'r') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get('id', path.stem)
        image_path = IMAGES_DIR / recipe_id / "dish.png"
        review = reviews.get(recipe_id, {})
        
        # Skip if marked as duplicate and removed
        if review.get('is_duplicate') and not path.exists():
            continue
        
        recipes.append({
            'id': recipe_id,
            'name': recipe.get('name', {}).get('en', recipe_id),
            'name_he': recipe.get('name', {}).get('he', ''),
            'description': recipe.get('description', {}).get('en', ''),
            'has_image': image_path.exists(),
            'has_custom_prompt': 'image_prompt' in recipe,
            'is_duplicate': review.get('is_duplicate', False)
        })
    
    return recipes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recipes')
def api_recipes():
    recipes = get_all_recipes()
    reviews = load_reviews()
    
    # Add review data to recipes
    for recipe in recipes:
        if recipe['id'] in reviews:
            recipe['review'] = reviews[recipe['id']]
        else:
            recipe['review'] = None
    
    return jsonify(recipes)

@app.route('/api/recipe/<recipe_id>')
def api_recipe(recipe_id):
    recipe_path = RECIPES_DIR / f"{recipe_id}.json"
    if not recipe_path.exists():
        return jsonify({'error': 'Recipe not found'}), 404
    
    with open(recipe_path, 'r') as f:
        recipe = json.load(f)
    
    reviews = load_reviews()
    recipe['review'] = reviews.get(recipe_id)
    
    return jsonify(recipe)

@app.route('/api/image/<recipe_id>')
def api_image(recipe_id):
    image_path = IMAGES_DIR / recipe_id / "dish.png"
    if image_path.exists():
        return send_file(image_path, mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/api/review/<recipe_id>', methods=['POST'])
def api_review(recipe_id):
    data = request.json
    reviews = load_reviews()
    
    reviews[recipe_id] = {
        'rating': data.get('rating', 0),
        'notes': data.get('notes', ''),
        'needs_regen': data.get('needs_regen', False),
        'is_duplicate': data.get('is_duplicate', False)
    }
    
    save_reviews(reviews)
    return jsonify({'success': True})

@app.route('/api/duplicate/<recipe_id>', methods=['POST'])
def api_mark_duplicate(recipe_id):
    """Mark a recipe as duplicate and optionally remove it."""
    data = request.json
    reviews = load_reviews()
    
    # Mark as duplicate
    if recipe_id not in reviews:
        reviews[recipe_id] = {}
    reviews[recipe_id]['is_duplicate'] = True
    reviews[recipe_id]['notes'] = data.get('notes', reviews[recipe_id].get('notes', ''))
    
    save_reviews(reviews)
    
    # If remove flag is set, actually delete the files
    if data.get('remove', False):
        return remove_duplicate(recipe_id)
    
    return jsonify({'success': True, 'marked': True})

def remove_duplicate(recipe_id):
    """Remove duplicate recipe files (JSON and images)."""
    import shutil
    
    archive_dir = ROOT / "data" / "recipes_duplicates"
    archive_dir.mkdir(exist_ok=True)
    
    image_archive_dir = ROOT / "data" / "images" / "archive"
    image_archive_dir.mkdir(exist_ok=True)
    
    removed = []
    errors = []
    
    # Move recipe JSON
    recipe_path = RECIPES_DIR / f"{recipe_id}.json"
    if recipe_path.exists():
        try:
            archive_path = archive_dir / f"{recipe_id}.json"
            shutil.move(str(recipe_path), str(archive_path))
            removed.append('recipe')
        except Exception as e:
            errors.append(f"Recipe: {e}")
    
    # Move image folder
    image_path = IMAGES_DIR / recipe_id
    if image_path.exists():
        try:
            archive_image_path = image_archive_dir / recipe_id
            if archive_image_path.exists():
                shutil.rmtree(str(archive_image_path))
            shutil.move(str(image_path), str(archive_image_path))
            removed.append('images')
        except Exception as e:
            errors.append(f"Images: {e}")
    
    if errors:
        return jsonify({'success': False, 'removed': removed, 'errors': errors}), 500
    
    return jsonify({'success': True, 'removed': removed})

@app.route('/api/stats')
def api_stats():
    reviews = load_reviews()
    recipes = get_all_recipes()
    
    total = len(recipes)
    reviewed = len(reviews)
    needs_regen = sum(1 for r in reviews.values() if r.get('needs_regen'))
    duplicates = sum(1 for r in reviews.values() if r.get('is_duplicate'))
    avg_rating = sum(r.get('rating', 0) for r in reviews.values()) / reviewed if reviewed else 0
    
    return jsonify({
        'total': total,
        'reviewed': reviewed,
        'pending': total - reviewed,
        'needs_regen': needs_regen,
        'duplicates': duplicates,
        'avg_rating': round(avg_rating, 1)
    })

if __name__ == '__main__':
    print("Image Reviewer")
    print("=" * 40)
    print(f"Recipes: {RECIPES_DIR}")
    print(f"Images: {IMAGES_DIR}")
    print()
    print("Open http://localhost:5050 in your browser")
    print()
    app.run(host='0.0.0.0', port=5050, debug=True)

