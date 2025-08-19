from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    name = Column(String(200), nullable=False)
    developer_id = Column(String, ForeignKey("developers.id"))
    project_status = Column(String(50), default="under_construction")  # under_construction, ready_to_move, completed
    total_units = Column(Integer)
    total_floors = Column(Integer)
    possession_date = Column(DateTime)
    rera_number = Column(String(100))
    description = Column(Text)
    project_type = Column(String(50))  # residential, commercial, mixed
    video_url = Column(String(500), nullable=True)  # URL for project video
    
    # Relationships
    properties = relationship("Property", back_populates="project", cascade="all, delete-orphan")
    project_locations = relationship("ProjectLocation", back_populates="project", cascade="all, delete-orphan")
    project_amenities = relationship("ProjectAmenity", backref="project", cascade="all, delete-orphan")
    
    # New relationships for project details
    construction_specs = relationship("ProjectConstructionSpec", back_populates="project", cascade="all, delete-orphan")
    environmental_features = relationship("ProjectEnvironmentalFeature", back_populates="project", cascade="all, delete-orphan")
    expert_reviews = relationship("ProjectExpertReview", back_populates="project", cascade="all, delete-orphan")
    safety_features = relationship("ProjectSafetyFeature", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("ProjectMilestone", back_populates="project", cascade="all, delete-orphan")
    
    # Media relationship - using viewonly to avoid conflicts
    media = relationship("ProjectMedia", viewonly=True)
    
    # Nearby places relationship
    nearby_places = relationship("NearbyPlace", back_populates="project", cascade="all, delete-orphan")
    
    # Project nearby relationship (for the junction table)
    project_nearby = relationship("ProjectNearby", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.project_status}')>"
