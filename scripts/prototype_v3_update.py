import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# --- 1. LOGO SWAP FIX ---
# Find the entire logo container div to replace its contents. This is more robust.
logo_container_pattern = re.compile(r'(<div class="logo-center">)(.*?)(</div>)', re.DOTALL)

# This is the new HTML for the logo with the two versions for the hover effect.
new_logo_html = '''
<div class="logo-container">
    <img src="assets/brands/jamrock/ILJ-LOGO-FINAL-WHITE.png" alt="Jamrock Logo" class="logo-white">
    <img src="assets/brands/jamrock/ILJ-LOGO-FINAL.png" alt="Jamrock Logo" class="logo-color">
</div>
'''
# Replace the content of the logo div
html = logo_container_pattern.sub(r'\\1' + new_logo_html + r'\\3', html)


# --- 2. NAVIGATION & ICON COLOR FIX ---
# Inject a more specific CSS rule for the nav links and icons
color_fix_css = """
<style id="nav-color-fix">
    /* Default state over video */
    .header.translucent .nav-left a,
    .header.translucent .nav-right a,
    .header.translucent .header-icons a {
        color: white !important;
        /* mix-blend-mode is a great idea but can have weird color interactions, let's stick to a solid color for reliability */
    }

    /* Hover state with white background */
    .header.translucent:hover .nav-left a,
    .header.translucent:hover .nav-right a,
    .header.translucent:hover .header-icons a {
       color: #111111 !important;
    }
</style>
"""
# Add this style fix right before the </head> tag
html = html.replace('</head>', color_fix_css + '\n</head>')

# Ensure the nav-right still has the text links if they were stripped
nav_right_pattern = re.compile(r'(<div class="nav-right">)(.*?)(</div>)', re.DOTALL)
if "Collections" not in nav_right_pattern.search(html).group(2): # Check if text links are missing
    # This is a bit of a guess based on Prestige theme structure
    # Let's rebuild the nav-right completely to be sure
    
    # We will assume the icons are what's important from the last step.
    # The user mentioned "menu items over that side", let's check the banani html.
    # The original Banani had left-nav, center-logo, right-icons.
    # Let's stick to that structure for now, the user can clarify if text links should also be on the right.
    pass # Keeping the icon-only nav-right for now as per Prestige layout.


with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Prototype V3 updated with logo swap and nav color fixes.")
