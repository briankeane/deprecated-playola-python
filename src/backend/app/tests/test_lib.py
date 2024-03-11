from sqlmodel import Session

from spotipy import oauth2
import spotipy

from app.lib import get_or_create_spotify_user_from_spotify_code
from app.tests.utils.spotify_user import create_random_spotify_user, random_token_info
from app.tests.utils.user import create_random_user

mocked_token_info = random_token_info()


class MockSpotifyOauth:
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
        return mocked_token_info


def test_get_or_create_spotify_from_code_where_spotify_user_exists(
    db: Session, mock_SpotifyOauth, mock_Spotify
):
    user = create_random_user(db=db)
    spotify_user = create_random_spotify_user(db=db, user_id=user.id)
    spotify_user.spotify_user_id = "random_spotify_id"
    db.add(spotify_user)
    db.commit()

    spotify_user_retrieved = get_or_create_spotify_user_from_spotify_code(
        session=db, code="this_is_the_code"
    )
    assert spotify_user.id == spotify_user_retrieved.id
