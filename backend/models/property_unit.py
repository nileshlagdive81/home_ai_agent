from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class PropertyUnit(Base, TimestampMixin):
    __tablename__ = "property_units"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    unit_number = Column(String(50))
    floor_number = Column(Integer)
    bhk = Column(Integer, nullable=False, index=True)  # 1, 2, 3, 4, 5+
    carpet_area_sqft = Column(Numeric(8, 2))
    built_up_area_sqft = Column(Numeric(8, 2))
    super_built_up_area_sqft = Column(Numeric(8, 2))
    price_per_sqft = Column(Numeric(10, 2))
    total_price = Column(Numeric(15, 2), index=True)
    booking_amount = Column(Numeric(12, 2))
    is_available = Column(Boolean, default=True)
    is_booked = Column(Boolean, default=False)
    is_sold = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="property_units")
    property_images = relationship("PropertyImage", back_populates="unit", cascade="all, delete-orphan")
    property_viewings = relationship("PropertyViewing", back_populates="unit", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PropertyUnit(id={self.id}, bhk={self.bhk}, price={self.total_price})>"
