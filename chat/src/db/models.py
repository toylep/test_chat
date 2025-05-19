from datetime import datetime
from sqlalchemy import Float, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()


class User(Base):
    """
    Модель пользователя
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    messages = relationship("Message", back_populates="user")


class Chat(Base):
    """
    Модель чата
    """

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    is_group: Mapped[bool] = mapped_column(Boolean, default=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=True)

    messages = relationship("Message", back_populates="chat")


class Group(Base):
    """
    Модель группы
    """

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    members = relationship("GroupMember", back_populates="group")


class GroupMember(Base):
    """
    Табличка для связи пользователей и групп
    """

    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    group = relationship("Group", back_populates="members")


class Message(Base):
    """
    Модель сообщения
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    timestampt: Mapped[str] = mapped_column(DateTime, default=datetime.now())
    is_readed: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")
