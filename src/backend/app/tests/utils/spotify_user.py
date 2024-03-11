from app.tests.utils.utils import random_email, random_lower_string
from app.models import SpotifyUserCreate, SpotifyUser, SpotifyUserUpdate
from app import crud
from sqlmodel import Session


def create_random_spotify_user(db: Session, user_id: int) -> SpotifyUser:
    spotify_user_in = SpotifyUserCreate(
        spotify_display_name=random_lower_string(),
        spotify_user_id=random_lower_string(),
        spotify_token_info=random_token_info(),
        user_id=user_id,
    )
    spotify_user = crud.create_spotify_user(session=db, spotify_user_in=spotify_user_in)
    return spotify_user


def random_token_info() -> dict:
    return {
        "access_token": random_lower_string(),
        "refresh_token": random_lower_string(),
        "expires_in": 3600,
    }
