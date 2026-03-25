import re

# Read the clean HTML baseline
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_clean_baseline.html', 'r') as f:
    html = f.read()

# --- STEP 1: Define the final, robust HTML and CSS ---

# This version uses <img> tags pointing to the .svg files. Much safer.
final_header_html = """
<header class="header translucent">
    <nav class="header-nav">
        <a href="#" class="header-link">Shop</a>
        <a href="#" class="header-link">Collections</a>
        <a href="#" class="header-link">Journal</a>
    </nav>
    <div class="header-center">
        <div class="logo-container">
            <img src="assets/brands/jamrock/ILJ-LOGO-FINAL-WHITE.svg" alt="Jamrock" class="logo-svg logo-white">
            <img src="assets/brands/jamrock/ILJ-LOGO-FINAL.svg" alt="Jamrock" class="logo-svg logo-color">
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
<style id="robust-svg-overrides">
    /* Core Header Interaction */
    .header.translucent {
        position: absolute; top: 0; left: 0; width: 100%; z-index: 100;
        background-color: transparent; border-bottom: 1px solid transparent;
        transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out;
        padding: 24px 60px; /* Ensure padding is consistent */
    }
    .header.translucent:hover {
        background-color: #FFFFFF;
        border-bottom: 1px solid #e6e6e6;
    }

    /* Text & Icons Color Transition */
    .header.translucent .header-link, .header.translucent .header-icon {
        color: white;
        transition: color 0.3s ease-in-out;
        text-decoration: none;
    }
    .header.translucent:hover .header-link, .header.translucent:hover .header-icon {
        color: #111111;
    }

    /* SVG Logo Control via IMG tag */
    .logo-container {
        position: relative;
        /* Using vw for responsive scaling, clamped to prevent extremes */
        width: clamp(120px, 12vw, 180px);
        height: 60px; /* Give the container a consistent height */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-svg {
        position: absolute;
        width: 100%;
        height: 100%;
        object-fit: contain; /* This is key for SVGs in IMG tags */
        transition: opacity 0.3s ease-in-out;
    }

    /* SVG Logo Swap Logic */
    .logo-color { opacity: 0; }
    .logo-white { opacity: 1; }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }
</style>
<!-- Iconify Script for Icons -->
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
"""

# --- STEP 2: Perform the replacement ---
# Replace the original <header> with our new, robust version
html = re.sub(r'<header class="header">.*?</header>', final_header_html, html, flags=re.DOTALL)
# Inject the CSS before the </head> tag
html = html.replace('</head>', final_css_injection + '\n</head>')

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Definitive prototype (v8) has been built with robust IMG/SVG implementation.")
