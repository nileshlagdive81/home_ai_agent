from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserAuth(Base):
    __tablename__ = "user_auth"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="user_auth")
    
    def __repr__(self):
        return f"<UserAuth(user_id={self.user_id})>"
