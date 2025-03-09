#!/usr/bin/env python3
"""
Font optimization script for web use.
This script converts TTF fonts to WOFF2 format and optionally subsets them.
"""

import os
import argparse
import subprocess
import pathlib
from concurrent.futures import ThreadPoolExecutor

def ensure_tools_installed():
    """Check if required tools are installed."""
    try:
        # Check for fonttools
        subprocess.run(["pip", "show", "fonttools"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Installing fonttools...")
        subprocess.run(["pip", "install", "fonttools", "brotli"], check=True)
    
    print("All required tools are installed.")

def convert_to_woff2(font_path, output_dir=None, subset=False, subset_chars=None):
    """
    Convert a TTF font to WOFF2 format and optionally subset it.
    
    Args:
        font_path: Path to the TTF font file
        output_dir: Directory to save the optimized font (defaults to same directory)
        subset: Whether to subset the font
        subset_chars: Characters to include in the subset (defaults to Latin)
    """
    font_path = pathlib.Path(font_path)
    
    if output_dir:
        output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = font_path.parent
    
    output_path = output_dir / f"{font_path.stem}.woff2"
    
    # Base command for conversion
    cmd = ["pyftsubset", str(font_path), f"--output-file={output_path}", "--flavor=woff2"]
    
    # Add subsetting parameters if requested
    if subset:
        # Default to Latin character set if not specified
        if not subset_chars:
            subset_chars = "U+0000-00FF"  # Basic Latin + Latin-1 Supplement
        cmd.append(f"--unicodes={subset_chars}")
    else:
        # If not subsetting, we need to use a different approach
        cmd = ["fonttools", "ttLib.woff2", "compress", str(font_path), "-o", str(output_path)]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Converted {font_path.name} to WOFF2 format at {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting {font_path.name}: {e.stderr}")
        return None

def process_font_directory(directory, output_dir=None, subset=False, subset_chars=None):
    """Process all TTF and OTF fonts in a directory and organize them by family in the output directory."""
    directory = pathlib.Path(directory)
    font_files = list(directory.glob("**/*.[to]tf"))  # Include both TTF and OTF files
    
    if not font_files:
        print(f"No TTF or OTF fonts found in {directory}")
        return []
    
    print(f"Found {len(font_files)} TTF/OTF fonts in {directory}")
    
    converted_files = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for font_path in font_files:
            # Determine the family directory
            family_dir = font_path.parent.relative_to(directory)
            output_family_dir = output_dir / family_dir
            output_family_dir.mkdir(parents=True, exist_ok=True)
            
            # Submit the conversion task
            futures.append(
                executor.submit(convert_to_woff2, font_path, output_family_dir, subset, subset_chars)
            )
        
        for future in futures:
            result = future.result()
            if result:
                converted_files.append(result)
    
    return converted_files

def generate_css(converted_files, output_file="fonts.css"):
    """Generate a CSS file for the converted fonts."""
    output_file = pathlib.Path(output_file)
    
    css_content = """/* Optimized web fonts */
"""
    
    # Group fonts by family
    font_families = {}
    for font_path in converted_files:
        family_name = font_path.parent.name
        if family_name not in font_families:
            font_families[family_name] = []
        font_families[family_name].append(font_path)
    
    # Generate CSS for each font family
    for family, fonts in font_families.items():
        css_content += f"\n/* {family} */\n"
        
        for font in fonts:
            font_name = font.stem
            font_style = "italic" if "italic" in font_name.lower() else "normal"
            font_weight = "700" if "bold" in font_name.lower() else "400"
            
            css_content += f"""@font-face {{
    font-family: '{family}';
    src: url('{font.relative_to(output_file.parent)}') format('woff2');
    font-weight: {font_weight};
    font-style: {font_style};
    font-display: swap;
}}
"""
    
    with open(output_file, "w") as f:
        f.write(css_content)
    
    print(f"Generated CSS file at {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Optimize fonts for web use")
    parser.add_argument("--input", "-i", help="Input directory containing TTF fonts", default="rendercv_fonts")
    parser.add_argument("--output", "-o", help="Output directory for optimized fonts", default="web_fonts")
    parser.add_argument("--subset", "-s", action="store_true", help="Subset the fonts")
    parser.add_argument("--chars", "-c", help="Characters to include in subset (e.g., 'U+0000-00FF')")
    parser.add_argument("--css", help="Generate CSS file", default="web_fonts/fonts.css")
    
    args = parser.parse_args()
    
    ensure_tools_installed()
    
    output_dir = pathlib.Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converted_files = process_font_directory(
        args.input, output_dir, args.subset, args.chars
    )
    
    if converted_files and args.css:
        generate_css(converted_files, args.css)
    
    print(f"Font optimization complete. Optimized {len(converted_files)} fonts.")
    print(f"Original font directory: {args.input}")
    print(f"Optimized font directory: {args.output}")
    if args.css:
        print(f"CSS file: {args.css}")

if __name__ == "__main__":
    main() 