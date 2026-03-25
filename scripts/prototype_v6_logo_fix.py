import re

with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'r') as f:
    html = f.read()

# The only thing we need to change is the height in the CSS for the logo container.
# The old rule was: .logo-container { ... height: 36px; }
# The new rule will be:
new_height_rule = ".logo-container { position: relative; display: flex; align-items: center; justify-content: center; height: 50px; }"

# Use regex to find and replace that specific line
html = re.sub(r'\.logo-container.*?height: 36px;.*', new_height_rule, html)

# Also, let's ensure the images themselves can be a bit larger within that container.
html = re.sub(r'\.logo-container img {.*?}', '.logo-container img { height: 100%; object-fit: contain; transition: opacity 0.3s ease-in-out; position: absolute; }', html)


with open('/Users/krazeerastagroup/.openclaw/workspace/jamrock_final_prototype.html', 'w') as f:
    f.write(html)

print("Prototype V6: Logo container height corrected.")
