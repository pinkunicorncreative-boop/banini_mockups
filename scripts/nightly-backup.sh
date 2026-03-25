#!/bin/zsh
set -euo pipefail

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:$PATH"

LOCAL_BACKUP_DIR="$HOME/.openclaw/backups/nightly"
ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw_Backups"

mkdir -p "$LOCAL_BACKUP_DIR"
mkdir -p "$ICLOUD_BACKUP_DIR"

# Run the backup command in the home directory
cd "$HOME"
openclaw backup create > /dev/null

# Move newly created backups from home to the nightly folder
LATEST_BACKUP=$(ls -t "$HOME"/*-openclaw-backup.tar.gz | head -n 1)
if [[ -f "$LATEST_BACKUP" ]]; then
  mv "$LATEST_BACKUP" "$LOCAL_BACKUP_DIR/"
  # Copy the exact same file to iCloud Drive
  cp "$LOCAL_BACKUP_DIR/$(basename "$LATEST_BACKUP")" "$ICLOUD_BACKUP_DIR/"
fi

# Rotate Local: Keep the 7 most recent backups, delete the rest
find "$LOCAL_BACKUP_DIR" -maxdepth 1 -name "*-openclaw-backup.tar.gz" -type f | sort -r | tail -n +8 | xargs rm -f 2>/dev/null || true

# Rotate iCloud: Keep the 7 most recent backups, delete the rest (saves storage quota)
find "$ICLOUD_BACKUP_DIR" -maxdepth 1 -name "*-openclaw-backup.tar.gz" -type f | sort -r | tail -n +8 | xargs rm -f 2>/dev/null || true

# Upload to Google Drive (via gog CLI)
if command -v gog &> /dev/null; then
  echo "Uploading to Google Drive..."
  gog upload "$LOCAL_BACKUP_DIR/$(basename "$LATEST_BACKUP")" --account krazeerasta@gmail.com > /dev/null
fi

echo "Nightly backup completed and synced to iCloud Drive + Google Drive. Kept the last 7 days locally."
