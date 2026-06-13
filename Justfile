sync:
  uv sync

bootstrap-ssh:
  sudo systemctl enable --now sshd
  sudo ufw allow OpenSSH

apply target="@local": sync
  if [ "{{target}}" = "@local" ]; then sudo -v; fi
  uv run pyinfra -vv {{target}} deploy.py --data action=apply

upgrade target="@local": sync
  if [ "{{target}}" = "@local" ]; then sudo -v; fi
  uv run pyinfra -vvv {{target}} deploy.py --data action=upgrade

doctor target="@local": sync
  uv run pyinfra -vv {{target}} deploy.py --data action=doctor
