#!/usr/bin/env python3
"""
Master Pipeline for Vegan Djerban Family Cookbook
Orchestrates the complete process from CSV to final cookbook
"""

import sys
import argparse
import subprocess
from pathlib import Path

def run_markdown_pipeline():
    """Run the core AI pipeline to generate markdown content"""
    print("🚀 Starting Markdown Generation Pipeline...")
    print("=" * 60)
    
    try:
        # Run the core AI pipeline
        print("🤖 Running AI content generation pipeline...")
        result = subprocess.run([sys.executable, 'cookbook_pipeline.py'], 
                              capture_output=True, text=True, check=True)
        print("✅ AI pipeline completed successfully!")
        print(result.stdout)
        
        # Show summary of generated files
        print("\n📊 Generated Content Summary:")
        print("-" * 40)
        
        # Count markdown files
        markdown_dir = Path("data/recipes/markdown")
        if markdown_dir.exists():
            markdown_files = list(markdown_dir.glob("*.md"))
            print(f"📝 Markdown Recipes: {len(markdown_files)}")
        
        # Count translation files
        translation_dir = Path("data/recipes/translations")
        if translation_dir.exists():
            translation_files = list(translation_dir.glob("*.md"))
            print(f"🌍 Translations: {len(translation_files)}")
        
        # Count research files
        research_dir = Path("data/research")
        if research_dir.exists():
            research_files = list(research_dir.glob("*.txt"))
            print(f"🔍 Research Files: {len(research_files)}")
            
        # Count generated images
        images_dir = Path("data/images/generated")
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            print(f"🖼️  Generated Images: {len(image_files)}")
        
        print("\n✅ Markdown pipeline completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in AI pipeline: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_latex_pipeline():
    """Run the LaTeX generation pipeline"""
    print("📚 Starting LaTeX Generation Pipeline...")
    print("=" * 60)
    
    try:
        # Generate LaTeX structure
        print("🏗️  Generating LaTeX structure...")
        result = subprocess.run([sys.executable, 'latex_generator.py'], 
                              capture_output=True, text=True, check=True)
        print("✅ LaTeX structure generated!")
        print(result.stdout)
        
        # Build PDF
        print("🔨 Building PDF...")
        result = subprocess.run(['./build_latex.sh'], 
                              capture_output=True, text=True, check=True)
        print("✅ PDF built successfully!")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in LaTeX pipeline: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Vegan Djerban Family Cookbook Pipeline')
    parser.add_argument('--markdown-only', action='store_true', 
                       help='Run only markdown generation (skip LaTeX)')
    parser.add_argument('--latex-only', action='store_true', 
                       help='Run only LaTeX generation (skip AI pipeline)')
    parser.add_argument('--full', action='store_true', 
                       help='Run complete pipeline (markdown + LaTeX)')
    
    args = parser.parse_args()
    
    # If no specific args, default to markdown only for now
    if not any([args.markdown_only, args.latex_only, args.full]):
        args.markdown_only = True
    
    print("🍽️  VEGAN DJERBAN FAMILY COOKBOOK PIPELINE")
    print("=" * 60)
    print("Preserving the culinary heritage of the Silver family")
    print("🇹🇳 Djerban Jewish → 🇲🇦 Tangier Jewish → 🌱 Modern Vegan")
    print("=" * 60)
    
    success = True
    
    if args.markdown_only or args.full:
        success &= run_markdown_pipeline()
    
    if (args.latex_only or args.full) and success:
        success &= run_latex_pipeline()
    
    if success:
        print("\n🎉 Pipeline completed successfully!")
        print("📁 Check the following directories:")
        print("   • data/recipes/ - Generated recipes and translations")
        print("   • data/research/ - Cultural and culinary research")
        print("   • data/images/generated/ - AI-generated food images")
        if args.latex_only or args.full:
            print("   • latex/output/ - Final PDF cookbook")
    else:
        print("\n❌ Pipeline failed. Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 