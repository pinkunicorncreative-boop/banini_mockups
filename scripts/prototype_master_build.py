import re

# Start with the clean, un-touched baseline from Banani
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_clean_baseline.html', 'r') as f:
    html = f.read()

# --- 1. DEFINE ALL FINAL COMPONENTS ---

# --- Dependencies ---
final_dependencies = """
<!-- Swiper.js CSS -->
<link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />
<!-- Iconify Script for Icons -->
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
<!-- Swiper.js JS -->
<script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
"""

# --- Header ---
final_header_html = """
<header class="header translucent">
    <nav class="header-nav">
        <a href="#" class="header-link">Shop</a>
        <a href="#" class="header-link">Collections</a>
        <a href="#" class="header-link">Journal</a>
    </nav>
    <div class="header-center">
        <div class="logo-container">
            <img src="assets/brands/jamrock/ILJ-LOGO-MAIN-FINAL-WT.svg" alt="Jamrock" class="logo-svg logo-white">
            <img src="assets/brands/jamrock/ILJ-LOGO-MAIN-FINAL.svg" alt="Jamrock" class="logo-svg logo-color">
        </div>
    </div>
    <div class="header-nav right">
        <a href="#" class="header-icon"><iconify-icon icon="lucide:search" style="font-size: 20px;"></iconify-icon></a>
        <a href="#" class="header-icon"><iconify-icon icon="lucide:user" style="font-size: 20px;"></iconify-icon></a>
        <a href="#" class="header-icon" style="display: flex; align-items: center; gap: 8px;">
            <iconify-icon icon="lucide:shopping-bag" style="font-size: 20px;"></iconify-icon>
            <span style="font-size: 13px; font-weight: 500;">0</span>
        </a>
    </div>
</header>
"""

# --- Hero Carousel ---
image_urls = re.findall(r'https://storage\.googleapis\.com/banani-generated-images/generated-images/[a-f0-9-]+\.jpg', html)
image_urls = list(dict.fromkeys(image_urls))
while len(image_urls) < 4: image_urls.append(image_urls[0])

hero_carousel_html = f"""
<section class="hero swiper-container">
    <div class="swiper-wrapper">
        <div class="swiper-slide" style="background-image:url({image_urls[0]})">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>
                <h1 class="hero-title">NUH APOLOGIES</h1>
                <button class="btn-primary">Discover Collection</button>
            </div>
        </div>
        <div class="swiper-slide" style="background-image:url({image_urls[1]})">
            <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
        </div>
        <div class="swiper-slide" style="background-image:url({image_urls[2]})">
            <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
        </div>
        <div class="swiper-slide" style="background-image:url({image_urls[3]})">
            <div class="hero-overlay"></div><div class="hero-content"><p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p><h1 class="hero-title">NUH APOLOGIES</h1><button class="btn-primary">Discover Collection</button></div>
        </div>
    </div>
</section>
"""

# --- Footer ---
final_footer_html = """
<footer class="site-footer">
    <div class="footer-grid">
        <div class="footer-column footer-subscribe">
            <h3 class="column-title">Join The Culture</h3>
            <p>Be the first to know about new collections, special events, and what’s going on in the Jamrock world.</p>
            <form class="subscribe-form"><input type="email" placeholder="Enter your email" class="subscribe-input"><button type="submit" class="subscribe-button">Subscribe</button></form>
        </div>
        <div class="footer-column"><h3 class="column-title">Shop</h3><div class="footer-link-list"><a href="#" class="footer-link">New Arrivals</a><a href="#" class="footer-link">Apparel</a><a href="#" class="footer-link">Headwear</a><a href="#" class="footer-link">Collections</a></div></div>
        <div class="footer-column"><h3 class="column-title">About</h3><div class="footer-link-list"><a href="#" class="footer-link">Our Story</a><a href="#" class="footer-link">Journal</a><a href="#" class="footer-link">Contact</a><a href="#" class="footer-link">Stores</a></div></div>
        <div class="footer-column"><h3 class="column-title">Support</h3><div class="footer-link-list"><a href="#" class="footer-link">FAQ</a><a href="#" class="footer-link">Shipping & Returns</a><a href="#" class="footer-link">Terms of Service</a><a href="#" class="footer-link">Privacy Policy</a></div></div>
    </div>
    <div class="footer-bottom-bar">
        <div class="copyright">© <span id="copyright-year"></span> I LOVE JAMROCK APPARELS</div>
        <div class="footer-socials">
            <a href="#"><iconify-icon icon="lucide:instagram" style="font-size: 20px;"></iconify-icon></a>
            <a href="#"><iconify-icon icon="lucide:twitter" style="font-size: 20px;"></iconify-icon></a>
            <a href="#"><iconify-icon icon="lucide:facebook" style="font-size: 20px;"></iconify-icon></a>
        </div>
    </div>
</footer>
"""

# --- Scripts ---
final_scripts = """
<script>
    document.getElementById('copyright-year').textContent = new Date().getFullYear();
    document.addEventListener('DOMContentLoaded', function () {
        var heroSwiper = new Swiper('.swiper-container', {
            loop: true, effect: 'fade', fadeEffect: { crossFade: true },
            autoplay: { delay: 4000, disableOnInteraction: false },
        });
    });
</script>
"""

# --- CSS ---
final_css = """
<style id="jamrock-master-styles">
    /* --- ANNOUNCEMENT & HEADER WRAPPER --- */
    .site-header-container{position:absolute;top:0;left:0;width:100%;z-index:100}
    .announcement{position:relative;z-index:101}
    /* --- HEADER --- */
    .header.translucent{background-color:transparent;border-bottom:1px solid transparent;transition:background-color .3s ease-in-out,border-color .3s ease-in-out;padding:24px 60px}
    .header.translucent:hover{background-color:#fff;border-bottom:1px solid #e6e6e6}
    .header.translucent .header-link,.header.translucent .header-icon{color:#fff;transition:color .3s ease-in-out;text-decoration:none}
    .header.translucent:hover .header-link,.header.translucent:hover .header-icon{color:#111}
    /* --- LOGO --- */
    .logo-container{position:relative;width:clamp(120px,12vw,180px);height:60px;display:flex;align-items:center;justify-content:center}
    .logo-svg{position:absolute;width:100%;height:100%;object-fit:contain;transition:opacity .3s ease-in-out}
    .logo-color{opacity:0;z-index:1}
    .logo-white{opacity:.5;z-index:2}
    .header.translucent:hover .logo-color{opacity:1}
    .header.translucent:hover .logo-white{opacity:0}
    /* --- HERO CAROUSEL --- */
    .swiper-container{width:100%;height:750px;position:relative}
    .swiper-slide{display:flex;align-items:center;justify-content:center;background-size:cover;background-position:center}
    /* --- FOOTER --- */
    .site-footer{background-color:var(--muted);color:var(--muted-foreground);padding:100px 60px;border-top:1px solid var(--border)}
    .footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:60px;margin-bottom:80px}
    .footer-column .column-title{font-size:14px;font-weight:500;color:var(--foreground);letter-spacing:.1em;text-transform:uppercase;margin-bottom:24px}
    .footer-column .footer-link-list{display:flex;flex-direction:column;gap:16px}
    .footer-column .footer-link{font-size:14px;color:var(--muted-foreground);text-decoration:none;transition:color .2s ease-in-out}
    .footer-column .footer-link:hover{color:var(--foreground)}
    .footer-subscribe p{font-size:14px;line-height:1.7;margin-bottom:24px}
    .subscribe-form{display:flex}
    .subscribe-input{flex-grow:1;border:1px solid var(--border);padding:12px 16px;font-size:14px;background-color:var(--background);color:var(--foreground);border-radius:0}
    .subscribe-button{border:1px solid var(--primary);background-color:var(--primary);color:var(--primary-foreground);padding:12px 24px;cursor:pointer;font-size:13px;text-transform:uppercase;letter-spacing:.1em;border-radius:0}
    .footer-bottom-bar{display:flex;justify-content:space-between;align-items:center;padding-top:40px;border-top:1px solid var(--border);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
    .footer-socials{display:flex;gap:24px}
    .footer-socials a{color:var(--muted-foreground);transition:color .2s ease-in-out}
    .footer-socials a:hover{color:var(--foreground)}
</style>
"""

# --- 2. PERFORM ALL MODIFICATIONS IN ONE PASS ---

# A. Inject all dependencies and master CSS into the head
html = html.replace('</head>', final_dependencies + '\n' + final_css + '\n</head>')

# B. Extract original announcement bar and then remove placeholders
announcement_html = re.search(r'<div class="announcement">.*?</div>', html, re.DOTALL).group(0)
html = html.replace(announcement_html, '')
html = re.sub(r'<header class="header">.*?</header>', '', html, flags=re.DOTALL)
html = re.sub(r'<section class="hero">.*?</section>', '', html, flags=re.DOTALL)
html = re.sub(r'<footer class="footer">.*?</footer>', '', html, flags=re.DOTALL)

# C. Build the new page structure
new_page_structure = f"""
<div class="site-header-container">
    {announcement_html}
    {final_header_html}
</div>
{hero_carousel_html}
"""

# D. Inject the new structure at the top of the theme wrapper
html = re.sub(r'(<div class="prestige-theme">)', r'\\1' + new_page_structure, html)

# E. Append the final footer before the closing div
html = re.sub(r'(<div class="collection-row">.*?</div>)', r'\\1' + final_footer_html, html)

# F. Inject the final scripts before the closing body tag
html = html.replace('</body>', final_scripts + '\n</body>')

# --- 3. WRITE THE FINAL FILE ---
with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Master build complete. All features integrated into a clean file.")
