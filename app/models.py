from .database import Base 
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) 
     # This line establishes a foreign key relationship with the users table, linking each post to its owner. The ondelete="CASCADE" option ensures that if a user is deleted, all their associated posts will also be deleted automatically.
    owner = relationship("User")  # This line sets up a relationship between the Post and User models, allowing easy access to the owner of a post through the owner attribute.

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable = False, primary_key = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    