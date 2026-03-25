#!/bin/bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
DB_ID="32a99e91-5cba-813b-bee0-000bcfe9472c"

create_task() {
  local title="$1"
  local priority="$2"
  local role="$3"
  local status="$4"
  
  curl -s -X POST "https://api.notion.com/v1/pages" \
    -H "Authorization: Bearer $NOTION_KEY" \
    -H "Notion-Version: 2025-09-03" \
    -H "Content-Type: application/json" \
    -d '{
      "parent": {"database_id": "'"$DB_ID"'"},
      "properties": {
        "Project Name": {"title": [{"text": {"content": "'"$title"'"}}]},
        "Campaign/Brand": {"select": {"name": "Jamrock: T01"}},
        "Priority": {"select": {"name": "'"$priority"'"}},
        "Lead Agency Role": {"select": {"name": "'"$role"'"}},
        "Status": {"select": {"name": "'"$status"'"}}
      }
    }' > /dev/null
}

create_task "Hero Apparel Specimen (USPTO Class 025 Fix)" "P1 - Critical" "Creative Director" "Briefing"
create_task "Jamrock Flagship Web Experience (Banani UI)" "P1 - Critical" "Art Director" "Briefing"
create_task "T01 'They Carried It' Core Copy Matrix" "P2 - High" "Copywriter" "Backlog"

echo "Kanban populated."
