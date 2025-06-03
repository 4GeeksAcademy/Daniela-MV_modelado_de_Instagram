from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120),nullable=False)
    lastname: Mapped[str] = mapped_column(String(120),nullable=False)
    email:Mapped[str] = mapped_column(String(120),nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers_from_user = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="follow")
    followers_to_user = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="followers")

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id"))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    medias = relationship("Media", back_populates="posts")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")  

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    posts = relationship("Post", back_populates="medias")

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    followers = relationship("User", foreign_keys=[user_to_id], back_populates="followers_to_user")
    follow = relationship("User", foreign_keys=[user_from_id], back_populates="followers_from_user")