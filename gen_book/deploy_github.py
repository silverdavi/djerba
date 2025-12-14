#!/usr/bin/env python3
"""
Deploy Silver Cooks Flipbook to GitHub Pages

This script:
1. Creates a deployment folder with all necessary files
2. Copies flipbook files (index.html, JS, CSS)
3. Copies recipe HTML pages to recipes/
4. Copies recipe images to images/
5. Copies ingredient images to images/ingredients/
6. Fixes image paths in HTML files
7. Generates/updates search-index.json
8. Optionally commits and pushes to silverdavi/silvercooks repo
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).parent.parent
GEN_BOOK = ROOT / "gen_book"
FLIPBOOK_SRC = GEN_BOOK / "flipbook"
WEB_SRC = GEN_BOOK / "output" / "web"
IMAGES_SRC = ROOT / "data" / "images" / "current"
INGREDIENTS_SRC = ROOT / "data" / "images" / "ingredients" / "final"
DEPLOY_DIR = ROOT / "deploy"

# GitHub config
GITHUB_USER = "silverdavi"
GITHUB_REPO = "silvercooks"
GITHUB_REMOTE = f"git@github.com:{GITHUB_USER}/{GITHUB_REPO}.git"
CNAME = "silvercooks.com"


def clean_deploy_dir():
    """Remove and recreate deploy directory."""
    if DEPLOY_DIR.exists():
        print(f"  Removing existing {DEPLOY_DIR.name}/...")
        shutil.rmtree(DEPLOY_DIR)
    DEPLOY_DIR.mkdir(parents=True)
    print(f"  ✓ Created {DEPLOY_DIR}/")


def get_build_timestamp() -> str:
    """Generate build timestamp string."""
    now = datetime.now()
    return now.strftime("Built %b %d, %Y at %H:%M")


def copy_flipbook_files():
    """Copy flipbook HTML, JS, CSS files."""
    print("\n  Copying flipbook files...")
    build_timestamp = get_build_timestamp()
    
    for filename in ["index.html", "viewer.js", "viewer.css", "search-index.json"]:
        src = FLIPBOOK_SRC / filename
        if src.exists():
            if filename == "index.html":
                # Inject build timestamp
                content = src.read_text(encoding="utf-8")
                content = content.replace("<!-- BUILD_TIMESTAMP -->", build_timestamp)
                (DEPLOY_DIR / filename).write_text(content, encoding="utf-8")
            else:
                shutil.copy(src, DEPLOY_DIR / filename)
            print(f"    ✓ {filename}")
        else:
            print(f"    ⚠ Missing: {filename}")
    
    print(f"    📅 {build_timestamp}")
    
    # Copy assets folder if exists
    assets_src = FLIPBOOK_SRC / "assets"
    if assets_src.exists():
        shutil.copytree(assets_src, DEPLOY_DIR / "assets")
        print(f"    ✓ assets/")
    
    # Copy GitHub Actions workflow
    workflow_src = FLIPBOOK_SRC / ".github" / "workflows" / "deploy.yml"
    if workflow_src.exists():
        workflow_dest = DEPLOY_DIR / ".github" / "workflows"
        workflow_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(workflow_src, workflow_dest / "deploy.yml")
        print(f"    ✓ .github/workflows/deploy.yml")


def copy_recipe_pages():
    """Copy individual recipe HTML pages with fixed image paths."""
    print("\n  Copying recipe pages...")
    recipes_dir = DEPLOY_DIR / "recipes"
    recipes_dir.mkdir()
    
    count = 0
    for html_file in sorted(WEB_SRC.glob("*.html")):
        if html_file.name != "index.html":
            # Read and fix paths
            content = html_file.read_text(encoding="utf-8")
            fixed_content = fix_image_paths(content)
            
            # Write to deploy folder
            dest = recipes_dir / html_file.name
            dest.write_text(fixed_content, encoding="utf-8")
            count += 1
    
    print(f"    ✓ {count} recipe HTML files (paths fixed)")


def fix_image_paths(html_content: str) -> str:
    """Fix image paths in HTML for web deployment."""
    content = html_content
    
    # Fix dish image paths: ../images/current/{id}/dish.png -> ../images/{id}.png
    content = re.sub(
        r'src="\.\.?/images/current/([^/]+)/dish\.png"',
        r'src="../images/\1.png"',
        content
    )
    
    # Fix dish image paths: ../images/generated/current/{id}/dish.png -> ../images/{id}.png
    content = re.sub(
        r'src="[^"]*?/images/generated/current/([^/]+)/dish\.png"',
        r'src="../images/\1.png"',
        content
    )
    
    # Fix ingredient paths: /absolute/path/.../ingredients/final/{name}.png -> ../images/ingredients/{name}.png
    content = re.sub(
        r'src="[^"]*?/ingredients/final/([^"]+\.png)"',
        r'src="../images/ingredients/\1"',
        content
    )
    
    # Also fix file:// URLs that might be in there
    content = re.sub(
        r'src="file://[^"]*?/ingredients/final/([^"]+\.png)"',
        r'src="../images/ingredients/\1"',
        content
    )
    
    content = re.sub(
        r'src="file://[^"]*?/current/([^/]+)/dish\.png"',
        r'src="../images/\1.png"',
        content
    )
    
    return content


def copy_images():
    """Copy recipe dish images."""
    print("\n  Copying dish images...")
    images_dir = DEPLOY_DIR / "images"
    images_dir.mkdir()
    
    count = 0
    total_size = 0
    
    if IMAGES_SRC.exists():
        for recipe_folder in sorted(IMAGES_SRC.iterdir()):
            if recipe_folder.is_dir():
                dish_img = recipe_folder / "dish.png"
                if dish_img.exists():
                    # Copy with recipe_id as filename
                    dest = images_dir / f"{recipe_folder.name}.png"
                    shutil.copy(dish_img, dest)
                    count += 1
                    total_size += dish_img.stat().st_size
    
    size_mb = total_size / (1024 * 1024)
    print(f"    ✓ {count} dish images ({size_mb:.1f} MB)")


def copy_ingredient_images():
    """Copy ingredient decoration images."""
    print("\n  Copying ingredient images...")
    ingredients_dir = DEPLOY_DIR / "images" / "ingredients"
    ingredients_dir.mkdir(parents=True, exist_ok=True)
    
    count = 0
    total_size = 0
    
    if INGREDIENTS_SRC.exists():
        for img_file in sorted(INGREDIENTS_SRC.glob("*.png")):
            dest = ingredients_dir / img_file.name
            shutil.copy(img_file, dest)
            count += 1
            total_size += img_file.stat().st_size
    
    size_mb = total_size / (1024 * 1024)
    print(f"    ✓ {count} ingredient images ({size_mb:.1f} MB)")


def create_cname():
    """Create CNAME file for custom domain."""
    cname_path = DEPLOY_DIR / "CNAME"
    cname_path.write_text(CNAME)
    print(f"\n  ✓ CNAME ({CNAME})")


def create_nojekyll():
    """Create .nojekyll file to disable Jekyll processing."""
    (DEPLOY_DIR / ".nojekyll").touch()
    print("  ✓ .nojekyll")


def create_readme():
    """Create README for the deployment repo."""
    readme = f"""# Silver Cooks - Four-Language Cookbook

A plant-based cookbook with recipes from Djerba & Tangier, presented in four languages:
Hebrew, Arabic, Spanish, and English.

## Live Site

Visit: [https://{CNAME}](https://{CNAME}) or [https://{GITHUB_USER}.github.io/{GITHUB_REPO}](https://{GITHUB_USER}.github.io/{GITHUB_REPO})

## About

This cookbook preserves recipes from two North African Jewish family lines:
- **Cohen-Trabelsi** family from Djerba, Tunisia
- **Kadoch-Muyal** family from Tangier, Morocco

All recipes have been adapted for plant-based cooking.

## Authors

David & Enny Silver

---

*Deployed automatically from [RecipeDjerba](https://github.com/{GITHUB_USER}/RecipeDjerba)*
"""
    (DEPLOY_DIR / "README.md").write_text(readme)
    print("  ✓ README.md")


def git_init_and_push(push: bool = False):
    """Initialize git repo and optionally push to GitHub."""
    print("\n  Initializing git repository...")
    os.chdir(DEPLOY_DIR)
    
    # Initialize
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Deploy Silver Cooks flipbook"], check=True, capture_output=True)
    print("    ✓ Git initialized and committed")
    
    if push:
        print(f"    Pushing to {GITHUB_USER}/{GITHUB_REPO}...")
        subprocess.run(["git", "remote", "add", "origin", GITHUB_REMOTE], check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True, capture_output=True)
        result = subprocess.run(["git", "push", "-u", "-f", "origin", "main"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    ✓ Pushed to GitHub!")
            print(f"\n  Site will be available at:")
            print(f"    https://{GITHUB_USER}.github.io/{GITHUB_REPO}/")
        else:
            print(f"    ❌ Push failed: {result.stderr}")
    else:
        print(f"    (Run with --push to push to GitHub)")


def main():
    push = "--push" in sys.argv
    
    print("=" * 50)
    print("Silver Cooks Flipbook Deployment")
    print("=" * 50)
    
    print("\n1. Preparing deployment directory...")
    clean_deploy_dir()
    
    print("\n2. Copying files...")
    copy_flipbook_files()
    copy_recipe_pages()
    copy_images()
    copy_ingredient_images()
    
    print("\n3. Creating deployment files...")
    create_cname()
    create_nojekyll()
    create_readme()
    
    print("\n4. Git setup...")
    git_init_and_push(push=push)
    
    print("\n" + "=" * 50)
    print("Deployment package ready!")
    print(f"  Location: {DEPLOY_DIR}/")
    
    if not push:
        print("\nNext steps:")
        print(f"  1. Create repo: https://github.com/new (name: {GITHUB_REPO})")
        print(f"  2. Run: python deploy_github.py --push")
        print(f"  3. Enable GitHub Pages in repo settings")


if __name__ == "__main__":
    main()

