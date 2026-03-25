import re

# Read the clean HTML baseline
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_clean_baseline.html', 'r') as f:
    html = f.read()

# Read the raw content of the SVG files
try:
    with open('/Users/krazeerastagroup/.openclaw/workspace/assets/brands/jamrock/ILJ-LOGO-FINAL-WHITE.svg', 'r') as f:
        svg_white_content = f.read()
    with open('/Users/krazeerastagroup/.openclaw/workspace/assets/brands/jamrock/ILJ-LOGO-FINAL.svg', 'r') as f:
        svg_color_content = f.read()
except FileNotFoundError:
    print("Error: SVG files not found. Please ensure they are in assets/brands/jamrock/")
    exit()

# --- STEP 1: Define the final SVG header and CSS ---

final_header_html = f"""
<header class="header translucent">
    <nav class="header-nav">
        <span class="header-link">Shop</span>
        <span class="header-link">Collections</span>
        <span class="header-link">Journal</span>
    </nav>
    <div class="header-center">
        <div class="logo-container">
            <div class="logo-svg logo-white">{svg_white_content}</div>
            <div class="logo-svg logo-color">{svg_color_content}</div>
        </div>
    </div>
    <div class="header-nav right">
        <a href="#" class="header-icon">
            <iconify-icon icon="lucide:search" style="font-size: 20px;"></iconify-icon>
        </a>
        <a href="#" class="header-icon">
            <iconify-icon icon="lucide:user" style="font-size: 20px;"></iconify-icon>
        </a>
        <a href="#" class="header-icon" style="display: flex; align-items: center; gap: 8px;">
            <iconify-icon icon="lucide:shopping-bag" style="font-size: 20px;"></iconify-icon>
            <span style="font-size: 13px; font-weight: 500;">0</span>
        </a>
    </div>
</header>
"""

final_css_injection = """
<style id="svg-art-direction-overrides">
    /* Core Header Interaction */
    .header.translucent {{
        position: absolute; top: 0; left: 0; width: 100%; z-index: 100;
        background-color: transparent; border-bottom: 1px solid transparent;
        transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out;
    }}
    .header.translucent:hover {{
        background-color: #FFFFFF;
        border-bottom: 1px solid #e6e6e6;
    }}

    /* Text & Icons Color Transition */
    .header.translucent .header-link, .header.translucent .header-icon {{
        color: white;
        transition: color 0.3s ease-in-out;
    }}
    .header.translucent:hover .header-link, .header.translucent:hover .header-icon {{
        color: #111111;
    }}

    /* SVG Logo Control */
    .logo-container {{
        position: relative;
        /* Use viewport width for responsive scaling. 4vw means 4% of the window's width. */
        /* Use min/max to prevent it from getting too small or too big. */
        width: clamp(120px, 12vw, 180px);
        height: auto;
    }}
    .logo-svg {{
        transition: opacity 0.3s ease-in-out;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
    }}
    .logo-svg svg {{
        width: 100%;
        height: auto;
        display: block;
    }}

    /* SVG Logo Swap Logic */
    .logo-color {{ opacity: 0; }}
    .logo-white {{ opacity: 1; }}
    .header.translucent:hover .logo-color {{ opacity: 1; }}
    .header.translucent:hover .logo-white {{ opacity: 0; }}
</style>
<!-- Iconify Script for Icons -->
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
"""

# --- STEP 2: Perform the replacement ---
html = re.sub(r'<header class="header">.*?</header>', final_header_html, html, flags=re.DOTALL)
html = html.replace('</head>', final_css_injection + '\n</head>')

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Definitive prototype (v7) has been built with responsive SVG logos.")
