from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Property(Base, TimestampMixin):
    """Property model mapping to the properties table"""
    __tablename__ = "properties"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    property_type = Column(String(100), nullable=True)
    bhk_count = Column(Numeric(3, 1), nullable=True)  # 1.0, 2.0, 3.5, etc.
    carpet_area_sqft = Column(Numeric(8, 2), nullable=True)
    super_builtup_area_sqft = Column(Numeric(8, 2), nullable=True)
    floor_number = Column(Integer, nullable=True)
    facing = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    sell_price = Column(Numeric(15, 2), nullable=False, index=True)
    floor_plan_url = Column(String(500), nullable=True)  # URL for floor plan image
    
    # Relationships
    project = relationship("Project", back_populates="properties")
    room_specifications = relationship("RoomSpecification", back_populates="property", cascade="all, delete-orphan")
    
    # Media relationship
    media = relationship("ProjectMedia", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Property(id={self.id}, bhk={self.bhk_count}, price={self.sell_price})>"
