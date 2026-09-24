#!/usr/bin/env bash
# Pilote le conteneur GROBID : start | stop | status
set -uo pipefail
IMAGE="lfoppiano/grobid:0.8.1"
NAME="grobid"
URL="http://localhost:8070/api/isalive"
TIMEOUT=120

alive() { [ "$(curl -s -m 3 "$URL" 2>/dev/null)" = "true" ]; }

case "${1:-}" in
  start)
    if alive; then echo "GROBID déjà actif"; exit 0; fi
    if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
      docker start "$NAME" >/dev/null || exit 1
    else
      docker run --rm -d --name "$NAME" -p 8070:8070 "$IMAGE" >/dev/null || exit 1
    fi
    echo -n "Attente de GROBID"
    for ((i = 0; i < TIMEOUT; i += 2)); do
      if alive; then echo " — prêt"; exit 0; fi
      echo -n "."; sleep 2
    done
    echo
    echo "GROBID ne répond pas après ${TIMEOUT} s. Voir : docker logs $NAME" >&2
    exit 1
    ;;
  stop)
    docker stop "$NAME" >/dev/null 2>&1 && echo "GROBID arrêté" || echo "GROBID n'était pas actif"
    ;;
  status)
    if alive; then echo "GROBID actif"; exit 0; else echo "GROBID inactif"; exit 1; fi
    ;;
  *)
    echo "usage: $0 {start|stop|status}" >&2; exit 2 ;;
esac
