import re
import glob
import os

# Get the path to the hero images
hero_image_path = '/Users/krazeerastagroup/.openclaw/workspace/assets/brands/jamrock/hero/'
# Use glob to get the actual, current filenames, and sort them
image_files = sorted(glob.glob(os.path.join(hero_image_path, 'Screenshot*.png')))

if not image_files:
    print("Error: No hero images found.")
    exit()

# Ensure we have a list of 4 images, looping if necessary
final_image_list = image_files
while len(final_image_list) < 4:
    final_image_list.extend(image_files) # Add the list to itself
final_image_list = final_image_list[:4] # Slice to get exactly 4

# Get relative paths for the HTML
relative_image_paths = [os.path.relpath(p, '/Users/krazeerastagroup/.openclaw/workspace/') for p in final_image_list]

# Read the current state of the prototype
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# Define the new swiper wrapper with exactly 4 slides
new_swiper_wrapper_html = f"""
<div class="swiper-wrapper">
    <div class="swiper-slide" style="background-image:url('{relative_image_paths[0]}')">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
            <h1 class="hero-title">NUH APOLOGIES</h1>
            <button class="btn-primary">Discover Collection</button>
        </div>
    </div>
    <div class="swiper-slide" style="background-image:url('{relative_image_paths[1]}')">
        <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
    </div>
    <div class="swiper-slide" style="background-image:url('{relative_image_paths[2]}')">
        <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
    </div>
    <div class="swiper-slide" style="background-image:url('{relative_image_paths[3]}')">
        <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
    </div>
</div>
"""

# Find the old swiper wrapper and replace it
html = re.sub(r'<div class="swiper-wrapper">.*?</div>', new_swiper_wrapper_html, html, flags=re.DOTALL)

# Write the final file
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Hero carousel updated to a 4-slide loop.")
