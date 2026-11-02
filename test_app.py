from app import app


def test_health():
    assert app.test_client().get("/healthz").status_code == 200


def test_pages():
    c = app.test_client()
    for p in ["/", "/medicines", "/order", "/api/medicines", "/metrics"]:
        assert c.get(p).status_code == 200
