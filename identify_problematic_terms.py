#!/usr/bin/env python3
"""
Identify potentially problematic terms in parentheses.
Focus on:
1. Dish names that might be wrong (like qarnoun)
2. English words in non-English text
3. Terms that don't match the recipe
"""

import json
import re
from pathlib import Path

recipes_dir = Path('data/recipes_multilingual')

# Known problematic patterns
problematic_terms = {
    'qarnoun': 'Specific dish name, not general artichoke term',
    'kakawiya': 'Check if this is correct for peanuts',
}

# English words that shouldn't appear in non-English text
english_words_in_other_langs = ['capers', 'appetizer', 'broth', 'stew', 'fried', 'pieces', 
                                'circle', 'sponge', 'turning', 'semolina', 'sour', 'warming',
                                'curdled', 'clay']

print('Identifying potentially problematic terms...')
print('=' * 60)

issues = []

for recipe_file in sorted(recipes_dir.glob('*.json')):
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    recipe_id = recipe.get('id', recipe_file.stem)
    recipe_name = recipe.get('name', {}).get('en', recipe_id)
    
    for lang in ['he', 'es', 'ar']:  # Check non-English languages
        desc = recipe.get('description', {}).get(lang, '')
        if not desc:
            continue
        
        # Check for known problematic terms
        for term, reason in problematic_terms.items():
            if f"('{term}')" in desc or f"({term})" in desc:
                idx = desc.find(f"('{term}')") if f"('{term}')" in desc else desc.find(f"({term})")
                context_start = max(0, idx - 60)
                context_end = min(len(desc), idx + len(term) + 80)
                context = desc[context_start:context_end]
                
                issues.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_name,
                    'lang': lang,
                    'term': term,
                    'reason': reason,
                    'context': context,
                    'full_desc': desc
                })
        
        # Check for English words in non-English text
        for word in english_words_in_other_langs:
            pattern = f'\\({word}\\)'
            if re.search(pattern, desc, re.IGNORECASE):
                idx = desc.lower().find(f'({word})')
                context_start = max(0, idx - 60)
                context_end = min(len(desc), idx + len(word) + 80)
                context = desc[context_start:context_end]
                
                issues.append({
                    'recipe_id': recipe_id,
                    'recipe_name': recipe_name,
                    'lang': lang,
                    'term': word,
                    'reason': f'English word in {lang.upper()} text',
                    'context': context,
                    'full_desc': desc
                })

# Report
if issues:
    print(f'\nFound {len(issues)} potentially problematic terms:\n')
    
    # Group by recipe
    by_recipe = {}
    for issue in issues:
        key = issue['recipe_id']
        if key not in by_recipe:
            by_recipe[key] = []
        by_recipe[key].append(issue)
    
    for recipe_id in sorted(by_recipe.keys()):
        recipe_issues = by_recipe[recipe_id]
        print(f'\n{recipe_id} ({recipe_issues[0]["recipe_name"]}):')
        for issue in recipe_issues:
            print(f'  [{issue["lang"].upper()}] "{issue["term"]}" - {issue["reason"]}')
            print(f'    Context: ...{issue["context"]}...')
            print()
else:
    print('✅ No problematic terms found')

print('=' * 60)
print(f'Total issues found: {len(issues)}')

