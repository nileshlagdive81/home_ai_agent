from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base

class PropertyType(Base):
    __tablename__ = "property_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    projects = relationship("Project", back_populates="property_type", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PropertyType(id={self.id}, name='{self.name}')>"
