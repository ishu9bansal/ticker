from fastapi import HTTPException, Request
from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions

from app.constants.index import ALLOWED_ORIGINS, CLERK_SECRET_KEY

def is_signed_in(request: Request):
    sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)
    auth_opts = AuthenticateRequestOptions(
        authorized_parties=ALLOWED_ORIGINS
    )
    request_state = sdk.authenticate_request(request, auth_opts)
    return request_state.is_signed_in

def authenticate_request(request: Request):
    if not is_signed_in(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request
