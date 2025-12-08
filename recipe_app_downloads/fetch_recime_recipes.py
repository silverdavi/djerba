#!/usr/bin/env python3
"""
Fetch recipes from ReciMe using Firebase ID Token

Usage:
    python fetch_recime_recipes.py --token YOUR_ID_TOKEN --cookbook-id COOKBOOK_ID
    python fetch_recime_recipes.py --token YOUR_ID_TOKEN --recipe-id RECIPE_ID

Example:
    python fetch_recime_recipes.py \
        --token "eyJhbGciOiJSUzI1NiIs..." \
        --cookbook-id "7fa89dcb-f59c-4db7-b13a-e24d3a9522e4"
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class ReciMeFetcher:
    """Fetch recipes from ReciMe API using Firebase authentication"""
    
    # ReciMe/Firebase API endpoints
    BASE_URL = "https://www.recime.app"
    FIREBASE_URL = "https://recime-prod.firebaseapp.com"
    
    # Try multiple potential API endpoints
    API_ENDPOINTS = [
        "https://api.recime.app",
        "https://recime-prod.firebaseapp.com",
        "https://www.recime.app/api",
    ]
    
    def __init__(self, id_token: str, output_dir: str = "raw"):
        self.id_token = id_token
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.headers = {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        self.recipes = []
        self.log_entries = []
    
    def log(self, message: str):
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_entries.append(full_message)
        print(full_message)
    
    def fetch_cookbook(self, cookbook_id: str) -> bool:
        """Fetch recipes from a specific cookbook"""
        self.log(f"📚 Fetching cookbook: {cookbook_id}")
        
        # Try different API endpoints
        endpoints = [
            f"{self.FIREBASE_URL}/api/cookbooks/{cookbook_id}",
            f"https://www.recime.app/api/cookbooks/{cookbook_id}",
            f"{self.BASE_URL}/dashboard/cookbooks/{cookbook_id}/recipes",
        ]
        
        for endpoint in endpoints:
            try:
                self.log(f"  Trying: {endpoint}")
                response = requests.get(
                    endpoint,
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.log(f"✓ Successfully fetched from: {endpoint}")
                    self._process_cookbook_data(data)
                    return True
                elif response.status_code == 401:
                    self.log(f"❌ Unauthorized (401): Token may be expired")
                elif response.status_code == 404:
                    self.log(f"⚠️  Not found (404): {endpoint}")
                else:
                    self.log(f"⚠️  Status {response.status_code}: {endpoint}")
                    
            except requests.exceptions.RequestException as e:
                self.log(f"⚠️  Request failed: {str(e)}")
                continue
        
        self.log("❌ Failed to fetch cookbook from all endpoints")
        return False
    
    def fetch_recipe(self, recipe_id: str) -> bool:
        """Fetch a single recipe"""
        self.log(f"📖 Fetching recipe: {recipe_id}")
        
        endpoints = [
            f"{self.FIREBASE_URL}/api/recipes/{recipe_id}",
            f"https://www.recime.app/api/recipes/{recipe_id}",
            f"{self.BASE_URL}/dashboard/recipes/{recipe_id}",
        ]
        
        for endpoint in endpoints:
            try:
                self.log(f"  Trying: {endpoint}")
                response = requests.get(
                    endpoint,
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.log(f"✓ Successfully fetched from: {endpoint}")
                    self._process_recipe_data(data)
                    return True
                else:
                    self.log(f"⚠️  Status {response.status_code}: {endpoint}")
                    
            except requests.exceptions.RequestException as e:
                self.log(f"⚠️  Request failed: {str(e)}")
                continue
        
        self.log("❌ Failed to fetch recipe from all endpoints")
        return False
    
    def _process_cookbook_data(self, data: Dict):
        """Process cookbook response data"""
        # Handle various response formats
        recipes = []
        
        if isinstance(data, dict):
            if "recipes" in data:
                recipes = data["recipes"] if isinstance(data["recipes"], list) else [data["recipes"]]
            elif "items" in data:
                recipes = data["items"] if isinstance(data["items"], list) else [data["items"]]
            elif "data" in data:
                recipes = data["data"] if isinstance(data["data"], list) else [data["data"]]
            else:
                # Might be a single recipe
                recipes = [data]
        elif isinstance(data, list):
            recipes = data
        
        self.log(f"  Found {len(recipes)} recipes")
        for recipe in recipes:
            self._process_recipe_data(recipe)
    
    def _process_recipe_data(self, recipe: Dict):
        """Process individual recipe data"""
        if not recipe.get("name"):
            return
        
        # Normalize recipe data
        normalized = {
            "id": recipe.get("id", recipe.get("_id", "")),
            "name": recipe.get("name", "Unknown"),
            "ingredients": self._normalize_list(recipe.get("ingredients", [])),
            "instructions": self._normalize_list(recipe.get("instructions", recipe.get("steps", []))),
            "description": recipe.get("description", ""),
            "servings": recipe.get("servings", ""),
            "prep_time": recipe.get("prepTime", recipe.get("prep_time", "")),
            "cook_time": recipe.get("cookTime", recipe.get("cook_time", "")),
            "image": recipe.get("image", recipe.get("imageUrl", "")),
            "source": recipe.get("source", "recime"),
            "metadata": {
                "original": recipe
            }
        }
        
        self.recipes.append(normalized)
        self.log(f"  ✓ Processed: {normalized['name']}")
    
    def _normalize_list(self, data) -> List[str]:
        """Normalize ingredients/instructions to list of strings"""
        if not data:
            return []
        
        if isinstance(data, list):
            return [str(item) if not isinstance(item, str) else item for item in data]
        elif isinstance(data, str):
            return [data]
        else:
            return [str(data)]
    
    def save_recipes(self) -> int:
        """Save fetched recipes to JSON files"""
        if not self.recipes:
            self.log("⚠️  No recipes to save")
            return 0
        
        count = 0
        for recipe in self.recipes:
            try:
                # Use recipe name as filename, sanitize it
                filename = recipe["name"].lower().strip()
                filename = ''.join(c if c.isalnum() or c in '_- ' else '_' for c in filename)
                filename = '_'.join(filename.split())
                
                output_file = self.output_dir / f"{filename}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(recipe, f, ensure_ascii=False, indent=2)
                
                count += 1
                self.log(f"  💾 Saved: {output_file.name}")
                
            except Exception as e:
                self.log(f"  ❌ Error saving recipe: {e}")
        
        self.log(f"💾 Saved {count} recipes to {self.output_dir}")
        return count
    
    def write_log(self):
        """Write import log"""
        log_file = self.output_dir.parent / "FETCH_LOG.md"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("# ReciMe Recipe Fetch Log\n\n")
            f.write(f"**Fetch Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Total recipes fetched:** {len(self.recipes)}\n\n")
            f.write("## Log Entries\n\n")
            for entry in self.log_entries:
                f.write(f"{entry}\n")
        
        print(f"✅ Log written to {log_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch recipes from ReciMe using Firebase ID Token"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="Firebase ID Token (from browser DevTools)"
    )
    parser.add_argument(
        "--cookbook-id",
        help="Cookbook ID to fetch (e.g., 7fa89dcb-f59c-4db7-b13a-e24d3a9522e4)"
    )
    parser.add_argument(
        "--recipe-id",
        help="Single recipe ID to fetch"
    )
    parser.add_argument(
        "--output",
        default="raw",
        help="Output directory for recipes (default: raw)"
    )
    
    args = parser.parse_args()
    
    if not args.cookbook_id and not args.recipe_id:
        parser.error("Provide either --cookbook-id or --recipe-id")
    
    print("=" * 70)
    print("ReciMe Recipe Fetcher")
    print("=" * 70)
    print()
    
    fetcher = ReciMeFetcher(args.token, args.output)
    
    # Fetch recipes
    if args.cookbook_id:
        fetcher.fetch_cookbook(args.cookbook_id)
    elif args.recipe_id:
        fetcher.fetch_recipe(args.recipe_id)
    
    print()
    
    # Save recipes
    if fetcher.recipes:
        saved_count = fetcher.save_recipes()
        fetcher.log(f"✅ Fetch complete: {saved_count} recipes saved")
    else:
        fetcher.log("⚠️  No recipes fetched")
    
    # Write log
    print()
    fetcher.write_log()
    
    print()
    print("=" * 70)
    print(f"✅ Total recipes fetched: {len(fetcher.recipes)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
