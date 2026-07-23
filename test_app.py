import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
def test_dashboard_page(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
def test_valid_login(client):

    response = client.post(
        "/login",
        data={
            "username": "vishal",
            "password": "vishu17"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.data
def test_inspection_page(client):
    response = client.get("/inspection")
    assert response.status_code == 200
def test_records_page(client):
    response = client.get("/records")
    assert response.status_code == 200
def test_report_page(client):

    with client.session_transaction() as session:
        session["username"] = "testuser"

    response = client.get("/report")

    assert response.status_code == 200
def test_tracker_page(client):
    response = client.get("/tracker")
    assert response.status_code == 200
def test_defect_library_page(client):
    response = client.get("/defect-library")
    assert response.status_code == 200
def test_invalid_login(client):

    response = client.post(
        "/login",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 200
def test_pass_inspection(client):

    response = client.post(
        "/inspection",
        data={
            "tire_id": "T101",
            "article_number": "AR101",
            "tire_size": "205/55 R16",
            "pattern_name": "All Season",
            "batch_number": "B101",
            "inspector_name": "Test User",
            "inspection_date": "2026-07-21",
            "shift": "A",
            "machine_name": "Uniformity",
            "inspection_status": "Pass",
            "remarks": "OK",
            "final_decision": "Accepted"
        }
    )

    assert response.status_code == 302
    assert "/dashboard" in response.location
def test_fail_inspection_redirect(client):

    response = client.post(
        "/inspection",
        data={
            "tire_id": "T102",
            "article_number": "AR102",
            "tire_size": "205/55 R16",
            "pattern_name": "Winter",
            "batch_number": "B102",
            "inspector_name": "Test User",
            "inspection_date": "2026-07-21",
            "shift": "A",
            "machine_name": "Geometry",
            "inspection_status": "Fail",
            "remarks": "Sidewall Crack",
            "final_decision": "Rejected"
        }
    )

    assert response.status_code == 302
    assert "/defect" in response.location