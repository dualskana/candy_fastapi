import datetime

from sqlalchemy import Integer, ForeignKey, Column, String, DateTime
from sqlalchemy.orm import relationship

from db.database import Base


class Letter(Base):
    __tablename__ = "letters"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    images = Column(String, nullable=True)
    audio = Column(String, nullable=True)
    video = Column(String, nullable=True)
    type = Column(Integer, default=1)
    author_id = Column(Integer, ForeignKey("users.id"))
    create_time = Column(DateTime, default=datetime.datetime.utcnow())

    author = relationship("User", back_populates="letters")
