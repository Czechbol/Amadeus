from repository.base_repository import BaseRepository
from repository.database import session
from repository.database.vote import Vote

from datetime import datetime


class VoteRepository(BaseRepository):
    # unknown - pending - verified - kicked - banned

    def add_vote(self, channel_id: int, message_id: int, edit_id: int, date: str):
        """Add new vote"""
        session.add(Vote(channel_id=channel_id, message_id=message_id, edit_id=edit_id, date=date))
        session.commit()

    def get_list(self):
        """Update a specified user with a new verification code"""
        votes = session.query(Vote).all()
        result = []

        if votes is not None:
            for v in votes:
                result.append(v.__dict__)
        else:
            result = None
        return result

    def del_vote(self, channel_id: int = None, message_id: int = None):
        users = (
            session.query(Vote)
            .filter(Vote.message_id == message_id)
            .filter(Vote.channel_id == channel_id)
            .delete()
        )
        session.commit()
        return users
