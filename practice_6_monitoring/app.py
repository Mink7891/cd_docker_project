from flask import Flask, Response
import logging
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

LOG_FILE = os.getenv("LOG_FILE", "/var/log/flask-app/app.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("monitoring_project")
logger.setLevel(logging.INFO)
logger.propagate = False

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

if not logger.handlers:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

REQUEST_COUNT = Counter(
    "flask_app_requests_total",
    "Total number of HTTP requests processed by the Flask application",
    ["endpoint", "method", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "flask_app_request_latency_seconds",
    "Request latency for the Flask application",
    ["endpoint"],
)


@app.route("/")
def home():
    with REQUEST_LATENCY.labels(endpoint="/").time():
        logger.info("Received request on home page")
        REQUEST_COUNT.labels(endpoint="/", method="GET", http_status="200").inc()
        return "Hello, Monitoring!"


@app.route("/health")
def health():
    logger.info("Health check request")
    REQUEST_COUNT.labels(endpoint="/health", method="GET", http_status="200").inc()
    return {"status": "ok"}


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
