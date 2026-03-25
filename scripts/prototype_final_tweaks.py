import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# --- 1. Restructure the HTML ---
# Find the announcement bar and the header to wrap them.
body_content_pattern = re.compile(r'(<div class="prestige-theme">)(.*?)(</div>)', re.DOTALL)
body_content_match = body_content_pattern.search(html)

if body_content_match:
    inner_html = body_content_match.group(2)
    
    announcement_pattern = re.compile(r'<div class="announcement">.*?</div>', re.DOTALL)
    header_pattern = re.compile(r'<header class="header translucent">.*?</header>', re.DOTALL)
    
    announcement_html = announcement_pattern.search(inner_html).group(0)
    header_html = header_pattern.search(inner_html).group(0)
    
    # Remove them from their original position
    inner_html = announcement_pattern.sub('', inner_html)
    inner_html = header_pattern.sub('', inner_html)
    
    # Prepend them in the correct, new structure
    new_top_structure = f"""
    <div class="site-header-container">
        {announcement_html}
        {header_html}
    </div>
    """
    inner_html = new_top_structure + inner_html
    
    # Reassemble the body
    html = body_content_match.group(1) + inner_html + body_content_match.group(3)


# --- 2. Inject the final CSS tweaks ---
final_tweaks_css = """
<style id="final-tweaks">
    /* Make announcement bar a permanent fixture */
    .announcement {
        position: relative;
        z-index: 101; /* Higher than the header */
    }
    /* Adjust header to sit below the announcement bar */
    .header.translucent {
        /* Calculate top based on a typical announcement bar height */
        /* This can be made dynamic with JS later if needed */
        top: 37px;
    }

    /* Set the white logo's default opacity to 70% */
    .logo-white {
        opacity: 0.7;
        z-index: 2;
    }
</style>
"""

# Inject this block after our main style block
html = html.replace('</style>\n<!-- Iconify Script for Icons -->', '</style>' + final_tweaks_css + '\n<!-- Iconify Script for Icons -->')

# Also, need to adjust the hero pull-up to account for the announcement bar
# Original header height was ~90px. Annuncement is ~37px. Total ~127px.
html = html.replace('<h1 class="hero-title">', '<style>.hero{margin-top:0 !important;}</style><h1 class="hero-title">', 1)
# And the absolute header should now be inside a relative container.
html = html.replace('<div class="site-header-container">', '<div class="site-header-container" style="position: relative; z-index: 100;">')


with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Final tweaks (opacity and announcement bar) have been applied.")
