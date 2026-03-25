import re

# Start with the clean, un-touched baseline from Banani
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_clean_baseline.html', 'r') as f:
    html = f.read()

# --- 1. Define the final, correct HTML components ---

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
<style id="final-art-direction">
    /* Core Header Interaction */
    .header.translucent {
        position: absolute; top: 0; left: 0; width: 100%; z-index: 100;
        background-color: transparent; border-bottom: 1px solid transparent;
        transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out;
        padding: 24px 60px;
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

    /* SVG Logo Control */
    .logo-container {
        position: relative;
        width: clamp(120px, 12vw, 180px);
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-svg {
        position: absolute;
        width: 100%; height: 100%;
        object-fit: contain;
        transition: opacity 0.3s ease-in-out;
    }

    /* SVG Logo Swap Logic with z-index */
    .logo-color { opacity: 0; z-index: 1; }
    .logo-white { opacity: 1; z-index: 2; }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }
</style>
<!-- Iconify Script for Icons -->
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
"""

# --- 2. Perform all modifications in one pass ---

# A. Replace the entire original header
html = re.sub(r'<header class="header">.*?</header>', final_header_html, html, flags=re.DOTALL)

# B. Replace the generic hero slogans with the correct ones
html = html.replace('<p class="hero-subtitle">The New Standard</p>', '<p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>')
html = html.replace('<h1 class="hero-title">Elevated<br>Essentials</h1>', '<h1 class="hero-title">NUH APOLOGIES</h1>')

# C. Inject the final CSS and script
html = html.replace('</head>', final_css_injection + '\n</head>')

# --- 3. Write the final, clean file ---
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Definitive All-in-One build complete. This is the final version.")
