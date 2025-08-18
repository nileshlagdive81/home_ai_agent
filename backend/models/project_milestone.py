from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid

class ProjectMilestone(Base, TimestampMixin):
    __tablename__ = "project_milestones"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    milestone_name = Column(String(100), nullable=False)  # Foundation, Structure, Interiors, etc.
    status = Column(String(50), nullable=False)  # completed, in_progress, pending
    completion_date = Column(Date)
    planned_date = Column(Date)
    description = Column(Text)
    progress_percentage = Column(Integer)  # 0-100
    sort_order = Column(Integer)
    
    # Relationships
    project = relationship("Project", back_populates="milestones")
    
    def __repr__(self):
        return f"<ProjectMilestone(id={self.id}, project_id={self.project_id}, milestone_name='{self.milestone_name}', status='{self.status}')>"
