#!/bin/bash

# Armagdon Prep - General Content Creator
# Usage: ./new-note.sh "Title" "Section"
# Sections: philosophy, tech, essays

TITLE=$1
SECTION=$2

if [ -z "$TITLE" ] || [ -z "$SECTION" ]; then
    echo "Usage: ./new-note.sh \"Title\" \"Section\""
    echo "Available sections: philosophy, tech, essays"
    exit 1
fi

FILENAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
FILEPATH="content/$SECTION/$FILENAME.md"

hugo new "$FILEPATH" --kind default
echo "✅ Created new $SECTION note: $FILEPATH"
# Optional: Open editor
# $EDITOR "$FILEPATH"
