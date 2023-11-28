from .database import db

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    avatar = Column(String)
    birthday = Column(DateTime)
    last_updated = Column(DateTime, default=db.func.now())
    online = Column(Boolean, default=False)  # 新增字段，表示用户在线状态

    messages = relationship("Message", back_populates="user")
    user_rooms = relationship("UserRoom", back_populates="user")
    friendships = relationship("Friendship", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    capacity = Column(Integer)
    last_updated = Column(DateTime, default=db.func.now())

    meetings = relationship("Meeting", back_populates="room")
    messages = relationship("Message", back_populates="room")
    user_rooms = relationship("UserRoom", back_populates="room")

class UserRoom(db.Model):
    __tablename__ = 'user_rooms'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)

    user = relationship("User", back_populates="user_rooms")
    room = relationship("Room", back_populates="user_rooms")

class Friendship(db.Model):
    __tablename__ = 'friendships'
    
    user_id1 = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_id2 = Column(Integer)

    user = relationship("User", back_populates="friendships")

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    meeting_link = Column(String)
    password = Column(String)
    last_updated = Column(DateTime, default=db.func.now())

    room_id = Column(Integer, ForeignKey('rooms.id'))
    room = relationship("Room", back_populates="meetings")

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    content = Column(String)
    sent_time = Column(DateTime)

    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))

    user = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")
