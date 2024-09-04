from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Searchterms(Base):
    __tablename__ = "search_terms"
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True)
    
    generated_content_id = Column(Integer, ForeignKey('generated_content.id'))
    sentiment_analysis_id = Column(Integer, ForeignKey('sentiment_analysis.id'))
    
    generated_content = relationship("GeneratedContent", back_populates="search_terms", uselist=False)
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="search_terms", uselist=False)
    

class GeneratedContent(Base):
    __tablename__ = "generated_content"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    search_terms = relationship("Searchterms", back_populates="generated_content", uselist=False)
    

class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"
    id = Column(Integer, primary_key=True, index=True)
    readability = Column(String)
    sentiment = Column(String)
    search_terms = relationship("Searchterms", back_populates="sentiment_analysis", uselist=False)
