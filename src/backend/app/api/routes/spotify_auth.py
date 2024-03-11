
from fastapi import APIRouter

from app.api.deps import SessionDep

router = APIRouter()
#
#
# @router.get("/code")
# async def spotify_auth_code(
#         session: SessionDep,
#         code: str,
# ):
#     user = await get_or_create_user_from_spotify_code(payload.code)
#     return RedirectResponse(
#         f"{settings.client_base_url}/users/{user.id}",
#         status_code=status.HTTP_302_FOUND,
#     )
#
# @router.get("/authorize")
# async def spotify_auth_redirect(settings: Settings = Depends(get_settings)):
#     sp_oauth = oauth2.SpotifyOAuth(
#         settings.spotify_client_id,
#         settings.spotify_client_secret,
#         f"{settings.base_url}/api/v1/auth/spotify/code",
#         scope=scopes,
#     )
#
#     return RedirectResponse(
#         sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND
#     )