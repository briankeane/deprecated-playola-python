from sqlmodel import Session

from app.models import SpotifyUserCreate, SpotifyUser, SpotifyUserUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from app import crud


def test_create_spotify_user(db: Session) -> None:
    spotify_user_id = random_lower_string()
    spotify_display_name = random_lower_string()
    user = create_random_user(db)
    spotify_token_info = {
        "accessToken": "theAccessToken",
        "refreshToken": "theRefreshToken",
        "expiresIn": 3600,
    }
    spotify_user_in = SpotifyUserCreate(
        user_id=user.id,
        spotify_display_name=spotify_display_name,
        spotify_user_id=spotify_user_id,
        spotify_token_info=spotify_token_info,
    )
    spotify_user = crud.create_spotify_user(session=db, spotify_user_in=spotify_user_in)
    assert spotify_user.user_id == user.id
    assert spotify_user_id == spotify_user_id
    assert spotify_user.spotify_display_name == spotify_display_name
    assert spotify_user.spotify_token_info == spotify_token_info


def test_get_spotify_user(db: Session) -> None:
    spotify_user_id = random_lower_string()
    spotify_display_name = random_lower_string()
    user = create_random_user(db)
    spotify_token_info = {
        "accessToken": "theAccessToken",
        "refreshToken": "theRefreshToken",
        "expiresIn": 3600,
    }
    spotify_user_in = SpotifyUserCreate(
        user_id=user.id,
        spotify_display_name=spotify_display_name,
        spotify_user_id=spotify_user_id,
        spotify_token_info=spotify_token_info,
    )
    spotify_user = crud.create_spotify_user(session=db, spotify_user_in=spotify_user_in)
    spotify_user_retrieved = db.get(SpotifyUser, spotify_user.id)
    assert spotify_user_retrieved
    assert spotify_user_retrieved.user_id == spotify_user.user_id
    assert spotify_user_retrieved.spotify_user_id == spotify_user.spotify_user_id
    assert (
        spotify_user_retrieved.spotify_display_name == spotify_user.spotify_display_name
    )


def test_update_spotify_user(db: Session) -> None:
    spotify_user_id = random_lower_string()
    spotify_display_name = random_lower_string()
    user = create_random_user(db)
    spotify_token_info = {
        "accessToken": "theAccessToken",
        "refreshToken": "theRefreshToken",
        "expiresIn": 3600,
    }
    spotify_user_in = SpotifyUserCreate(
        user_id=user.id,
        spotify_display_name=spotify_display_name,
        spotify_user_id=spotify_user_id,
        spotify_token_info=spotify_token_info,
    )
    new_spotify_display_name = "a new spotify display name"
    new_spotify_token_info = {"the new info": "looks like this"}
    spotify_user = crud.create_spotify_user(session=db, spotify_user_in=spotify_user_in)
    spotify_user_in_update = SpotifyUserUpdate(
        spotify_display_name=new_spotify_display_name,
        spotify_token_info=new_spotify_token_info,
    )
    crud.update_spotify_user(
        session=db,
        spotify_user_id=spotify_user.id,
        spotify_user_in=spotify_user_in_update,
    )

    spotify_user_retrieved = db.get(SpotifyUser, spotify_user.id)
    assert spotify_user_retrieved.spotify_display_name == new_spotify_display_name
    assert spotify_user_retrieved.spotify_token_info == new_spotify_token_info
