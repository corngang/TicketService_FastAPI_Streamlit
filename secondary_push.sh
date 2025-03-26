#!/bin/bash

# .github 및 manifests 디렉토리 무시 설정
git update-index --assume-unchanged .github/
git update-index --assume-unchanged manifests/

# 모든 변경 사항 추가 및 커밋
git add --all
git reset .github/
git reset manifests/
git commit -m "Update files excluding .github and manifests" || echo "No changes to commit"

# secondary에 푸시
git push secondary main

# 푸시 후 assume-unchanged 해제
git update-index --no-assume-unchanged .github/
git update-index --no-assume-unchanged manifests/
