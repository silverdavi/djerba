#!/usr/bin/env python3
"""
Scan all recipes for incorrect terms in parentheses.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

recipes_dir = Path('data/recipes_multilingual')
all_issues = defaultdict(list)

print('Scanning all recipes for terms in parentheses...')
print('=' * 60)

for recipe_file in sorted(recipes_dir.glob('*.json')):
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    recipe_id = recipe.get('id', recipe_file.stem)
    recipe_name = recipe.get('name', {}).get('en', recipe_id)
    
    # Check descriptions for various patterns
    for lang in ['he', 'es', 'ar', 'en']:
        desc = recipe.get('description', {}).get(lang, '')
        if not desc:
            continue
        
        # Pattern 1: Single-quoted terms in parentheses: ('term')
        pattern1 = r"\('([^']+)'\)"
        matches1 = re.findall(pattern1, desc)
        for match in matches1:
            idx = desc.find(f"('{match}')")
            context_start = max(0, idx - 50)
            context_end = min(len(desc), idx + len(match) + 60)
            context = desc[context_start:context_end]
            
            all_issues[recipe_id].append({
                'type': 'single_quoted',
                'lang': lang,
                'term': match,
                'recipe': recipe_name,
                'context': context
            })
        
        # Pattern 2: Terms in parentheses that might be transliterations
        pattern2 = r'\(([a-z]+)\)'
        matches2 = re.findall(pattern2, desc)
        for match in matches2:
            # Skip common words
            skip_words = {'optional', 'vegan', 'frozen', 'cubed', 'chopped', 'sliced', 'diced', 
                         'crushed', 'minced', 'fresh', 'dried', 'canned', 'packet', 'small', 
                         'large', 'medium', 'approx', 'about', 'etc', 'eg', 'ie', 'aka',
                         'lost', 'enterrada', 'enterrado', 'buried', 'cooked', 'toast'}
            if match.lower() not in skip_words and len(match) > 3:
                idx = desc.find(f'({match})')
                context_start = max(0, idx - 50)
                context_end = min(len(desc), idx + len(match) + 60)
                context = desc[context_start:context_end]
                
                all_issues[recipe_id].append({
                    'type': 'parenthesized_term',
                    'lang': lang,
                    'term': match,
                    'recipe': recipe_name,
                    'context': context
                })

# Report findings
if all_issues:
    print(f'Found {len(all_issues)} recipes with potential issues:\n')
    for recipe_id, issues in sorted(all_issues.items()):
        print(f'\n{recipe_id} ({issues[0]["recipe"]}):')
        for issue in issues:
            print(f'  [{issue["lang"].upper()}] {issue["type"]}: "{issue["term"]}"')
            print(f'    Context: ...{issue["context"]}...')
else:
    print('✅ No issues found')

print()
print('=' * 60)
print(f'Total recipes scanned: {len(list(recipes_dir.glob("*.json")))}')
print(f'Recipes with issues: {len(all_issues)}')

