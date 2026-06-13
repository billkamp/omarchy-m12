#!/usr/bin/env bash
set -euo pipefail

target_dir="$HOME/.config/hypr"
source_dir="$HOME/.config/yolk/eggs/home/.config/hypr"
stamp=$(date +%Y%m%d%H%M%S)

bash_config="$HOME/.config/bash"
bash_target=$(readlink "$bash_config" 2>/dev/null || true)

case "$bash_target" in
  "$HOME/.config/yolk/eggs/home/.config/bash"|"$HOME/.local/share/omarchy-m12/dots/eggs/home/.config/bash")
    rm -f "$bash_config"
    mkdir -p "$bash_config/interactive.d"
    ;;
esac

mkdir -p "$target_dir"

for name in looknfeel.lua bindings.lua; do
  target="$target_dir/$name"
  source="$source_dir/$name"

  if [[ -L "$target" ]]; then
    [[ $(readlink -f "$target") == $(readlink -f "$source") ]] && continue
    rm -f "$target"
  elif [[ -e "$target" ]]; then
    mv "$target" "$target.bak.omarchy-m12.$stamp"
  fi
done
