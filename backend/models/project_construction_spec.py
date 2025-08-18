from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid

class ProjectConstructionSpec(Base, TimestampMixin):
    __tablename__ = "project_construction_specs"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    structure_type = Column(String(100))  # RCC frame, steel frame, etc.
    wall_material = Column(String(100))  # AAC blocks, bricks, etc.
    flooring_material = Column(String(100))  # Vitrified tiles, marble, etc.
    ceiling_type = Column(String(100))  # POP, gypsum, etc.
    electrical_specs = Column(Text)  # Wiring, switches, etc.
    plumbing_specs = Column(Text)  # Pipes, fittings, etc.
    paint_specs = Column(Text)  # Interior/exterior paint types
    
    # Relationships
    project = relationship("Project", back_populates="construction_specs")
    
    def __repr__(self):
        return f"<ProjectConstructionSpec(id={self.id}, project_id={self.project_id}, structure_type='{self.structure_type}')>"
