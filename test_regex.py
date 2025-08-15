import re

# Test the problematic patterns
text = "2 BHK apartments under 1 crore in Mumbai"

# Test price patterns
price_patterns = [
    r'(?:under|below|less\s+than)\s+(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
    r'(?:above|over|more\s+than)\s+(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
    r'(?:>=?)\s*(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
    r'(?:<=?)\s*(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
    r'(?:>)\s*(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
    r'(?:<)\s*(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
    r'(?:=)\s*(\d{1,}(?:\.\d+)?)\s*(?:cr|crore|crores|lakh|lakhs|thousand|thousands)',
]

print("Testing price patterns:")
for i, pattern in enumerate(price_patterns):
    try:
        matches = re.finditer(pattern, text.lower())
        for match in matches:
            print(f"Pattern {i+1} matched: '{match.group(0)}'")
    except Exception as e:
        print(f"Pattern {i+1} failed: {e}")

# Test area patterns
area_patterns = [
    r'carpet\s+area\s+(?:under|below|less\s+than)\s+(\d{3,5})\s*sqft',
    r'carpet\s+area\s+(?:above|over|more\s+than)\s+(\d{3,5})\s*sqft',
    r'carpet\s+area\s+between\s+(\d{3,5})\s*(?:to|-)\s*(\d{3,5})\s*sqft',
    r'carpet\s+area\s*>=?\s*(\d{3,5})\s*sqft',
    r'carpet\s+area\s*<=?\s*(\d{3,5})\s*sqft',
    r'carpet\s+area\s*>\s*(\d{3,5})\s*sqft',
    r'carpet\s+area\s*<\s*(\d{3,5})\s*sqft',
    r'carpet\s+area\s*=\s*(\d{3,5})\s*sqft',
    r'carpet\s+area\s+(\d{3,5})\s*sqft',
]

print("\nTesting area patterns:")
for i, pattern in enumerate(area_patterns):
    try:
        matches = re.finditer(pattern, text.lower())
        for match in matches:
            print(f"Pattern {i+1} matched: '{match.group(0)}'")
    except Exception as e:
        print(f"Pattern {i+1} failed: {e}")
