from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class NearbyCategory(Base, TimestampMixin):
    __tablename__ = "nearby_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)  # UUID type
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    
    def __repr__(self):
        return f"<NearbyCategory(id={self.id}, name='{self.name}')>"
