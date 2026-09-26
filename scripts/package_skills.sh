#!/usr/bin/env bash
# Package each skill as a self-contained zip uploadable at
# https://claude.ai/admin-settings/skills, which rejects zips with more
# than 200 files (see issue #23 — the whole-repo zip cannot be used there).
# Skills reference plays/, templates/, and data/ relative to the plugin
# root, so those files are vendored into each zip at the same relative
# paths.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$PWD/dist/skills"
rm -rf "$OUT"
mkdir -p "$OUT"

for skill in plugins/*/skills/*/; do
  plugin=$(dirname "$(dirname "$skill")")
  name=$(basename "$skill")
  stagedir="$OUT/.staging"
  stage="$stagedir/$name"
  rm -rf "$stagedir"
  mkdir -p "$stage"
  cp "$skill/SKILL.md" "$stage/"

  # Plays: only the specific play files the skill references.
  for play in $(grep -ohE 'plays/[A-Za-z0-9._-]+\.md' "$skill/SKILL.md" | sort -u); do
    mkdir -p "$stage/plays"
    cp "$plugin/$play" "$stage/plays/"
  done

  # Templates: the whole dir when referenced (two small files).
  if grep -q 'templates/' "$skill/SKILL.md"; then
    cp -R "$plugin/templates" "$stage/templates"
  fi

  # Data: each referenced dataset, minus READMEs (never loaded at runtime).
  for d in $(grep -ohE 'data/[a-z-]+' "$skill/SKILL.md" | sort -u); do
    mkdir -p "$stage/$d"
    find "$plugin/$d" -name '*.md' ! -name 'README.md' -exec cp {} "$stage/$d/" \;
  done

  # ponytail: MASTG tests are only ever loaded via the mastg_tests lists in
  # the MASVS files, so unreferenced tests are pruned to fit the 200-file
  # limit; revisit if skills ever load mastg files directly.
  if [ -d "$stage/data/mastg" ] && [ -d "$stage/data/masvs" ]; then
    referenced=$(grep -rhoE 'MASTG-TEST-[0-9]+' "$stage/data/masvs" | sort -u)
    for f in "$stage"/data/mastg/*.md; do
      grep -qx "$(basename "$f" .md)" <<<"$referenced" || rm "$f"
    done
  fi

  count=$(find "$stage" -type f | wc -l | tr -d ' ')
  if [ "$count" -gt 200 ]; then
    echo "ERROR: $name stages $count files, exceeding the 200-file upload limit" >&2
    exit 1
  fi
  (cd "$stagedir" && zip -qr "$OUT/$name.zip" "$name")
  rm -rf "$stagedir"
  echo "$name.zip ($count files)"
done
