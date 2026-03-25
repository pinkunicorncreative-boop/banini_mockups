import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_clean_baseline.html', 'r') as f:
    html = f.read()

# --- STEP 1: Define the final, correct HTML components ---

# This is the full, correct header structure we want to build.
# It uses the classes from the Banani export for consistency.
final_header_html = """
<header class="header translucent">
    <nav class="header-nav">
        <span class="header-link">Shop</span>
        <span class="header-link">Collections</span>
        <span class="header-link">Journal</span>
    </nav>
    <div class="header-center">
        <div class="logo-container">
            <img src="assets/brands/jamrock/ILJ-LOGO-FINAL-WHITE.png" alt="Jamrock" class="logo-white">
            <img src="assets/brands/jamrock/ILJ-LOGO-FINAL.png" alt="Jamrock" class="logo-color">
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

# This is the CSS that controls all the interactive magic.
final_css_injection = """
<style id="art-direction-overrides">
    /* Core Interaction: Header starts transparent, becomes solid white on hover */
    .header.translucent {
        position: absolute; /* Changed from sticky to absolute for video overlay */
        top: 0;
        left: 0;
        width: 100%;
        z-index: 100;
        background-color: transparent;
        border-bottom: 1px solid transparent;
        transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out;
    }
    .header.translucent:hover {
        background-color: #FFFFFF;
        border-bottom: 1px solid #e6e6e6;
    }

    /* Text & Icons: Start white, turn black on hover */
    .header.translucent .header-link,
    .header.translucent .header-icon {
        color: white;
        transition: color 0.3s ease-in-out;
    }
    .header.translucent:hover .header-link,
    .header.translucent:hover .header-icon {
        color: #111111;
    }

    /* Logo Swap: White logo visible by default, color logo appears on hover */
    .logo-container { position: relative; display: flex; align-items: center; justify-content: center; height: 36px; }
    .logo-container img { height: 100%; object-fit: contain; transition: opacity 0.3s ease-in-out; position: absolute; }
    .logo-color { opacity: 0; }
    .logo-white { opacity: 1; }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }

    /* Pull hero video up behind the header */
    .hero {
       /* The absolute positioning of the header handles the overlay effect */
    }
</style>
<!-- Iconify Script for Icons -->
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
"""

# --- STEP 2: Perform the replacement ---

# Find the original <header>...</header> block from the clean file and replace it entirely.
html = re.sub(r'<header class="header">.*?</header>', final_header_html, html, flags=re.DOTALL)

# Inject the CSS and Iconify script just before the </head> tag.
html = html.replace('</head>', final_css_injection + '\n</head>')


with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Definitive prototype (v5) has been built from a clean baseline.")
