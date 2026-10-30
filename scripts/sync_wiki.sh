#!/usr/bin/env bash
# Sync docs/wiki to GitHub Wiki git repo
set -e

REPO_NAME="SWAGAT10241/haunted-shell"
WIKI_DIR="docs/wiki"

echo "Syncing $WIKI_DIR to https://github.com/$REPO_NAME.wiki.git..."

TOKEN=$(printf "protocol=https\nhost=github.com\n" | git credential fill | grep password | cut -d= -f2)

TEMP_WIKI="/tmp/haunted_shell_wiki_sync"
rm -rf "$TEMP_WIKI"

if git clone "https://$TOKEN@github.com/$REPO_NAME.wiki.git" "$TEMP_WIKI" 2>/dev/null; then
  cp -r "$WIKI_DIR/"* "$TEMP_WIKI/"
  cd "$TEMP_WIKI"
  git config user.name "SWAGAT SOURAV DHAR"
  git config user.email "swagatsourav10241@gmail.com"
  git add .
  if git commit -m "docs: synchronize wiki documentation"; then
    git push origin master || git push origin main
    echo "✓ GitHub Wiki synchronized successfully!"
  else
    echo "Wiki is already up to date."
  fi
else
  echo "Notice: To initialize GitHub's wiki backend, visit:"
  echo "  https://github.com/$REPO_NAME/wiki"
  echo "and click 'Create the first page'. Once initialized, rerun this script!"
fi
