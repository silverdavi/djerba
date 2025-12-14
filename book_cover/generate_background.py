#!/usr/bin/env python3
"""Generate a decorative background image for the book cover using Gemini."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from google import genai
from google.genai import types
import os

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env")
        return
    
    print(f"✅ API key loaded: {api_key[:10]}...")
    
    client = genai.Client(api_key=api_key)
    
    prompt = """Generate an image: A seamless decorative background pattern for a cookbook cover. 
The pattern features subtle, elegant illustrations of Mediterranean and North African culinary ingredients:
olive branches, pomegranates, figs, dates, wheat stalks, almonds, lemons, mint leaves, and traditional ceramic tagine pots.
The style is delicate line art in warm terracotta and gold tones on a cream/parchment colored background.
The pattern should be subtle enough to allow text overlay. No text in the image.
Vintage botanical illustration style. Soft, muted earth tones.
High resolution, detailed but not busy. Professional cookbook aesthetic.
Wide panoramic format suitable for a book cover spread (front + spine + back)."""

    print("🎨 Generating cover background image with Gemini 3 Pro...")
    
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["image", "text"],
            temperature=1.0,
        ),
    )

    output_path = Path(__file__).parent / "background.png"
    
    # Extract image from response
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                img_data = part.inline_data.data
                output_path.write_bytes(img_data)
                print(f"✅ Background saved: {output_path}")
                return
    
    print("❌ No image in response")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
