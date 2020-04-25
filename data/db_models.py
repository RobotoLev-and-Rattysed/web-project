import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    vk_user = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    discord_user = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)

    conversations = orm.relation("Conversation", back_populates='user_id')

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # jobs = orm.relation("Jobs", back_populates='team_leader_object')
    # departments = orm.relation("Department", back_populates='chief_object')

    def __repr__(self):
        return f'<User> {self.id} {self.login}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Conversation(SqlAlchemyBase):
    __tablename__ = 'conversations'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    vk_conversation_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    discord_guild_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class VkConversation(SqlAlchemyBase):
    __tablename__ = 'vk_conversations'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    vk_chat = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    vk_leader = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    vk_moderators = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class DiscordGuild(SqlAlchemyBase):
    __tablename__ = 'discord_guilds'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    discord_server = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    discord_leader = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    discord_moderator_role = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    discord_mute_role = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
