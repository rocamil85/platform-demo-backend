from datetime import datetime

import app_backend


def test_inicio_responde_correctamente():
    client = app_backend.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"mensaje": "Backend funcionando"}


def test_api_info_devuelve_hora_y_pod(monkeypatch):
    monkeypatch.setattr(
        app_backend.socket,
        "gethostname",
        lambda: "backend-test-pod",
    )

    client = app_backend.app.test_client()

    response = client.get("/api/info")
    data = response.get_json()

    assert response.status_code == 200
    assert data["pod"] == "backend-test-pod"

    hora = datetime.fromisoformat(data["hora"])
    assert hora.tzinfo is not None


def test_ruta_inexistente_devuelve_404():
    client = app_backend.app.test_client()

    response = client.get("/ruta-inexistente")

    assert response.status_code == 404
