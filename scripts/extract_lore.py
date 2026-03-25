import json
import os
import glob
import re

export_dir = os.path.expanduser('~/.openclaw/workspace/chatgpt_export')
output_dir = os.path.expanduser('~/.openclaw/workspace/extracted_lore')
os.makedirs(output_dir, exist_ok=True)

brands = {
    "Jamrock": ["jamrock", "ijamrock"],
    "Fruitmoss": ["fruitmoss", "fruit moss"],
    "Face Moss": ["face moss", "facemoss"],
    "Rummy Bear": ["rummy bear", "rummybear"],
    "Krazee Rasta": ["krazee rasta"]
}

brand_files = {brand: open(os.path.join(output_dir, f"{brand.replace(' ', '_')}_raw.md"), 'w') for brand in brands}

def extract_text(message):
    try:
        if message and 'content' in message and 'parts' in message['content']:
            parts = message['content']['parts']
            return ' '.join([str(p) for p in parts if isinstance(p, str)])
    except Exception:
        pass
    return ""

def process_file(filepath):
    print(f"Processing {os.path.basename(filepath)}...")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    for conv in data:
        title = conv.get('title', 'Untitled') or 'Untitled'
        mapping = conv.get('mapping', {})
        
        # Reconstruct conversation
        messages = []
        for node_id, node in mapping.items():
            if node and 'message' in node and node['message']:
                msg = node['message']
                role = msg.get('author', {}).get('role', 'unknown')
                text = extract_text(msg)
                if text:
                    messages.append(f"**{role}**: {text}\n")
        
        conv_text = "\n".join(messages)
        conv_text_lower = conv_text.lower()
        title_lower = title.lower()
        
        for brand, keywords in brands.items():
            if any(kw in conv_text_lower or kw in title_lower for kw in keywords):
                brand_files[brand].write(f"## Conversation: {title}\n\n")
                brand_files[brand].write(conv_text)
                brand_files[brand].write("\n---\n\n")

for filepath in glob.glob(os.path.join(export_dir, 'conversations-*.json')):
    process_file(filepath)

for f in brand_files.values():
    f.close()

print("Extraction complete. Check ~/.openclaw/workspace/extracted_lore/")
