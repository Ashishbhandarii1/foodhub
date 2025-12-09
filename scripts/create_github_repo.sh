#!/usr/bin/env bash
# Usage: ./scripts/create_github_repo.sh your-org-or-username repo-name [public|private]
set -e
OWNER=${1:-$(git config user.name)}
REPO=${2:-Feast-Fleet}
VISIBILITY=${3:-public}

# Ensure git is initialized
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial commit"
fi

# Create remote using gh (https://cli.github.com/)
gh repo create "${OWNER}/${REPO}" --${VISIBILITY} --source=. --remote=origin --push
echo "Created and pushed to https://github.com/${OWNER}/${REPO}"
