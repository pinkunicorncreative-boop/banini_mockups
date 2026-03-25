import re

# Start with the current, correct version of the prototype
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# --- 1. Define the new components and dependencies ---

# Swiper.js CDN Links (a quick search would find these, but I know them)
swiper_cdn = """
<!-- Swiper.js CSS -->
<link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />

<!-- Swiper.js JS -->
<script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
"""

# Find existing cinematic images to use as placeholders
image_urls = re.findall(r'https://storage\.googleapis\.com/banani-generated-images/generated-images/[a-f0-9-]+\.jpg', html)
# Make sure we have at least 4 unique images
image_urls = list(dict.fromkeys(image_urls))
while len(image_urls) < 4:
    image_urls.append(image_urls[0]) # Duplicate if necessary

# New Swiper HTML structure
new_hero_html = f"""
<section class="hero swiper-container">
    <div class="swiper-wrapper">
        <div class="swiper-slide">
            <div class="hero-bg"><img src="{image_urls[0]}" alt="Campaign Image 1"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
                <h1 class="hero-title">NUH APOLOGIES</h1>
                <button class="btn-primary">Discover Collection</button>
            </div>
        </div>
        <div class="swiper-slide">
            <div class="hero-bg"><img src="{image_urls[1]}" alt="Campaign Image 2"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
                <h1 class="hero-title">NUH APOLOGIES</h1>
                <button class="btn-primary">Discover Collection</button>
            </div>
        </div>
        <div class="swiper-slide">
            <div class="hero-bg"><img src="{image_urls[2]}" alt="Campaign Image 3"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
                <h1 class="hero-title">NUH APOLOGIES</h1>
                <button class="btn-primary">Discover Collection</button>
            </div>
        </div>
        <div class="swiper-slide">
            <div class="hero-bg"><img src="{image_urls[3]}" alt="Campaign Image 4"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
                <h1 class="hero-title">NUH APOLOGIES</h1>
                <button class="btn-primary">Discover Collection</button>
            </div>
        </div>
    </div>
</section>
"""

# JavaScript to initialize Swiper
swiper_init_js = """
<script>
    document.addEventListener('DOMContentLoaded', function () {
        var heroSwiper = new Swiper('.swiper-container', {
            loop: true,
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            },
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
        });
    });
</script>
"""

# New CSS for Swiper integration
swiper_css = """
<style id="swiper-styles">
    .swiper-container {
        width: 100%;
        height: 750px;
    }
    .swiper-slide {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
"""

# --- 2. Perform the replacements ---

# A. Add Swiper CDN links to the head
html = html.replace('</head>', swiper_cdn + '\n</head>')

# B. Replace the old static hero with the new Swiper structure
html = re.sub(r'<section class="hero">.*?</section>', new_hero_html, html, flags=re.DOTALL)

# C. Add the Swiper initialization script before the body ends
html = html.replace('</body>', swiper_init_js + '\n</body>')

# D. Inject the Swiper-specific CSS into the main style block
html = html.replace('/* --- SVG LOGO --- */', '/* --- SWIPER HERO --- */\\n' + swiper_css + '\\n    /* --- SVG LOGO --- */')


# --- 3. Write the final file ---
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Hero section rebuilt with Swiper.js carousel.")
