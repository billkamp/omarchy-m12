sync:
  uv sync

apply target="@local": sync
  uv run pyinfra {{target}} deploy.py --data action=apply

upgrade target="@local": sync
  uv run pyinfra {{target}} deploy.py --data action=upgrade

doctor target="@local": sync
  uv run pyinfra {{target}} deploy.py --data action=doctor
