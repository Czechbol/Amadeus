from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime
from repository.database import database


class UserChannel(database.base):
    __tablename__ = "user_channels"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger)
    guild_name = Column(String)
    channel_id = Column(BigInteger)
    channel_name = Column(String)
    user_id = Column(BigInteger)
    user_name = Column(String)
    is_webhook = Column(Boolean)
    count = Column(BigInteger, default=1)
    last_msg_at = Column(DateTime)

    def __repr__(self):
        return (
            f'<UserChannel idx="{self.idx}" '
            f'guild_id="{self.guild_id}" channel_id="{self.channel_id}" '
            f'channel_name="{self.channel_name}" user_id="{self.user_id}" '
            f'user_name="{self.user_name}" is_webhook="{self.is_webhook}"'
            f'count="{self.user_id}" last_msg_at="{self.is_webhook}">'
        )
