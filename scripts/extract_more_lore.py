import json
import os
import glob

export_dir = os.path.expanduser('~/.openclaw/workspace/chatgpt_export')
output_dir = os.path.expanduser('~/.openclaw/workspace/extracted_lore')

new_brands = {
    "Big BumboClaat": ["big bumboclaat"],
    "Joo Club": ["joo club", "jooclub"],
    "Factor 8": ["factor 8", "factor8"]
}

brand_files = {brand: open(os.path.join(output_dir, f"{brand.replace(' ', '_')}_raw.md"), 'w') for brand in new_brands}

def extract_text(message):
    try:
        if message and 'content' in message and 'parts' in message['content']:
            parts = message['content']['parts']
            return ' '.join([str(p) for p in parts if isinstance(p, str)])
    except Exception:
        pass
    return ""

for filepath in glob.glob(os.path.join(export_dir, 'conversations-*.json')):
    print(f"Processing {os.path.basename(filepath)}...")
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    for conv in data:
        title = conv.get('title', 'Untitled') or 'Untitled'
        mapping = conv.get('mapping', {})
        
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
        
        for brand, keywords in new_brands.items():
            if any(kw in conv_text_lower or kw in title_lower for kw in keywords):
                brand_files[brand].write(f"## Conversation: {title}\n\n")
                brand_files[brand].write(conv_text)
                brand_files[brand].write("\n---\n\n")

for f in brand_files.values():
    f.close()
