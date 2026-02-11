#!/usr/bin/env python3
"""
Simple test to verify LPMD HTML generation works
"""

from lpmd_standalone_html import LPMDStandaloneHTMLGenerator

# Create a simple test LPMD content
test_content = '''# Simple Test

<!-- cell:test -->
```python
print("Hello from LPMD!")
x = 42
result = x * 2
print(f"Result: {result}")
```
'''

# Write test file
with open('test_simple.md', 'w') as f:
    f.write(test_content)

# Generate HTML
generator = LPMDStandaloneHTMLGenerator()
if generator.parse_lpmd_file('test_simple.md'):
    generator.generate_standalone_html('test_simple.html')
    print("✅ Generated test_simple.html")
    print("📖 Open test_simple.html in browser to test execution!")
else:
    print("❌ Failed to parse test file")
