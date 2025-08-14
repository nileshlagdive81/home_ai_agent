from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class NearbyCategory(Base, TimestampMixin):
    __tablename__ = "nearby_categories"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<NearbyCategory(id={self.id}, name='{self.name}')>"
