from app.models import User, SpotifyUser, UserCreate, SpotifyUserCreate

from sqlmodel import Session
import spotipy
from app.core.config import settings
from app import crud
from app.spotipy_extensions import UserSpecificSpotify

scopes = ",".join(
    [
        "playlist-read-collaborative",
        "user-follow-read",
        "user-read-playback-position",
        "user-top-read",
        "user-read-recently-played",
        "user-library-read",
        "user-read-email",
        "user-read-private",
        "user-read-currently-playing",
        "user-modify-playback-state",
        "user-read-playback-state",
    ]
)

def get_or_create_spotify_user_from_spotify_code(*, session: Session, code: str) -> User:
    sp_oauth = spotipy.oauth2.SpotifyOAuth(
        settings.SPOTIFY_CLIENT_ID,
        settings.SPOTIFY_CLIENT_SECRET,
        f"{settings.SERVER_HOST}/api/v1/auth/spotify/code",
        scope=scopes,
    )
    token_info = sp_oauth.get_access_token(code, check_cache=False)
    sp = spotipy.Spotify(auth=token_info["access_token"])
    spotify_user_data = sp.current_user()
    spotify_user = crud.get_spotify_user_by_spotify_user_id(session=session, spotify_user_id=spotify_user_data["id"])
    if spotify_user is not None:
        return spotify_user

    user_in = UserCreate(
        email=spotify_user_data["email"]
    )
    user = crud.create_user(session=session, user_create=user_in)
    spotify_user_in = SpotifyUserCreate(
        spotify_user_id=spotify_user_data["id"],
        spotify_token_info=token_info,
        spotify_display_name=spotify_user_data["display_name"],
        user_id=user.id,
    )
    spotify_user = crud.create_spotify_user(session=session, spotify_user_in=spotify_user_in)


