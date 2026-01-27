
from pydantic import BaseModel

class ClerkUser(BaseModel):
    exp: int
    iat: int
    iss: str
    sub: str
    azp: str
