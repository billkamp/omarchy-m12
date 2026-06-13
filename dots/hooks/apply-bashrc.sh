#!/usr/bin/env bash
set -euo pipefail

bashrc="$HOME/.bashrc"
dropin_dir="$HOME/.config/bash/interactive.d"
begin_marker="# >>> omarchy-m12 bash drop-ins >>>"
end_marker="# <<< omarchy-m12 bash drop-ins <<<"

mkdir -p "$dropin_dir"
touch "$dropin_dir/.keep"
touch "$bashrc"

block=$(cat <<'EOF'
# >>> omarchy-m12 bash drop-ins >>>
if [[ $- == *i* && -d "$HOME/.config/bash/interactive.d" ]]; then
  for file in "$HOME"/.config/bash/interactive.d/*.bash; do
    [[ -r "$file" ]] && source "$file"
  done
  unset file
fi
# <<< omarchy-m12 bash drop-ins <<<
EOF
)

tmp=$(mktemp)
awk -v begin="$begin_marker" -v end="$end_marker" '
  $0 == begin { skip = 1; next }
  $0 == end { skip = 0; next }
  !skip { print }
' "$bashrc" >"$tmp"

printf '%s\n\n%s\n' "$(sed '${/^$/d;}' "$tmp")" "$block" >"$bashrc"
rm -f "$tmp"
