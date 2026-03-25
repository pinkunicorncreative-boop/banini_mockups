import json

def read_html(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data['designs'][0]['html']

html1 = read_html('/Users/krazeerastagroup/.openclaw/workspace/scripts/banani_design_part2.json')
html2 = read_html('/Users/krazeerastagroup/.openclaw/workspace/scripts/banani_design_part3.json')
html3 = read_html('/Users/krazeerastagroup/.openclaw/workspace/scripts/banani_design4.json')

# For now, let's just take the most complete one as our base
# A more complex script would parse and merge sections, but this is a good start
baseline_html = html3

# Inject the new header CSS and JS for the hover effect
header_injection = """
<style>
    .header.translucent {
        background-color: transparent;
        color: white; /* Assuming video is dark */
        transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
    }
    .header.translucent .header-logo, .header.translucent .header-nav a, .header.translucent .header-icons a {
        color: white !important;
        mix-blend-mode: difference;
    }
    .header.translucent:hover {
        background-color: #FFFFFF;
        color: #111111;
        border-bottom: 1px solid #e6e6e6;
    }
    .header.translucent:hover .header-logo, .header.translucent:hover .header-nav a, .header.translucent:hover .header-icons a {
       color: #111111 !important;
       mix-blend-mode: normal;
    }
    .hero {
        position: relative;
        top: -100px; /* Pull the hero up behind the header */
        margin-bottom: -100px; /* Adjust layout flow */
        z-index: -1;
    }
</style>
"""

# Replace logo and slogans
baseline_html = baseline_html.replace(
    '#i❤️jamrock', 
    '../../../assets/brands/jamrock/ILJ-02.png'
)
baseline_html = baseline_html.replace(
    'Elevated<br>Essentials', 
    'NUH APOLOGIES'
)
baseline_html = baseline_html.replace(
    '<p class="hero-subtitle">The New Standard</p>', 
    '<p class="hero-subtitle">IF YOU LOVE THE CULTURE. WEAR THE COLOR.</p>'
)

# Inject CSS at the end of <head>
final_html = baseline_html.replace('</head>', header_injection + '</head>')

# Add class to header
final_html = final_html.replace('<header class="header">', '<header class="header translucent">')

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(final_html)

print("Final prototype created.")
