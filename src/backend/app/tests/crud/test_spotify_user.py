from sqlmodel import Session

from app.models import SpotifyUserCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from app import crud

def test_create_spotify_user(db: Session) -> None:
    spotify_user_id = random_lower_string()
    spotify_display_name = random_lower_string()
    user = create_random_user(db)
    spotify_token_info = {"accessToken": "theAccessToken",
                                                    "refreshToken": "theRefreshToken",
                                                    "expiresIn": 3600}
    spotify_user_in = SpotifyUserCreate(user_id=user.id,
                                        display_name=spotify_display_name,
                                        spotify_user_id=spotify_user_id,
                                        token_info=spotify_token_info)
    spotify_user = crud.create_spotify_user(session=db, spotify_user_in=spotify_user_in)
    assert spotify_user.user_id == user.id
    assert spotify_user.display_name == spotify_display_name
    assert spotify_user.token_info == spotify_token_info