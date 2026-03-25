import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_prototype.html', 'r') as f:
    content = f.read()

# Replace the hero text with the actual ILJ-NUH-APOLOGIES logo for maximum brand fidelity
replacement = '''<h1 class="hero-title" style="display: none;">NUH APOLOGIES</h1>
    <img src="assets/brands/jamrock/ILJ-NUH-APOLOGIES-blk.png" alt="Nuh Apologies" style="max-height: 120px; object-fit: contain; margin-bottom: 24px;">'''

content = content.replace('<h1 class="hero-title">NUH APOLOGIES</h1>', replacement)

# Add Google Fonts to make it actually feel like Prestige (e.g. Tenor Sans for headings, Inter for body)
fonts = '''<link href="https://fonts.googleapis.com/css2?family=Tenor+Sans&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Inter', sans-serif; }
  h1, h2, h3, .hero-title, .editorial-manifesto { font-family: 'Tenor Sans', sans-serif; }
  .nav-link { letter-spacing: 0.15em; font-size: 11px; text-transform: uppercase; font-weight: 500; }
  .btn-primary, .hero-cta { border-radius: 0px !important; letter-spacing: 0.1em; text-transform: uppercase; font-size: 12px; font-weight: 600; padding: 18px 36px; }
  .product-image { background-color: #F8F8F8; padding: 40px; }
  .logo-center img { height: 90px; } /* make the main logo pop more */
</style>'''

content = content.replace('</head>', fonts + '\n</head>')

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_prototype.html', 'w') as f:
    f.write(content)

