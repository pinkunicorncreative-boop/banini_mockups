import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# --- 1. Find the main header element ---
# Banani uses <header class="header translucent">
header_pattern = re.compile(r'(<header class="header translucent">)(.*?)(</header>)', re.DOTALL)
header_match = header_pattern.search(html)

if header_match:
    header_content = header_match.group(2)
    
    # --- 2. Replace Logo Placeholder with Dynamic Container ---
    logo_placeholder = re.compile(r'<div class="header-center".*?</div>', re.DOTALL)
    
    dynamic_logo_html = '''
    <div class="header-center">
        <div class="logo-container">
            <img src="assets/brands/jamrock/ILJ-LOGO-FINAL-WHITE.png" alt="Jamrock" class="logo-white">
            <img src="assets/brands/jamrock/ILJ-LOGO-FINAL.png" alt="Jamrock" class="logo-color">
        </div>
    </div>
    '''
    header_content = logo_placeholder.sub(dynamic_logo_html, header_content)

    # --- 3. Fix the right-side navigation and icons ---
    # The current one has inline styles and wrong colors. Let's rebuild it.
    nav_right_placeholder = re.compile(r'<div class="header-nav right">.*?</div>', re.DOTALL)

    new_nav_right_html = '''
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
    '''
    header_content = nav_right_placeholder.sub(new_nav_right_html, header_content)
    
    # Reassemble the header
    html = html.replace(header_match.group(0), header_match.group(1) + header_content + header_match.group(3))

# --- 4. CSS Injection for colors and hover effects ---
# Consolidate all the style fixes into one block for cleanliness
final_css_injection = """
<style id="final-art-direction-overrides">
    /* Logo Swap Logic */
    .logo-container { position: relative; display: flex; align-items: center; justify-content: center; }
    .logo-container img { height: 42px; object-fit: contain; transition: opacity 0.3s ease-in-out; }
    .logo-color { opacity: 0; position: absolute; }
    .logo-white { opacity: 1; }

    /* Header Color & Interaction Logic */
    .header.translucent {
        background-color: transparent;
        border-bottom: 1px solid transparent; /* Start with transparent border */
        transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out;
    }
    .header.translucent .header-link,
    .header.translucent .header-icon {
        color: white;
        transition: color 0.3s ease-in-out;
    }

    .header.translucent:hover {
        background-color: #FFFFFF;
        border-bottom: 1px solid #e6e6e6;
    }
    .header.translucent:hover .header-link,
    .header.translucent:hover .header-icon {
        color: #111111;
    }
    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }
    
    /* Pull hero video up behind header */
    .hero {
        margin-top: -100px; 
    }
    
</style>
"""
# Replace any old style blocks and add the new one cleanly before </head>
html = re.sub(r'<style id="nav-color-fix">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<style>.*logo-container.*</style>', '', html, flags=re.DOTALL)
html = html.replace('</head>', final_css_injection + '\n</head>')


with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Prototype V4 rebuild complete.")

