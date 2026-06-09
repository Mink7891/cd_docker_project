# practice_6_monitoring

Практическая работа №6: мониторинг и логирование контейнеризированного Flask-приложения с Prometheus, Grafana, Loki и Promtail. Папка предназначена для добавления в существующий репозиторий с практикой №5.

## Сервисы

- Flask-приложение: `http://SERVER_IP:5006`
- Grafana: `http://SERVER_IP:3001`
- Prometheus: `http://SERVER_IP:9091`
- Loki: `http://SERVER_IP:3101`

Логин Grafana по умолчанию:

- login: `admin`
- password: `admin`

## Размещение в репозитории

Папку `practice_6_monitoring` нужно положить в корень существующего репозитория. Workflow `monitoring-cd.yml` нужно положить в `.github/workflows/`.

## Локальный запуск

```bash
docker compose up -d --build
```

Проверка приложения:

```bash
curl http://127.0.0.1:5006
curl http://127.0.0.1:5006/metrics
```

## GitHub Secrets для деплоя

Обязательные:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
SERVER_IP
SERVER_USER
SSH_PRIVATE_KEY
```

Необязательные, если нужно изменить порты:

```text
MONITORING_APP_PORT=5006
GRAFANA_PORT=3001
PROMETHEUS_PORT=9091
LOKI_PORT=3101
GRAFANA_ADMIN_PASSWORD=admin
```

## Адреса для отчета на сервере 109.196.98.82

```text
Flask:      http://109.196.98.82:5006
Grafana:    http://109.196.98.82:3001
Prometheus: http://109.196.98.82:9091
Loki:       http://109.196.98.82:3101
```

## Проверка контейнеров на сервере

```bash
cd /opt/monitoring_project
docker compose ps
docker logs monitoring_flask_app
docker logs monitoring_promtail
```
