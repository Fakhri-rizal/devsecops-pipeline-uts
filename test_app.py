import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Menyiapkan database terpisah untuk setiap pengujian."""
    test_db = tmp_path / "test_users.db"

    monkeypatch.setattr(app_module, "DB_PATH", str(test_db))

    app_module.app.config["TESTING"] = True
    app_module.init_db()

    with app_module.app.test_client() as test_client:
        yield test_client


def test_login_page_opens(client):
    """Memastikan halaman login dapat dibuka."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_success(client):
    """Memastikan login berhasil menggunakan akun yang benar."""
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "supersecret",
        },
    )

    assert response.status_code == 200
    assert b"Login Berhasil" in response.data


def test_login_failure(client):
    """Memastikan login gagal jika password salah."""
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "password_salah",
        },
    )

    assert response.status_code == 401
    assert b"Login Gagal" in response.data


def test_login_unknown_username(client):
    """Memastikan username yang tidak terdaftar ditolak."""
    response = client.post(
        "/",
        data={
            "username": "pengguna_tidak_dikenal",
            "password": "supersecret",
        },
    )

    assert response.status_code == 401
    assert b"Login Gagal" in response.data


def test_login_sql_injection(client):
    """Memastikan percobaan SQL Injection tidak berhasil login."""
    response = client.post(
        "/",
        data={
            "username": "' OR '1'='1",
            "password": "password_salah",
        },
    )

    assert response.status_code == 401
    assert b"Login Gagal" in response.data
