#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Find all HTML files
html_files = list(Path('.').glob('*.html'))
html_files = [f for f in html_files if f.name != 'index.html']  # Skip our index.html

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove contenteditable attributes
        content = re.sub(r'\s+contenteditable="[^"]*"', '', content)
        content = re.sub(r"\s+contenteditable='[^']*'", '', content)
        
        # Remove class="is-html-mode" which is Adobe Campaign editor specific
        content = re.sub(r'\s+class="is-html-mode"', '', content)
        
        # Remove data-nl-* attributes (Adobe Campaign specific metadata)
        content = re.sub(r'\s+data-nl-[^=]*="[^"]*"', '', content)
        
        # Remove acr-block spans that wrap content (including multiline)
        content = re.sub(r'<span[^>]*class="acr-block[^"]*"[^>]*>(.*?)</span>', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'<span[^>]*class="[^"]*acr-block[^"]*"[^>]*>(.*?)</span>', r'\1', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {file_path.name}")
        else:
            print(f"- No changes needed: {file_path.name}")
    
    except Exception as e:
        print(f"✗ Error processing {file_path.name}: {e}")

print("\nDone!")
