import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# The CSS for the logo swap is being ignored. Let's make it impossible to ignore.

old_css_block = """/* SVG Logo Swap Logic */
    .logo-color { opacity: 0; z-index: 1; }
    .logo-white { opacity: 1; z-index: 2; }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }"""

# This is a horrible, ugly, but extremely specific selector.
# If this doesn't work, the problem is not CSS specificity.
new_css_block = """/* SVG Logo Swap Logic - Forceful Override */
    .logo-color { opacity: 0; z-index: 1; }
    .logo-white { opacity: 1; z-index: 2; }

    body .prestige-theme header.header.translucent:hover .logo-container .logo-svg.logo-color {
        opacity: 1 !important;
    }
    body .prestige-theme header.header.translucent:hover .logo-container .logo-svg.logo-white {
        opacity: 0 !important;
    }
    """

# Find and replace the block
html = html.replace(old_css_block, new_css_block)

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Prototype V10: Forced CSS override applied.")
