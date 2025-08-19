from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class ProjectMedia(Base, TimestampMixin):
    """ProjectMedia model for storing project images and videos"""
    __tablename__ = "project_media"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    property_id = Column(String, ForeignKey("properties.id"), nullable=True)
    
    # Media file information
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # Relative path from project root
    file_type = Column(String(20), nullable=False)  # 'image' or 'video'
    mime_type = Column(String(100), nullable=True)  # e.g., 'image/jpeg', 'video/mp4'
    file_size_bytes = Column(Integer, nullable=True)
    
    # Media categorization
    media_category = Column(String(50), nullable=False)  # 'exterior', 'interior', 'floor_plan', 'amenity', 'location', 'video_tour'
    is_primary = Column(Boolean, default=False)  # Primary image for project
    is_featured = Column(Boolean, default=False)  # Featured in listings
    
    # Display properties
    alt_text = Column(String(255), nullable=True)  # Alt text for accessibility
    caption = Column(Text, nullable=True)  # Optional caption
    sort_order = Column(Integer, default=0)  # For ordering in galleries
    
    # Metadata
    width = Column(Integer, nullable=True)  # For images/videos
    height = Column(Integer, nullable=True)  # For images/videos
    duration_seconds = Column(Integer, nullable=True)  # For videos
    
    # Status and tracking
    is_active = Column(Boolean, default=True)
    
    # Relationships - no backref to avoid conflicts
    project = relationship("Project", overlaps="media")
    property = relationship("Property", overlaps="media")
    
    def __repr__(self):
        return f"<ProjectMedia(id={self.id}, type='{self.file_type}', category='{self.media_category}', path='{self.file_path[:50]}...')>"
