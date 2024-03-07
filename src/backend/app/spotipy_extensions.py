from sqlmodel import Session

from app.core.config import settings
from spotipy import CacheHandler, Spotify, SpotifyOAuth
from app.crud import create_spotify_user, update_spotify_user
from app.models import SpotifyUser, SpotifyUserUpdate


class UserSpecificCacheHandler(CacheHandler):
    def __init__(self, db: Session, spotify_user: SpotifyUser):
        self.db = db
        self.spotify_user = spotify_user

    def get_cached_token(self):
        return self.spotify_user.spotify_token_info

    def save_token_to_cache(self, token_info):
        spotify_user_in = SpotifyUserUpdate(token_info=token_info)
        self.spotify_user = update_spotify_user(
            session=self.db,
            spotify_user_id=self.spotify_user.id,
            spotify_user_in=spotify_user_in,
        )


class UserSpecificSpotify(Spotify):
    def __init__(self, db: Session, spotify_user: SpotifyUser):
        cache_handler = UserSpecificCacheHandler(db=db, spotify_user=spotify_user)
        spotify_oath = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTFIY_REDIRECT_URI,
            cache_handler=cache_handler,
        )
        super().__init__(oauth_manager=spotify_oath)
