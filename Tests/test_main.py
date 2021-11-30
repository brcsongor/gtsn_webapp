import os
import sys
import pytest

from main import app
from model import User, Pontok, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    os.environ['DATABASE_URL'] = "sqlite:///:memory:"
    client = app.test_client()
    cleanup()
    db.create_all()
    yield client


def cleanup():
    db.drop_all()


def test_available(client):
    response = client.get("/")
    assert response.status_code == 200
def test_not_logged_in(client):
    response = client.get("/")
    assert b"BEJELENTKEZ" in response.data
def test_not_logged_in_gtsn(client):
    response = client.get("/start")
    assert b"BEJELENTKEZ" not in response.data
def test_register_user(client):
    params = {
        "user-name": "Teszt user1",
        "user-email": "teszt1@teszt.hu",
        "user-pw": "123456"
    }
    register = client.post("/register", data=params, follow_redirects=True)
    assert register.status == "200 OK"
def test_log_in(client):
    params = {
        "user-name": "Teszt user1",
        "user-pw": "123456"
    }
    login = client.post("/login", data=params)
    response = client.get("/start")
    assert b"BEJELENTKEZ" not in response.data
def test_login_bad_data(client):
    params = {
        "user-name": "Nincs user",
        "user-pw": "Biztosannemez"
    }
    login = client.post("/login", data=params, follow_redirect=True)
    response = client.get("/")
    assert b"BEJELENTKEZ" in response.data
def test_make_correct_guess(client):
    params = {
        "test_secret_number": "15",
        "guess_data": "15"
    }
    guess = client.get("/result", data=params, follow_redirections = True)
    assert (b"nagyobb, mint" not in guess.data and b"kisebb, mint" not in guess.data)
def test_make_bad_guess_smaller(client):
    params = {
        "test_secret_number": "15",
        "guess_data": "10"
    }
    guess = client.get("/result", data=params, follow_redirections = True)
    assert b"nagyobb, mint" in guess.data
def test_make_bad_guess_bigger(client):
    params = {
        "test_secret_number": "15",
        "guess_data": "18"
    }
    guess = client.get("/result", data=params)
    assert b"kisebb, mint" in guess.data
