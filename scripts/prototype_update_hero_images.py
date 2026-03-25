import re

# Get the filenames (NOTE: In a real scenario, the script would get these dynamically)
# For this script, we'll hardcode them based on the previous command's output.
# IMPORTANT: The user must not add other screenshots in the meantime.
# To be safe, let's list them again inside the script.
import glob
import os

hero_image_path = '/Users/krazeerastagroup/.openclaw/workspace/assets/brands/jamrock/hero/'
# Use glob to get the actual, current filenames
image_files = sorted(glob.glob(os.path.join(hero_image_path, 'Screenshot*.png')))

if len(image_files) < 3:
    print("Error: Not enough new hero images found.")
    exit()

# Get relative paths for the HTML
relative_image_paths = [os.path.relpath(p, '/Users/krazeerastagroup/.openclaw/workspace/') for p in image_files]


# Read the current state of the prototype
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# Define the new swiper wrapper with the correct 3 slides
new_swiper_wrapper_html = f"""
<div class="swiper-wrapper">
    <div class="swiper-slide" style="background-image:url({relative_image_paths[0]})">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
            <h1 class="hero-title">NUH APOLOGIES</h1>
            <button class="btn-primary">Discover Collection</button>
        </div>
    </div>
    <div class="swiper-slide" style="background-image:url({relative_image_paths[1]})">
        <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
    </div>
    <div class="swiper-slide" style="background-image:url({relative_image_paths[2]})">
        <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
    </div>
</div>
"""

# Find the old swiper wrapper and replace it
html = re.sub(r'<div class="swiper-wrapper">.*?</div>', new_swiper_wrapper_html, html, flags=re.DOTALL)


# Write the final file
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Hero carousel updated with new images from desktop.")
