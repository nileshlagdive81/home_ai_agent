from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Date, Numeric
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid

class ProjectExpertReview(Base, TimestampMixin):
    __tablename__ = "project_expert_reviews"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    location_rating = Column(Numeric(3, 1))  # 4.8/5
    construction_quality_rating = Column(Numeric(3, 1))
    investment_potential_rating = Column(Numeric(3, 1))
    overall_rating = Column(Numeric(3, 1))
    expert_name = Column(String(200))
    review_date = Column(Date)
    review_summary = Column(Text)
    detailed_review = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="expert_reviews")
    
    def __repr__(self):
        return f"<ProjectExpertReview(id={self.id}, project_id={self.project_id}, overall_rating={self.overall_rating})>"
