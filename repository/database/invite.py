from sqlalchemy import Column, BigInteger, Boolean, DateTime, String, Integer
from repository.database import database


class Invite(database.base):
    __tablename__ = "user_channels"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    guild = Column(BigInteger)
    uses = Column(Integer, default=0)
    created_at = Column(DateTime)
    inviter = Column(BigInteger)
    invite_code = Column(String)
    revoked = Column(Boolean)
