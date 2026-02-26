#!/bin/bash

# 1. Paths (Double quoted, no backslashes)
PROJECT_DIR="/Users/pietro/Builds/gitmermaid"
TARGET_MD="/Users/pietro/Builds/ObsidianVault/Sistemi Distribuiti/Tesi SmartDS.md"
PYTHON_EXE="$PROJECT_DIR/.venv/bin/python"
CONVERTER_SCRIPT="$PROJECT_DIR/converter.py"

# 2. Check if the environment exists
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Error: Virtual environment not found at $PYTHON_EXE"
    exit 1
fi

# 3. Clean the file (If "# Git Graph" exists, delete it and everything after)
if grep -q "^# Git Graph" "$TARGET_MD"; then
    echo "Cleaning existing graph section..."
    # macOS sed: Delete from match to end of file ($)
    sed -i '' '/^# Git Graph/,$d' "$TARGET_MD"
fi

# 4. Append the fresh content to the bottom
{
    echo -e "\n# Git Graph"
    echo '```mermaid'
    $PYTHON_EXE "$CONVERTER_SCRIPT"
    echo '```'
} >> "$TARGET_MD"

echo "Update complete for: $TARGET_MD"
