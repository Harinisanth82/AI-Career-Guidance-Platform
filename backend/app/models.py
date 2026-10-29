import datetime
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, JSON, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from backend.app.database import Base

def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_onboarded = Column(Boolean, default=False)
    target_career_id = Column(String, nullable=True)
    created_at = Column(String, default=utc_now_iso)
    updated_at = Column(String, default=utc_now_iso, onupdate=utc_now_iso)

    # Relationships
    profile = relationship("CareerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="user", cascade="all, delete-orphan")
    evidences = relationship("SkillEvidence", back_populates="user", cascade="all, delete-orphan")
    resumes = relationship("ResumeAnalysis", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    career_analyses = relationship("CareerAnalysis", back_populates="user", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")
    insights = relationship("CareerInsight", back_populates="user", cascade="all, delete-orphan")
    timeline_events = relationship("ProgressTimeline", back_populates="user", cascade="all, delete-orphan")

class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    education = Column(JSON, default=dict)
    technical_skills = Column(JSON, default=list)
    soft_skills = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    experience = Column(JSON, default=dict)
    career_goals = Column(JSON, default=dict)
    work_preferences = Column(JSON, default=dict)
    readiness_score = Column(Integer, default=50)
    readiness_breakdown = Column(JSON, default=dict)
    current_direction = Column(String, default="Software Developer")
    match_percentage = Column(Integer, default=70)
    direction_explanation = Column(Text, default="")
    biggest_opportunity = Column(Text, default="")
    next_best_action = Column(Text, default="")
    created_at = Column(String, default=utc_now_iso)
    updated_at = Column(String, default=utc_now_iso, onupdate=utc_now_iso)

    user = relationship("User", back_populates="profile")

class CareerRole(Base):
    __tablename__ = "career_roles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    what_they_do = Column(JSON, default=list)
    core_technical_skills = Column(JSON, default=list)
    soft_skills = Column(JSON, default=list)
    common_tools = Column(JSON, default=list)
    entry_level_expectations = Column(JSON, default=list)
    suggested_projects = Column(JSON, default=list)
    career_progression = Column(JSON, default=list)
    related_careers = Column(JSON, default=list)

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    current_question_index = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    answers = Column(JSON, default=list)
    category_scores = Column(JSON, default=dict)
    ai_analysis = Column(JSON, default=dict)
    started_at = Column(String, default=utc_now_iso)
    completed_at = Column(String, nullable=True)

    user = relationship("User", back_populates="assessments")

class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    url = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    difficulty = Column(String, index=True, nullable=False)
    estimated_duration = Column(String, default="")
    resource_type = Column(String, default="Guide")
    related_skills = Column(JSON, default=list)
    is_verified = Column(Boolean, default=True)

class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    target_career_id = Column(String, nullable=False)
    target_career_title = Column(String, nullable=False)
    phases = Column(JSON, default=list)
    overall_progress = Column(Integer, default=0)
    generated_at = Column(String, default=utc_now_iso)
    updated_at = Column(String, default=utc_now_iso, onupdate=utc_now_iso)

    user = relationship("User", back_populates="roadmaps")

class SkillEvidence(Base):
    __tablename__ = "skill_evidences"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    skill_name = Column(String, nullable=False)
    evidence_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=True)
    description = Column(Text, default="")
    verified_status = Column(String, default="Evidence Added")
    strength = Column(String, default="Moderate")
    created_at = Column(String, default=utc_now_iso)

    user = relationship("User", back_populates="evidences")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    career_title = Column(String, nullable=False)
    difficulty = Column(String, default="Entry-Level")
    interview_type = Column(String, default="Technical")
    status = Column(String, default="in_progress")
    questions = Column(JSON, default=list)
    answers = Column(JSON, default=list)
    final_summary = Column(JSON, nullable=True)
    created_at = Column(String, default=utc_now_iso)
    completed_at = Column(String, nullable=True)

    user = relationship("User", back_populates="interviews")

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    target_role = Column(String, nullable=False)
    file_name = Column(String, default="Pasted_Resume")
    overall_score = Column(Integer, default=0)
    completeness_score = Column(Integer, default=0)
    keyword_match_score = Column(Integer, default=0)
    impact_score = Column(Integer, default=0)
    detected_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    soft_skills_detected = Column(JSON, default=list)
    sections = Column(JSON, default=list)
    suggestions = Column(JSON, default=list)
    bullet_point_rewrites = Column(JSON, default=list)
    analyzed_at = Column(String, default=utc_now_iso)

    user = relationship("User", back_populates="resumes")

class ChatMessage(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    mode = Column(String, default="local_engine")
    timestamp = Column(String, default=utc_now_iso)

    user = relationship("User", back_populates="chat_messages")

class CareerAnalysis(Base):
    __tablename__ = "career_analyses"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    analysis_date = Column(String, default=utc_now_iso)
    recommended_roles = Column(JSON, default=list)
    readiness_score = Column(Integer, default=0)
    target_role = Column(String, default="")

    user = relationship("User", back_populates="career_analyses")

class CareerInsight(Base):
    __tablename__ = "career_insights"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String, nullable=False)
    observation = Column(Text, nullable=False)
    suggested_action = Column(Text, nullable=False)
    action_route = Column(String, default="/roadmap")
    category = Column(String, default="readiness")
    is_read = Column(Boolean, default=False)
    created_at = Column(String, default=utc_now_iso)

    user = relationship("User", back_populates="insights")

class ProgressTimeline(Base):
    __tablename__ = "progress_timeline"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(String, default=utc_now_iso)
    meta = Column(JSON, default=dict)

    user = relationship("User", back_populates="timeline_events")
