# Silver Cooks - Book Cover

## Dimensions

- **Page size**: 8" × 8" (square format, matching interior)
- **Spine width**: 0.7" (~350 pages at 0.002" per page)
- **Bleed**: 0.125" on all sides
- **Total cover size**: 16.95" × 8.25" (with bleed)

## Files

- `cover.tex` - LaTeX source (requires LuaLaTeX for font support)
- `cover.pdf` - Generated PDF cover
- `build.sh` - Build script

## Building

```bash
./build.sh
```

Or manually:
```bash
lualatex cover.tex
```

## Requirements

- TexLive or MacTeX with LuaLaTeX
- Fonts: EB Garamond, Cinzel, David Libre, Noto Sans Arabic

## Adjusting Spine Width

For different page counts, adjust `\spinewidth` in `cover.tex`:
- 300 pages → 0.6"
- 350 pages → 0.7"
- 400 pages → 0.8"

Formula: pages × 0.002" (for standard 80gsm paper)

## Print Specifications

When sending to printer:
1. Ensure bleed marks are included
2. Use CMYK color mode for professional printing
3. Minimum 300 DPI for any raster elements

