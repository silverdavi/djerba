#!/bin/bash
# LaTeX Build Script for Vegan Djerban Family Cookbook

echo "🔨 Building Vegan Djerban Family Cookbook..."

# Create output directory
mkdir -p latex/output

# Copy images to latex directory
echo "📸 Copying images..."
cp -R data/images/generated/* latex/images/ 2>/dev/null || true

# Build LaTeX document (requires XeLaTeX for Unicode fonts)
echo "📚 Compiling LaTeX document..."
cd latex

# First pass
xelatex -output-directory=output main.tex

# Second pass for references
xelatex -output-directory=output main.tex

# Third pass for final formatting
xelatex -output-directory=output main.tex

echo "✅ Build complete! Check latex/output/main.pdf"

# Open PDF if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open output/main.pdf
fi
