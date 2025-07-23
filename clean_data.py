#!/usr/bin/env python3
"""
Clean Generated Data Script
Removes all generated content to start fresh
"""

import os
import shutil
import argparse
from pathlib import Path

def clean_data(confirm=False):
    """Remove all generated data"""
    
    if not confirm:
        print("⚠️  This will DELETE ALL generated content:")
        print("   • All recipes (markdown + translations)")
        print("   • All research files") 
        print("   • All generated images")
        print("   • All processing status files")
        print("   • All LaTeX generated files")
        print()
        response = input("Are you sure? Type 'DELETE' to confirm: ")
        if response != 'DELETE':
            print("❌ Cancelled")
            return
    
    print("🧹 Cleaning generated data...")
    
    # Directories to clean
    dirs_to_clean = [
        "data/recipes/markdown",
        "data/recipes/translations", 
        "data/research",
        "data/images/generated",
        "latex/recipes",
        "latex/images"
    ]
    
    # Files to clean
    files_to_clean = [
        "data/pipeline_progress.json",
        "recipe_processing_status.csv",
        "recipe_processing_progress.json",
        "latex/output/main.pdf",
        "latex/output/main.aux",
        "latex/output/main.toc",
        "latex/output/main.log"
    ]
    
    # Clean directories
    for dir_path in dirs_to_clean:
        if Path(dir_path).exists():
            try:
                shutil.rmtree(dir_path)
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                print(f"✅ Cleaned: {dir_path}")
            except Exception as e:
                print(f"❌ Error cleaning {dir_path}: {e}")
    
    # Clean files
    for file_path in files_to_clean:
        if Path(file_path).exists():
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    print("\n🎉 Data cleanup complete! Ready for fresh start.")
    print("💡 Run 'python process_all_recipes.py --workers 30' to regenerate")

def clean_status_only():
    """Clean only status/progress files (keep generated content)"""
    print("🧹 Cleaning status files only...")
    
    files_to_clean = [
        "recipe_processing_status.csv",
        "recipe_processing_progress.json"
    ]
    
    for file_path in files_to_clean:
        if Path(file_path).exists():
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
    
    print("✅ Status files cleaned! Processing will start fresh.")

def show_data_summary():
    """Show what data exists"""
    print("📊 Current Data Summary:")
    print("=" * 40)
    
    # Count files in each directory
    data_dirs = {
        "Recipes (Markdown)": "data/recipes/markdown",
        "Translations": "data/recipes/translations",
        "Research Files": "data/research", 
        "Generated Images": "data/images/generated",
        "LaTeX Recipes": "latex/recipes"
    }
    
    for name, path in data_dirs.items():
        if Path(path).exists():
            count = len(list(Path(path).rglob("*"))) - len(list(Path(path).rglob("*/")))
            print(f"  {name:20}: {count:3d} files")
        else:
            print(f"  {name:20}:   0 files (empty)")
    
    # Show status files
    status_files = [
        "recipe_processing_status.csv",
        "recipe_processing_progress.json"
    ]
    
    print("\nStatus Files:")
    for file_path in status_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"  {file_path:30}: {size:,} bytes")
        else:
            print(f"  {file_path:30}: Not found")

def main():
    parser = argparse.ArgumentParser(description='Clean generated cookbook data')
    parser.add_argument('--all', action='store_true', 
                       help='Clean ALL generated data (recipes, research, images)')
    parser.add_argument('--status', action='store_true',
                       help='Clean only status/progress files')
    parser.add_argument('--summary', action='store_true',
                       help='Show summary of current data')
    parser.add_argument('--force', action='store_true',
                       help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    if args.summary:
        show_data_summary()
    elif args.status:
        clean_status_only()
    elif args.all:
        clean_data(confirm=args.force)
    else:
        print("Clean Generated Cookbook Data")
        print("=" * 30)
        print("Options:")
        print("  --summary  Show what data exists")
        print("  --status   Clean only status files")
        print("  --all      Clean ALL generated data")
        print("  --force    Skip confirmation")
        print()
        print("Examples:")
        print("  python clean_data.py --summary")
        print("  python clean_data.py --status")
        print("  python clean_data.py --all")

if __name__ == "__main__":
    main() 