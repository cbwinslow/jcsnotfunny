#!/usr/bin/env bash
set -euo pipefail

# Map file prefixes to milestones
declare -A milestone_map=(
  ["01"]="MVP"
  ["02"]="MVP"
  ["03"]="Automation v1"
  ["04"]="Automation v1"
  ["05"]="Website Launch"
  ["06"]="Website Launch"
  ["07"]="Growth"
  ["08"]="MVP"
  ["09"]="MVP"
  ["10"]="Growth"
)

PROJECT_NUM=20
OWNER="cbwinslow"
REPO="cbwinslow/jcsnotfunny"

for f in .github/issues/*.md; do
  echo "\n---\nProcessing $f"
  title=$(sed -n '1p' "$f" | sed -e 's/^Title:[ ]*//I' -e 's/^#\s*Issue:[ ]*//I' -e 's/^#\s*//')
  # Skip if issue with same title exists
  if gh issue list --limit 100 --search "$title" | grep -q "$title"; then
    echo "Issue exists already; skipping: $title"
    continue
  fi

  labels_line=$(grep -i '^\*\*Labels\*\*:' "$f" || true)
  labels=$(echo "$labels_line" | sed 's/^\*\*Labels\*\*:[ ]*//I' | tr -d '\r' | sed 's/^\s*//; s/\s*$//')
  if [ -z "$labels" ]; then labels="documentation"; fi

  # Ensure labels exist; trim spaces
  IFS=',' read -ra labs <<< "$labels"
  for i in "${!labs[@]}"; do
    labs[$i]=$(echo "${labs[$i]}" | sed 's/^\s*//; s/\s*$//')
    # Check label list for existence
    if ! gh label list --limit 500 | awk '{print $1}' | grep -xq -- "${labs[$i]}"; then
      echo "Label '${labs[$i]}' missing; creating"
      gh label create "${labs[$i]}" --color cfbad2 --description "Auto-created label: ${labs[$i]}"
    fi
  done

  key=$(basename "$f" | cut -d- -f1)
  milestone=${milestone_map[$key]:-}

  echo "Creating issue: $title"
  cmd=(gh issue create --title "$title" --body-file "$f")
  for lbl in "${labs[@]}"; do cmd+=(--label "$lbl"); done
  if [ -n "$milestone" ]; then cmd+=(--milestone "$milestone"); fi
  cmd+=(--assignee @me)

  issue_url=$("${cmd[@]}")
  echo "Created: $issue_url"

  issue_number=$(echo "$issue_url" | grep -oE '[0-9]+$')
  gh project item-add $PROJECT_NUM --owner $OWNER --url "https://github.com/$REPO/issues/$issue_number"
  echo "Added to project $PROJECT_NUM"

done

echo "\nAll items processed."
