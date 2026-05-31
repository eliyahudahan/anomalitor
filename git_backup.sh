#!/bin/bash
# Automatic Git Backup Script for Anomalitor

cd ~/dev/anomalitor || { echo "❌ Directory not found"; exit 1; }

echo "📂 Working directory: $(pwd)"
echo "🔄 Checking Git status..."

# בדוק אם יש שינויים
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "✅ No changes to commit. Working tree clean."
    exit 0
fi

echo "📦 Changes detected. Adding files..."
git add .

echo "💾 Committing changes..."
COMMIT_MSG="Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Backup completed: $COMMIT_MSG"
