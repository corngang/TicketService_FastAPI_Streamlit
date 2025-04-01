#!/bin/bash

# Unmark previously assumed unchanged files
git update-index --no-assume-unchanged .github/
git update-index --no-assume-unchanged manifests/

# Add changes, except the ignored files
git add .  # This will add all changes except the ignored files

# Reset .github and manifests folders to avoid adding them
git reset .github
git reset manifests

# Commit changes
git commit -m "Update images and other changes" || echo "No changes to commit"

git push secondary main

# Mark files as unchanged again
git update-index --assume-unchanged .github/
git update-index --assume-unchanged manifests/
