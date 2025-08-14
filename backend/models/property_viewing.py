from sqlalchemy import Column, String, Boolean, ForeignKey, Date, Time, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class PropertyViewing(Base, TimestampMixin):
    __tablename__ = "property_viewings"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    unit_id = Column(String, ForeignKey("properties.id"), nullable=True)
    viewing_date = Column(Date, nullable=False)
    viewing_time = Column(Time, nullable=False)
    status = Column(String(20), default="scheduled")  # scheduled, confirmed, completed, cancelled
    agent_notes = Column(Text)
    customer_notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="property_viewings")
    project = relationship("Project", back_populates="property_viewings")
    
    def __repr__(self):
        return f"<PropertyViewing(id={self.id}, date={self.viewing_date}, status='{self.status}')>"
