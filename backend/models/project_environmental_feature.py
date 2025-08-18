from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid

class ProjectEnvironmentalFeature(Base, TimestampMixin):
    __tablename__ = "project_environmental_features"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    solar_water_heating = Column(Boolean, default=False)
    rainwater_harvesting = Column(Boolean, default=False)
    energy_efficient_lighting = Column(Boolean, default=False)
    waste_management_system = Column(Boolean, default=False)
    green_building_certification = Column(String(100))  # LEED, IGBC, etc.
    water_conservation_features = Column(Text)
    energy_conservation_features = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="environmental_features")
    
    def __repr__(self):
        return f"<ProjectEnvironmentalFeature(id={self.id}, project_id={self.project_id}, certification='{self.green_building_certification}')>"
