#!/usr/bin/env python3
"""
Fetch recipes from ReciMe Firestore using Firebase ID Token

Uses the Firestore REST API endpoint to retrieve recipes.

Usage:
    python fetch_recime_firestore.py --token YOUR_ID_TOKEN --user-id YOUR_USER_ID
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class ReciMeFirestoreFetcher:
    """Fetch recipes from ReciMe's Firestore database"""
    
    # Firebase Firestore REST API
    FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/recime-prod/databases/(default)/documents"
    
    def __init__(self, id_token: str, user_id: str, output_dir: str = "raw"):
        self.id_token = id_token
        self.user_id = user_id
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
    
    def fetch_user_recipes(self) -> bool:
        """Fetch all recipes for the current user from Firestore"""
        self.log(f"📚 Fetching recipes for user: {self.user_id}")
        
        # Try to fetch from users/{user_id}/recipes collection
        endpoint = f"{self.FIRESTORE_URL}/users/{self.user_id}/recipes"
        
        try:
            self.log(f"  Endpoint: {endpoint}")
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=15
            )
            
            self.log(f"  Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self._process_firestore_response(data)
                return True
            else:
                self.log(f"  Response body: {response.text[:500]}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request failed: {str(e)}")
            return False
    
    def _process_firestore_response(self, data: Dict):
        """Process Firestore REST response"""
        self.log(f"✓ Response received")
        
        if "documents" not in data:
            self.log(f"  ⚠️  No documents in response")
            self.log(f"  Full response: {json.dumps(data, indent=2)[:500]}")
            return
        
        documents = data.get("documents", [])
        self.log(f"  Found {len(documents)} documents")
        
        for doc in documents:
            self._process_firestore_document(doc)
    
    def _process_firestore_document(self, doc: Dict):
        """Process individual Firestore document"""
        # Firestore REST response format
        fields = doc.get("fields", {})
        
        recipe = self._firestore_to_dict(fields)
        recipe["id"] = doc.get("name", "").split("/")[-1]
        
        if recipe.get("name"):
            self.recipes.append(recipe)
            self.log(f"  ✓ Processed: {recipe.get('name', 'Unknown')}")
    
    def _firestore_to_dict(self, fields: Dict) -> Dict:
        """Convert Firestore field format to regular dict"""
        result = {}
        
        for key, value in fields.items():
            result[key] = self._firestore_value_to_python(value)
        
        return result
    
    def _firestore_value_to_python(self, firestore_value: Dict):
        """Convert Firestore value format to Python type"""
        if "stringValue" in firestore_value:
            return firestore_value["stringValue"]
        elif "integerValue" in firestore_value:
            return int(firestore_value["integerValue"])
        elif "doubleValue" in firestore_value:
            return float(firestore_value["doubleValue"])
        elif "booleanValue" in firestore_value:
            return firestore_value["booleanValue"]
        elif "arrayValue" in firestore_value:
            array_value = firestore_value["arrayValue"].get("values", [])
            return [self._firestore_value_to_python(v) for v in array_value]
        elif "mapValue" in firestore_value:
            map_value = firestore_value["mapValue"].get("fields", {})
            return self._firestore_to_dict(map_value)
        elif "nullValue" in firestore_value:
            return None
        else:
            return firestore_value
    
    def save_recipes(self) -> int:
        """Save fetched recipes to JSON files"""
        if not self.recipes:
            self.log("⚠️  No recipes to save")
            return 0
        
        count = 0
        for recipe in self.recipes:
            try:
                # Use recipe name as filename, sanitize it
                filename = recipe.get("name", "unknown").lower().strip()
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
        """Write fetch log"""
        log_file = self.output_dir.parent / "FIRESTORE_FETCH_LOG.md"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("# ReciMe Firestore Fetch Log\n\n")
            f.write(f"**Fetch Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**User ID:** {self.user_id}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Total recipes fetched:** {len(self.recipes)}\n\n")
            f.write("## Log Entries\n\n")
            for entry in self.log_entries:
                f.write(f"{entry}\n")
        
        print(f"✅ Log written to {log_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch recipes from ReciMe's Firestore using Firebase ID Token"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="Firebase ID Token (from browser DevTools)"
    )
    parser.add_argument(
        "--user-id",
        required=True,
        help="Firebase User ID (localId from auth response)"
    )
    parser.add_argument(
        "--output",
        default="raw",
        help="Output directory for recipes (default: raw)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("ReciMe Firestore Recipe Fetcher")
    print("=" * 70)
    print()
    
    fetcher = ReciMeFirestoreFetcher(args.token, args.user_id, args.output)
    
    # Fetch recipes
    success = fetcher.fetch_user_recipes()
    
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
