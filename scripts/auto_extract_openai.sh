#!/bin/bash
# Check Downloads folder for the ChatGPT zip
ZIP_FILE=$(ls -t ~/Downloads/*ChatGPT*.zip 2>/dev/null | head -n 1)

if [ -f "$ZIP_FILE" ]; then
    echo "Found ChatGPT export: $ZIP_FILE"
    echo "Extracting to workspace..."
    unzip -q -o "$ZIP_FILE" -d ~/.openclaw/workspace/chatgpt_export
    echo "Done. The export is now at ~/.openclaw/workspace/chatgpt_export"
else
    echo "No ChatGPT export zip found in ~/Downloads. Did you download it yet?"
fi
