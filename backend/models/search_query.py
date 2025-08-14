from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base

class SearchQuery(Base):
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    query_text = Column(Text, nullable=False)
    detected_intent = Column(String(100), index=True)
    extracted_entities = Column(JSON)
    search_results_count = Column(Integer)
    
    # Relationships
    user = relationship("User", back_populates="search_queries")
    
    def __repr__(self):
        return f"<SearchQuery(id={self.id}, intent='{self.detected_intent}', query='{self.query_text[:50]}...')>"
