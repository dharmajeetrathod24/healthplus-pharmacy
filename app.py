import os
from flask import Flask, jsonify, render_template, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "v1")
COLOR = os.getenv("APP_COLOR", "none")
REQUESTS = Counter("pharmacy_http_requests_total", "Total HTTP requests", ["path"])

# MOCK DATA ONLY - no real patient or prescription information
MEDICINES = [
    {"name": "Paracetamol 500mg", "price": 25, "stock": "In stock"},
    {"name": "Cetirizine 10mg", "price": 30, "stock": "In stock"},
    {"name": "Vitamin C Tablets", "price": 120, "stock": "In stock"},
    {"name": "ORS Sachet", "price": 20, "stock": "In stock"},
    {"name": "Antacid Syrup", "price": 85, "stock": "Low stock"},
    {"name": "First Aid Kit", "price": 450, "stock": "In stock"},
]


@app.before_request
def count_request():
    REQUESTS.labels(request.path).inc()


@app.context_processor
def inject_globals():
    return {"version": VERSION, "color": COLOR}


@app.route("/")
def home():
    return render_template("index.html", items=MEDICINES[:3])


@app.route("/medicines")
def medicines():
    return render_template("medicines.html", items=MEDICINES)


@app.route("/order")
def order():
    return render_template("order.html", items=MEDICINES)


@app.route("/healthz")
def health():
    return jsonify(status="ok")


@app.route("/api/medicines")
def api_medicines():
    return jsonify(MEDICINES)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
