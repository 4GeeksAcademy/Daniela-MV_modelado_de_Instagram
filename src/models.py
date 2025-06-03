from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_post= Table(
    "user_post",
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120),nullable=False)
    lastname: Mapped[str] = mapped_column(String(120),nullable=False)
    email:Mapped[str] = mapped_column(String(120),nullable=False)

    post_user:Mapped[list["Post"]]=relationship(
        secondary= user_post,
        back_populates= "user_who_post_user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_who_post_user:Mapped[list["User"]]=relationship(
        secondary= user_post,
        back_populates= "post_user" 
    )

    def serialize(self):
        return {
            "id": self.id,
        }

# class Comment(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     comment_text: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
#     author_id: Mapped[int] = mapped_column(nullable=False)
#     post_id: Mapped[int] = mapped_column(nullable=False)
    


#     def serialize(self):
#         return {
#             "id": self.id,
#             "comment_text": self.comment_text,
#             "author_id": self.author_id,
#              "post_id": self.post_id,
#         }


