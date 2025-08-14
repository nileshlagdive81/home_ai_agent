from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False, default="customer")  # admin, agent, customer
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user_auth = relationship("UserAuth", back_populates="user", uselist=False, cascade="all, delete-orphan")
    property_viewings = relationship("PropertyViewing", back_populates="user", cascade="all, delete-orphan")
    search_queries = relationship("SearchQuery", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
