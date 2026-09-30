from fastapi.testclient import TestClient

from app.main import app
import pytest


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client



def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["app"] == "FitBuddy"


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_nutrition_tip(client):
    response = client.get(
        "/nutrition-tip?goal=weight%20loss"
    )

    assert response.status_code == 200
    assert "Nutrition Tip" in response.text


def test_view_all_users(client):
    response = client.get("/view-all-users")

    assert response.status_code == 200
    assert "All Users" in response.text