from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class City(Base, TimestampMixin):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    state = Column(String(100), nullable=False)
    country = Column(String(50), default="India")
    is_active = Column(Boolean, default=True)
    
    # Relationships
    localities = relationship("Locality", back_populates="city", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}', state='{self.state}')>"
