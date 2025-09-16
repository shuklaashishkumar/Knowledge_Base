#!/bin/bash

# === CONFIG ===
PROJECT_ROOT="."                         # Current directory
PACKAGE_NAME="knowledge_base"               # <-- Set your project package name here

# === FOLDER STRUCTURE ===
FOLDERS=(
  "data"
  "store"
  "config"
  "prompts"
  "store/vector_store"
  "store/sqlite_db"
  "logs"
  "notebooks"
  "src/$PACKAGE_NAME/models"
  "src/$PACKAGE_NAME/utils"
  "src/$PACKAGE_NAME/core"
  "src/$PACKAGE_NAME/common"
  "src/$PACKAGE_NAME/providers"
)

# Python packages (need __init__.py)
PACKAGE_FOLDERS=(
  "src/$PACKAGE_NAME"
  "src/$PACKAGE_NAME/models"
  "src/$PACKAGE_NAME/utils"
  "src/$PACKAGE_NAME/core"
  "src/$PACKAGE_NAME/common"
  "src/$PACKAGE_NAME/providers"
)

# === CREATE FOLDERS ===
echo "📁 Creating folder structure..."
for folder in "${FOLDERS[@]}"; do
  mkdir -p "$PROJECT_ROOT/$folder"
  echo "  - $folder"
done

# === INIT FILES FOR PACKAGES ===
echo "🐍 Adding __init__.py files..."
for pkg in "${PACKAGE_FOLDERS[@]}"; do
  touch "$PROJECT_ROOT/$pkg/__init__.py"
done

# === README.md ===
README_FILE="$PROJECT_ROOT/README.md"
if [ ! -f "$README_FILE" ]; then
  cat > "$README_FILE" <<EOL
# ${PACKAGE_NAME^}

## Description
A brief description of your Python project.

## Folder Structure
\`\`\`
.
├── data/                     # Input datasets
├── store/      # Persisted stores 
├── store/vector_db      # Persisted stores vector DB
├── store/sqlite_db      # Persisted stores sql DB
├── prompts/                  # Prompt templates for LLMs
├── notebooks/                # python notebooks 
├── logs/                     # Logs or outputs
├── src/$PACKAGE_NAME/
│   ├── common/               # Common logic
│   ├── core/                 # Core logic
│   ├── models/               # Business logic / models
│   ├── providers/            # Business logic / models
│   └── utils/                # Helper functions
├── README.md
└── pyproject.toml
\`\`\`
EOL
  echo "📝 Created README.md"
else
  echo "✅ README.md already exists. Skipped."
fi

# === pyproject.toml ===
PYPROJECT_FILE="$PROJECT_ROOT/pyproject.toml"
if [ ! -f "$PYPROJECT_FILE" ]; then
  cat > "$PYPROJECT_FILE" <<EOL
[project]
name = "$PACKAGE_NAME"
version = "0.1.0"
description = "A brief description of your project"
authors = [{ name = "Ashish Shukla", email = "pro.ashish@gmail.com" }]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"

[tool.setuptools]
packages = ["src.$PACKAGE_NAME"]

[project.scripts]
start-app = "src.$PACKAGE_NAME.core.main:main"
EOL
  echo "🛠️ Created pyproject.toml"
else
  echo "✅ pyproject.toml already exists. Skipped."
fi

# === Create main.py ===
MAIN_PY="$PROJECT_ROOT/src/$PACKAGE_NAME/core/main.py"
if [ ! -f "$MAIN_PY" ]; then
  cat > "$MAIN_PY" <<EOL
def main():
    print("🚀 Project '$PACKAGE_NAME' started successfully!")

if __name__ == "__main__":
    main()
EOL
  echo "🚀 Created src/$PACKAGE_NAME/core/main.py"
else
  echo "✅ main.py already exists. Skipped."
fi

echo "✅ Project scaffold complete!"
