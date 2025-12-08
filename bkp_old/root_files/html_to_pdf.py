#!/usr/bin/env python3
"""
Convert HTML recipe to PDF using weasyprint or headless chrome
"""

import subprocess
import sys
import os
from pathlib import Path

def convert_html_to_pdf_weasyprint(html_path, pdf_path):
    """Convert HTML to PDF using WeasyPrint."""
    try:
        import weasyprint
        print(f"Converting {html_path} to {pdf_path} using WeasyPrint...")
        weasyprint.HTML(html_path).write_pdf(pdf_path)
        print(f"✓ PDF created: {pdf_path}")
        return True
    except ImportError:
        print("WeasyPrint not installed. Trying alternative methods...")
        return False
    except Exception as e:
        print(f"Error with WeasyPrint: {e}")
        return False

def convert_html_to_pdf_chromium(html_path, pdf_path):
    """Convert HTML to PDF using headless Chrome/Chromium."""
    try:
        # Check if chromium or google-chrome is available
        chrome_cmd = None
        for cmd in ['chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable']:
            result = subprocess.run(['which', cmd], capture_output=True)
            if result.returncode == 0:
                chrome_cmd = cmd
                break
        
        if not chrome_cmd:
            print("Chrome/Chromium not found")
            return False
        
        print(f"Converting {html_path} to {pdf_path} using {chrome_cmd}...")
        abs_html_path = os.path.abspath(html_path)
        abs_pdf_path = os.path.abspath(pdf_path)
        
        cmd = [
            chrome_cmd,
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + abs_pdf_path,
            'file://' + abs_html_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ PDF created: {pdf_path}")
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error with Chrome: {e}")
        return False

def convert_html_to_pdf_playwright(html_path, pdf_path):
    """Convert HTML to PDF using Playwright."""
    try:
        from playwright.sync_api import sync_playwright
        
        print(f"Converting {html_path} to {pdf_path} using Playwright...")
        abs_html_path = os.path.abspath(html_path)
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 800, "height": 800})
            page.goto(f'file://{abs_html_path}')
            page.pdf(path=pdf_path)
            browser.close()
        
        print(f"✓ PDF created: {pdf_path}")
        return True
    except ImportError:
        print("Playwright not installed")
        return False
    except Exception as e:
        print(f"Error with Playwright: {e}")
        return False

def main():
    html_file = '/Users/davidsilver/dev/private/RecipeDjerba/mhamsa_recipe_4page.html'
    pdf_file = '/Users/davidsilver/dev/private/RecipeDjerba/mhamsa_recipe_4page.pdf'
    
    if not os.path.exists(html_file):
        print(f"Error: HTML file not found: {html_file}")
        sys.exit(1)
    
    # Try multiple conversion methods in order of preference
    methods = [
        ('WeasyPrint', convert_html_to_pdf_weasyprint),
        ('Chromium/Chrome', convert_html_to_pdf_chromium),
        ('Playwright', convert_html_to_pdf_playwright),
    ]
    
    for method_name, method_func in methods:
        print(f"\nTrying {method_name}...")
        if method_func(html_file, pdf_file):
            print(f"\n✓ Successfully created PDF: {pdf_file}")
            sys.exit(0)
    
    print("\n✗ All conversion methods failed. Please install one of:")
    print("  pip install weasyprint")
    print("  pip install playwright && playwright install")
    print("  Or install Chrome/Chromium manually")
    sys.exit(1)

if __name__ == '__main__':
    main()

