import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# Define the old and new logo paths
old_logo_src = "../../../assets/brands/jamrock/ILJ-02.png"
new_logo_full_color_src = "assets/brands/jamrock/ILJ-LOGO-FINAL.png"
new_logo_white_src = "assets-brands-jamrock/ILJ-LOGO-FINAL-WHITE.png" # Placeholder for JS

# Find the logo img tag
logo_img_pattern = re.compile(r'<img src="[^"]*ILJ-02\.png[^"]*" alt="[^"]*"[^>]*>')
logo_img_tag = logo_img_pattern.search(html)

if logo_img_tag:
    # Create the new logo structure with two versions for the hover swap
    new_logo_html = f'''
    <div class="logo-container">
        <img src="assets/brands/jamrock/ILJ-LOGO-FINAL-WHITE.png" alt="Jamrock Logo White" class="logo-white">
        <img src="assets/brands/jamrock/ILJ-LOGO-FINAL.png" alt="Jamrock Logo" class="logo-color">
    </div>
    '''
    # Replace the old simple img tag with the new container
    html = logo_img_pattern.sub(new_logo_html, html)

# Inject CSS and JS for the logo swap and icon library
injection = """
<style>
    .logo-container { position: relative; display: flex; align-items: center; justify-content: center; }
    .logo-container img { height: 90px; object-fit: contain; transition: opacity 0.3s ease-in-out; }
    .logo-color { opacity: 0; position: absolute; }
    .logo-white { opacity: 1; }

    .header.translucent:hover .logo-color { opacity: 1; }
    .header.translucent:hover .logo-white { opacity: 0; }
    
    .header-icons { display: flex; gap: 24px; }
    .header-icons a { color: inherit; }
</style>
<!-- Iconify Script for shopping cart etc. -->
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
"""

# Add the new styles and script
html = html.replace('</head>', injection + '\n</head>')

# Find the placeholder for icons and replace it
icons_placeholder_pattern = re.compile(r'<div style="width: 24px; height: 24px;[^"]*"></div>\s*<div style="width: 24px; height: 24px;[^"]*"></div>')

shopping_cart_html = '''
<div class="header-icons">
    <a href="#" aria-label="Search">
        <iconify-icon icon="lucide:search" style="font-size: 22px;"></iconify-icon>
    </a>
    <a href="#" aria-label="Account">
        <iconify-icon icon="lucide:user" style="font-size: 22px;"></iconify-icon>
    </a>
    <a href="#" aria-label="Shopping Bag">
        <iconify-icon icon="lucide:shopping-bag" style="font-size: 22px;"></iconify-icon>
    </a>
</div>
'''

html = re.sub(r'<div class="nav-right">.*</div>', f'<div class="nav-right">{shopping_cart_html}</div>', html, flags=re.DOTALL)


with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Prototype updated with final assets and interactions.")

