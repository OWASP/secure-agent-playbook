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

  # Plays: only the specific play files the skill references. Their own
  # references (templates, data) are followed too, so they are scanned
  # alongside SKILL.md.
  docs="$skill/SKILL.md"
  for play in $(grep -ohE 'plays/[A-Za-z0-9._-]+\.md' "$skill/SKILL.md" | sort -u); do
    mkdir -p "$stage/plays"
    cp "$plugin/$play" "$stage/plays/"
    docs="$docs $plugin/$play"
  done

  # Templates: the whole dir when referenced (two small files).
  if grep -q 'templates/' $docs; then
    cp -RL "$plugin/templates" "$stage/templates"
  fi

  # Data: each referenced dataset. READMEs are dropped unless a doc cites
  # one (e.g. data/asvs/README.md as the chapter index). find -L follows
  # data dirs that are symlinks; an empty result is an error, not a
  # silently data-less zip.
  # The boundary keeps URLs like .../meta-data/iam/ from matching.
  for d in $(grep -ohE '(^|[^A-Za-z0-9_/-])data/[a-z-]+' $docs | grep -oE 'data/[a-z-]+' | sort -u); do
    # A play citing a dataset this plugin lacks (repo-root data/opencre,
    # prose like "data/services") is skipped; SKILL.md citing one fails.
    if [ ! -e "$plugin/$d" ] && ! grep -qE "(^|[^A-Za-z0-9_/-])$d" "$skill/SKILL.md"; then
      echo "note: $name: skipping $d (cited by a play, not in $plugin)" >&2
      continue
    fi
    mkdir -p "$stage/$d"
    find -L "$plugin/$d" -name '*.md' ! -name 'README.md' -exec cp {} "$stage/$d/" \;
    if grep -qh "$d/README.md" $docs; then
      cp "$plugin/$d/README.md" "$stage/$d/"
    fi
    if [ -z "$(ls -A "$stage/$d")" ]; then
      echo "ERROR: $name: $d vendored 0 files" >&2
      exit 1
    fi
  done

  # SKILL.md links to ../../plays and ../../templates (relative to its
  # place in the repo); in the zip those sit next to it.
  sed -i.bak 's#](\.\./\.\./#](#g' "$stage/SKILL.md" && rm "$stage/SKILL.md.bak"

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
