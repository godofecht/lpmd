#!/usr/bin/env python3
"""
Demo script showing how to view LPMD files with invisible syntax
"""

import os
import subprocess
import sys

def show_markdown_preview():
    """Show what markdown viewers see (simulated)"""
    print("🎨 Markdown Preview of literate_python.md")
    print("=" * 50)
    print()

    # Read the file and show only visible content
    with open('literate_python.md', 'r') as f:
        content = f.read()

    # Split by HTML comments and show content between them
    parts = content.split('<!--')
    for i, part in enumerate(parts):
        if '-->' in part:
            # This is content after an HTML comment
            visible_part = part.split('-->', 1)[1]
        else:
            # First part or content before comments
            visible_part = part

        # Print headers and content, skip code blocks for brevity
        lines = visible_part.split('\n')
        for line in lines[:10]:  # Show first 10 lines of each section
            if line.strip() and not line.startswith('```'):
                print(line)
                if len([l for l in lines if l.strip()]) > 3:
                    print("... (code blocks and content continue)")
                    break
        print()

def main():
    print("📖 How to View LPMD Files with Invisible Syntax")
    print("=" * 55)
    print()

    print("🔍 LPMD files use HTML comments (<!-- -->) to hide execution metadata.")
    print("Markdown viewers ignore these comments, so you see clean content!")
    print()

    print("🌟 What Markdown Viewers Show:")
    print("- ✅ Headers (# ## ###)")
    print("- ✅ Bold/italic text (**text**, *text*)")
    print("- ✅ Code blocks with syntax highlighting")
    print("- ✅ Lists, links, images")
    print("- ❌ LPMD cell markers (completely hidden)")
    print()

    if os.path.exists('literate_python.md'):
        show_markdown_preview()
    else:
        print("❌ literate_python.md not found in current directory")

    print("🛠️  Recommended Viewing Tools:")
    print("- VS Code: code literate_python.md")
    print("- GitHub: Upload or view in repository")
    print("- Browser: Use markdown viewer extensions")
    print("- Terminal: glow literate_python.md (if installed)")
    print()

    print("⚡ To execute: python lpmd_executor.py literate_python.md --yes")

if __name__ == "__main__":
    main()
