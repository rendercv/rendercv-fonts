# rendercv-fonts

A Python package with some fonts for the `rendercv` package.

## Font Optimization for Web Use

This repository includes a script to optimize fonts for web use. The script converts TTF fonts to WOFF2 format, which provides better compression and faster loading times. It can also subset fonts to include only the characters you need, further reducing file size.

### Prerequisites

- Python 3.10 or higher
- `fonttools` and `brotli` (the script will install these if they're not already installed)

### Usage

```bash
# Basic usage (converts all TTF fonts to WOFF2)
python optimize_fonts.py

# Convert and subset fonts to include only Latin characters
python optimize_fonts.py --subset

# Convert and subset fonts with custom character set
python optimize_fonts.py --subset --chars="U+0000-00FF,U+0131,U+0152-0153"

# Specify custom input and output directories
python optimize_fonts.py --input=my_fonts --output=optimized_fonts
```

### Options

- `--input`, `-i`: Input directory containing TTF fonts (default: "rendercv_fonts")
- `--output`, `-o`: Output directory for optimized fonts (default: "web_fonts")
- `--subset`, `-s`: Subset the fonts to reduce file size
- `--chars`, `-c`: Characters to include in subset (e.g., 'U+0000-00FF')
- `--css`: Path to generate CSS file (default: "web_fonts/fonts.css")

### Web Font Best Practices

1. **Use WOFF2 Format**: WOFF2 offers 30-50% better compression than TTF/OTF.
2. **Subset Fonts**: Only include the characters you need to reduce file size.
3. **Use Font Display**: The generated CSS includes `font-display: swap` for better loading behavior.
4. **Preload Critical Fonts**: Consider adding `<link rel="preload">` for critical fonts.
5. **Self-Host Fonts**: Self-hosting gives you more control over caching and performance.

### Example CSS Usage

```html
<link rel="stylesheet" href="web_fonts/fonts.css" />
<style>
  body {
    font-family: "Open Sans", sans-serif;
  }
  h1,
  h2,
  h3 {
    font-family: "Raleway", sans-serif;
  }
</style>
```
