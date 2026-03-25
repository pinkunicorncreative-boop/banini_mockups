import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# The CSS for the logo swap is the only thing that needs a slight modification.
# We will add z-index to ensure the stacking order is correct.

old_css_logic = """/* SVG Logo Swap Logic */
    .logo-color { opacity: 0; }
    .logo-white { opacity: 1; }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }"""

new_css_logic = """/* SVG Logo Swap Logic */
    .logo-color { opacity: 0; z-index: 1; }
    .logo-white { opacity: 1; z-index: 2; }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }"""

# Find and replace the block
html = html.replace(old_css_logic, new_css_logic)

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Prototype V9: z-index fix applied to logo swap.")
