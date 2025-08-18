from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Numeric, ARRAY, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid

class RoomSpecification(Base, TimestampMixin):
    __tablename__ = "room_specifications"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    property_id = Column(String, ForeignKey("properties.id"), nullable=False)
    room_name = Column(String(100), nullable=False)
    room_type = Column(String(50), nullable=False)  # bedroom, living, kitchen, bathroom, balcony
    length_feet = Column(Numeric(5, 2))
    width_feet = Column(Numeric(5, 2))
    area_sqft = Column(Numeric(8, 2))
    direction = Column(String(50))  # North, South, East, West, NE, NW, SE, SW
    features = Column(ARRAY(Text))  # Array of features like ['Built-in wardrobe', 'Garden view']
    
    # Relationships
    property = relationship("Property", back_populates="room_specifications")
    
    def __repr__(self):
        return f"<RoomSpecification(id={self.id}, room_name='{self.room_name}', room_type='{self.room_type}')>"
