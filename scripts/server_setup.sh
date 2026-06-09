#!/usr/bin/env bash
set -euo pipefail

DOCKERHUB_USERNAME="${1:-yourdockerhub}"
APP_PORT="${2:-80}"
PROJECT_DIR="/opt/cd_docker_project"

sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

sudo mkdir -p "$PROJECT_DIR"
sudo chown "$USER":"$USER" "$PROJECT_DIR"

cat > "$PROJECT_DIR/docker-compose.yml" <<'YAML'
services:
  web:
    image: ${IMAGE_NAME:-yourdockerhub/cd_docker_project:latest}
    container_name: cd_docker_project_web
    ports:
      - "${APP_PORT:-80}:5000"
    restart: always
YAML

cat > "$PROJECT_DIR/.env" <<ENV
IMAGE_NAME=${DOCKERHUB_USERNAME}/cd_docker_project:latest
APP_PORT=${APP_PORT}
ENV

printf '\nСервер подготовлен. Выйдите из SSH и зайдите снова, чтобы применились права Docker.\n'
printf 'Папка проекта: %s\n' "$PROJECT_DIR"
printf 'Порт приложения: %s\n' "$APP_PORT"
printf 'После первого push в GitHub приложение будет доступно по адресу: http://IP_сервера:%s\n' "$APP_PORT"
