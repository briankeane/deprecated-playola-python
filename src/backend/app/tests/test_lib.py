from sqlmodel import Session

from spotipy import oauth2, Spotify
import spotipy

from app.lib import get_or_create_spotify_user_from_spotify_code
from app.tests.utils.spotify_user import create_random_spotify_user, random_token_info
from app.tests.utils.user import create_random_user
mocked_token_info = random_token_info()

class MockSpotifyOauth:
    def __init__(self, spotify_client_id: str, spotify_client_secret: str, redirect_uri: str, scope: str):
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope


    def get_access_token(self,code: str, check_cache: bool):
        return mocked_token_info

class MockSpotify:
    def __init__(self, auth: str):
        assert auth == mocked_token_info["access_token"]

    def current_user(self) -> dict:
        return { "id": "random_spotify_id",
                 "display_name": "some_spotify_display_name",
                 "email": "test@testymctesterson.com" }


def test_get_or_create_spotify_from_code_where_spotify_user_exists(db: Session, monkeypatch):
    monkeypatch.setattr(oauth2, "SpotifyOAuth", MockSpotifyOauth)
    user= create_random_user(db=db)
    spotify_user = create_random_spotify_user(db=db, user_id=user.id)
    spotify_user.spotify_user_id = "random_spotify_id"
    db.add(spotify_user)
    db.commit()

    monkeypatch.setattr(spotipy, "Spotify", MockSpotify)

    spotify_user_retrieved = get_or_create_spotify_user_from_spotify_code(session=db, code="this_is_the_code")
    assert spotify_user.id == spotify_user_retrieved.id