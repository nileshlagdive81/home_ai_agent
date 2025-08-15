import re

# Test the patterns manually
text = "carpet area less than 1400"
text_lower = text.lower()

print(f"Testing text: '{text_lower}'")
print("=" * 50)

# Test the specific pattern that should match
pattern = r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d+)'
print(f"Testing pattern: {pattern}")

match = re.search(pattern, text_lower)
if match:
    print(f"✅ MATCHED: '{match.group(0)}'")
    print(f"   Captured: '{match.group(1)}'")
else:
    print("❌ NO MATCH")

print("\n" + "=" * 50)

# Test all patterns
carpet_area_patterns = [
    # Original patterns with sqft
    r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d+)\s*sqft',
    r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d+)\s*sqft',
    r'carpet\s+area\s+between\s+(\d+)\s*(?:to|-)\s*(\d+)\s*sqft',
    r'carpet\s+area\s*>=?\s*(\d+)\s*sqft',
    r'carpet\s+area\s*<=?\s*(\d+)\s*sqft',
    r'carpet\s+area\s*>\s*(\d+)\s*sqft',
    r'carpet\s+area\s*<\s*(\d+)\s*sqft',
    r'area\s+(?:under|below|less\s+than)\s+(\d+)\s*sqft',
    r'area\s+(?:above|over|more\s+than)\s+(\d+)\s*sqft',
    r'area\s+between\s+(\d+)\s*(?:to|-)\s*(\d+)\s*sqft',
    r'area\s*>=?\s*(\d+)\s*sqft',
    r'area\s*<=?\s*(\d+)\s*sqft',
    r'area\s*>\s*(\d+)\s*sqft',
    r'area\s*<\s*(\d+)\s*sqft',
    r'(\d+)\s*sqft\s+(?:and\s+)?(?:above|below|under|over)',
    r'(\d+)\s*sqft\s+to\s+(\d+)\s*sqft',
    
    # NEW: Flexible patterns without requiring "sqft"
    r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d+)',
    r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d+)',
    r'carpet\s+area\s+between\s+(\d+)\s*(?:to|-)\s*(\d+)',
    r'carpet\s+area\s*>=?\s*(\d+)',
    r'carpet\s+area\s*<=?\s*(\d+)',
    r'carpet\s+area\s*>\s*(\d+)',
    r'carpet\s+area\s*<\s*(\d+)',
    r'carpet\s+area\s*=\s*(\d+)',
    r'carpet\s+area\s+(\d+)',
    
    # NEW: Flexible area patterns without requiring "sqft"
    r'area\s+(?:under|below|less\s+than)\s+(\d+)',
    r'area\s+(?:above|over|more\s+than)\s+(\d+)',
    r'area\s+between\s+(\d+)\s*(?:to|-)\s*(\d+)',
    r'area\s*>=?\s*(\d+)',
    r'area\s*<=?\s*(\d+)',
    r'area\s*>\s*(\d+)',
    r'area\s*<\s*(\d+)',
    r'area\s*=\s*(\d+)',
    r'area\s+(\d+)',
    
    # NEW: Number followed by area-related keywords (assume sqft)
    r'(\d+)\s+(?:sqft|sq\s*ft|square\s*feet|square\s*foot)',
    r'(\d+)\s+(?:and\s+)?(?:above|below|under|over)',
    r'(\d+)\s+to\s+(\d+)',
    
    # NEW: Context-based patterns for area queries
    r'(?:less\s+than|under|below)\s+(\d+)',
    r'(?:more\s+than|above|over)\s+(\d+)',
    r'(\d+)\s+(?:or\s+)?(?:less|below|under)',
    r'(\d+)\s+(?:or\s+)?(?:more|above|over)'
]

print("Testing all patterns:")
for i, pattern in enumerate(carpet_area_patterns):
    match = re.search(pattern, text_lower)
    if match:
        print(f"✅ Pattern {i+1}: '{pattern}'")
        print(f"   Matched: '{match.group(0)}'")
        print(f"   Captured: '{match.group(1)}'")
        break
else:
    print("❌ No patterns matched!")
