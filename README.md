# Практическая работа №5: CD с GitHub Actions и Docker

Проект содержит тестовое Flask-приложение, Dockerfile, Docker Compose и GitHub Actions workflow для автоматического развертывания на сервере.

## 1. Файлы проекта

- `app.py` — Flask-приложение;
- `requirements.txt` — зависимости Python;
- `Dockerfile` — сборка Docker-образа;
- `docker-compose.yml` — запуск контейнера на сервере;
- `.github/workflows/cd.yml` — workflow для сборки образа, отправки в Docker Hub и деплоя на сервер;
- `scripts/server_setup.sh` — скрипт первичной настройки сервера.

## 2. Локальная проверка

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Открыть в браузере:

```text
http://127.0.0.1:5000
```

Проверка через Docker:

```bash
docker compose up --build
```

## 3. Подготовка GitHub

Создать репозиторий, например:

```text
https://github.com/Mink7891/cd_docker_project
```

Загрузить проект:

```bash
git init
git branch -M main
git remote add origin https://github.com/Mink7891/cd_docker_project.git
git add .
git commit -m "Add CD pipeline"
git push -u origin main
```

## 4. Подготовка Docker Hub

Создать репозиторий Docker Hub:

```text
cd_docker_project
```

Создать Access Token в Docker Hub. Токен будет использоваться в GitHub Secrets.

## 5. Настройка сервера

Подключиться к серверу:

```bash
ssh user@server-ip
```

Скачать или создать на сервере скрипт `server_setup.sh`, затем запустить:

```bash
bash server_setup.sh dockerhub_username 80
```

Где:

- `dockerhub_username` — логин Docker Hub;
- `80` — порт приложения. Если на сервере уже занят порт 80, можно указать `5005`.

После выполнения скрипта нужно выйти из SSH и подключиться заново:

```bash
exit
ssh user@server-ip
```

## 6. GitHub Secrets

В GitHub открыть:

```text
Settings -> Secrets and variables -> Actions -> New repository secret
```

Добавить секреты:

- `DOCKERHUB_USERNAME` — логин Docker Hub;
- `DOCKERHUB_TOKEN` — токен Docker Hub;
- `SERVER_IP` — IP сервера;
- `SERVER_USER` — SSH-пользователь сервера;
- `SSH_PRIVATE_KEY` — приватный SSH-ключ;
- `APP_PORT` — порт приложения, например `80` или `5005`.

## 7. Проверка автоматического деплоя

После изменения кода выполнить:

```bash
git add .
git commit -m "Update application"
git push origin main
```

GitHub Actions автоматически:

1. соберёт Docker-образ;
2. отправит образ в Docker Hub;
3. подключится к серверу по SSH;
4. обновит контейнер через Docker Compose.

Проверка на сервере:

```bash
cd /opt/cd_docker_project
docker compose ps
docker logs cd_docker_project_web
```

Адрес приложения:

```text
http://server-ip
```

Если использовался порт `5005`:

```text
http://server-ip:5005
```
