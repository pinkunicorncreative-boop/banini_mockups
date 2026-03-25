import json, glob, os
export_dir = os.path.expanduser('~/.openclaw/workspace/chatgpt_export')
for filepath in glob.glob(os.path.join(export_dir, 'conversations-*.json')):
    with open(filepath, 'r') as f:
        data = json.load(f)
    for conv in data:
        title = conv.get('title', 'Untitled') or 'Untitled'
        mapping = conv.get('mapping', {})
        for node_id, node in mapping.items():
            msg = node.get('message')
            if msg and 'content' in msg and 'parts' in msg['content']:
                text = ' '.join([str(p) for p in msg['content']['parts'] if isinstance(p, str)])
                if 'joo' in text.lower():
                    print(f"Title: {title} - Match snippet: {text[max(0, text.lower().find('joo')-30):text.lower().find('joo')+30]}")
                    break
