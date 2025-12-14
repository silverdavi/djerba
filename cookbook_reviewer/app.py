#!/usr/bin/env python3
"""
Cookbook Reviewer - Review full recipe pages and note fixes
"""

import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file, send_from_directory

app = Flask(__name__)

# Paths
ROOT = Path(__file__).parent.parent
RECIPES_DIR = ROOT / "data" / "recipes_multilingual_v2"
CANONICAL_DIR = ROOT / "data" / "recipes_canonical"
IMAGES_DIR = ROOT / "data" / "images" / "current"
WEB_OUTPUT_DIR = ROOT / "gen_book" / "output" / "web"
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
    """Load all recipes."""
    recipes = []
    reviews = load_reviews()
    
    for path in sorted(RECIPES_DIR.glob("*.json")):
        with open(path, 'r') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get('id', path.stem)
        review = reviews.get(recipe_id, {})
        
        # Find the corresponding HTML file
        html_file = WEB_OUTPUT_DIR / f"{recipe_id}.html"
        has_html = html_file.exists()
        
        # Get image path
        image_field = recipe.get('image', '')
        has_image = False
        if image_field:
            img_path = ROOT / "data" / image_field
            has_image = img_path.exists()
        
        recipes.append({
            'id': recipe_id,
            'filename': path.name,
            'name': recipe.get('name', {}).get('en', recipe_id),
            'name_he': recipe.get('name', {}).get('he', ''),
            'name_es': recipe.get('name', {}).get('es', ''),
            'name_ar': recipe.get('name', {}).get('ar', ''),
            'has_html': has_html,
            'has_image': has_image,
            'image_path': image_field,
            'review': review if review else None
        })
    
    return recipes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recipes')
def api_recipes():
    recipes = get_all_recipes()
    return jsonify(recipes)

@app.route('/api/recipe/<recipe_id>')
def api_recipe(recipe_id):
    # Try multiple filename patterns
    possible_files = [
        RECIPES_DIR / f"{recipe_id}.json",
    ]
    
    recipe_path = None
    for p in possible_files:
        if p.exists():
            recipe_path = p
            break
    
    if not recipe_path:
        return jsonify({'error': 'Recipe not found'}), 404
    
    with open(recipe_path, 'r') as f:
        recipe = json.load(f)
    
    reviews = load_reviews()
    recipe['review'] = reviews.get(recipe_id)
    
    return jsonify(recipe)

@app.route('/api/html/<recipe_id>')
def api_html(recipe_id):
    """Serve the HTML recipe page."""
    html_file = WEB_OUTPUT_DIR / f"{recipe_id}.html"
    if html_file.exists():
        return send_file(html_file, mimetype='text/html')
    return jsonify({'error': 'HTML not found'}), 404

@app.route('/api/image/<path:image_path>')
def api_image(image_path):
    """Serve recipe images."""
    full_path = ROOT / "data" / image_path
    if full_path.exists():
        return send_file(full_path, mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/web/<path:filename>')
def serve_web(filename):
    """Serve files from web output directory."""
    return send_from_directory(WEB_OUTPUT_DIR, filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from current directory."""
    return send_from_directory(IMAGES_DIR, filename)

# Serve relative image paths from HTML files
# When iframe loads /api/html/recipe, relative paths like ../images/... resolve to /api/images/...
@app.route('/api/images/<path:filename>')
def serve_relative_images(filename):
    """Serve images with relative paths from HTML."""
    # Handle paths like current/001_adafina/dish.png
    full_path = ROOT / "data" / "images" / filename
    if full_path.exists():
        return send_file(full_path, mimetype='image/png')
    # Try gen_book output
    full_path = ROOT / "gen_book" / "output" / "images" / filename
    if full_path.exists():
        return send_file(full_path, mimetype='image/png')
    return jsonify({'error': f'Image not found: {filename}'}), 404

# Serve absolute paths (ingredient images etc)
@app.route('/Users/<path:filepath>')
def serve_absolute_path(filepath):
    """Serve files with absolute paths."""
    full_path = Path('/Users') / filepath
    if full_path.exists() and full_path.suffix in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        return send_file(full_path)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/review/<recipe_id>', methods=['POST'])
def api_review(recipe_id):
    data = request.json
    reviews = load_reviews()
    
    reviews[recipe_id] = {
        'status': data.get('status', 'pending'),  # pending, ok, needs_fix
        'fixes_needed': data.get('fixes_needed', ''),
        'priority': data.get('priority', 'normal'),  # low, normal, high
    }
    
    save_reviews(reviews)
    return jsonify({'success': True})

@app.route('/api/stats')
def api_stats():
    reviews = load_reviews()
    recipes = get_all_recipes()
    
    total = len(recipes)
    reviewed = sum(1 for r in reviews.values() if r.get('status') in ['ok', 'needs_fix'])
    needs_fix = sum(1 for r in reviews.values() if r.get('status') == 'needs_fix')
    ok = sum(1 for r in reviews.values() if r.get('status') == 'ok')
    high_priority = sum(1 for r in reviews.values() if r.get('priority') == 'high')
    
    return jsonify({
        'total': total,
        'reviewed': reviewed,
        'pending': total - reviewed,
        'ok': ok,
        'needs_fix': needs_fix,
        'high_priority': high_priority,
    })

@app.route('/api/export')
def api_export():
    """Export all fixes needed as a summary."""
    reviews = load_reviews()
    fixes = []
    
    for recipe_id, review in reviews.items():
        if review.get('status') == 'needs_fix' and review.get('fixes_needed'):
            fixes.append({
                'recipe_id': recipe_id,
                'priority': review.get('priority', 'normal'),
                'fixes': review.get('fixes_needed', '')
            })
    
    # Sort by priority (high first)
    priority_order = {'high': 0, 'normal': 1, 'low': 2}
    fixes.sort(key=lambda x: priority_order.get(x['priority'], 1))
    
    return jsonify(fixes)

if __name__ == '__main__':
    print("Cookbook Reviewer")
    print("=" * 40)
    print(f"Recipes: {RECIPES_DIR}")
    print(f"Web Output: {WEB_OUTPUT_DIR}")
    print()
    print("Open http://localhost:5051 in your browser")
    print()
    app.run(host='0.0.0.0', port=5051, debug=True)

