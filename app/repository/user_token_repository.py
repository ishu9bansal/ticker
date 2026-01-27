from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import UserToken
from .base import RepositoryBase


class UserTokenRepository(RepositoryBase[UserToken]):
    def __init__(self, session: Session):
        super().__init__(session, UserToken)

    def get_token(self, user_id: str) -> str | None:
        stmt = select(UserToken).where(UserToken.user_id == user_id)
        result = self.session.execute(stmt).scalars().first()
        return result.token if result else None

    def update_token(self, user_id: str, new_token: str) -> UserToken:
        stmt = select(UserToken).where(UserToken.user_id == user_id)
        user_token = self.session.execute(stmt).scalars().first()
        if user_token:
            user_token.token = new_token
            self.add(user_token)
            return user_token
        else:
            new_user_token = UserToken(user_id=user_id, token=new_token)
            self.add(new_user_token)
            return new_user_token

