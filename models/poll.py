from sqlalchemy import ForeignKey, Integer, String, Boolean,Column
from sqlalchemy.orm import relationship, declarative_base

Base=declarative_base()

class Poll(Base):
    __tablename__ = "polls"

    id =  Column(Integer, primary_key = True, index = True)
    question = Column(String, index = True, nullable = False) 
    
    options = relationship("Option", back_populates = "poll", cascade="all, delete-orphan")
    
class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    votes = Column(Integer, default=0)

    poll_id = Column(Integer, ForeignKey("polls.id"))

    poll = relationship("Poll", back_populates="options")
    
