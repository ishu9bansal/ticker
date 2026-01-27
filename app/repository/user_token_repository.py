from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import UserToken
from app.utils import cached
from .base import RepositoryBase


class UserTokenRepository(RepositoryBase[UserToken]):
    def __init__(self, session: Session):
        super().__init__(session, UserToken)
        
    def _by_user_id(self, user_id: str) -> UserToken | None:
        stmt = select(UserToken).where(UserToken.user_id == user_id)
        result = self.session.execute(stmt).scalars().first()
        return result

    # @cached('user_tokens')    # NOTE: Caching at this layer lead to stale data issues, update_token method should invalidate cache if used
    def get_token(self, user_id: str) -> str | None:
        result = self._by_user_id(user_id)
        return result.token if result else None

    def _update(self, user_token: UserToken) -> UserToken:
        self.session.add(user_token)
        self.session.commit()
        self.session.refresh(user_token)
        return user_token
    
    def update_token(self, user_id: str, new_token: str) -> UserToken:
        obj = self._by_user_id(user_id)
        if obj:
            obj.token = new_token
            return self._update(obj)
        else:
            new_user_token = UserToken(user_id=user_id, token=new_token)
            return self._update(new_user_token)
