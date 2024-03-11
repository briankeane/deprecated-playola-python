from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from spotipy import oauth2
import spotipy

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import Item, User, SpotifyUser
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.spotify_user import random_token_info
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Item)
        session.execute(statement)
        statement = delete(SpotifyUser)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


class MockSpotifyOauth:
    token_info = random_token_info()

    def __init__(
        self,
        spotify_client_id: str,
        spotify_client_secret: str,
        redirect_uri: str,
        scope: str,
    ):
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    def get_access_token(self, code: str, check_cache: bool):
        return MockSpotifyOauth.token_info


class MockSpotify:
    token_info: dict = MockSpotifyOauth.token_info

    def __init__(self, auth: str):
        assert auth == MockSpotify.token_info["access_token"]

    def current_user(self) -> dict:
        return {
            "id": "random_spotify_id",
            "display_name": "some_spotify_display_name",
            "email": "test@testymctesterson.com",
        }


@pytest.fixture(scope="function")
def mock_SpotifyOauth(monkeypatch):
    monkeypatch.setattr(oauth2, "SpotifyOAuth", MockSpotifyOauth)
    return MockSpotifyOauth


@pytest.fixture(scope="function")
def mock_Spotify(monkeypatch):
    monkeypatch.setattr(spotipy, "Spotify", MockSpotify)
    return MockSpotify
