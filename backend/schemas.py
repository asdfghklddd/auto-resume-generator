from pydantic import BaseModel, Field
from typing import List, Optional

class ContactInfo(BaseModel):
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City, State, or Country")
    linkedin: Optional[str] = Field(None, description="LinkedIn URL or handle")
    github: Optional[str] = Field(None, description="GitHub URL or handle")
    portfolio: Optional[str] = Field(None, description="Personal website or portfolio URL")

class Experience(BaseModel):
    company: str = Field(description="Name of the company or organization")
    title: str = Field(description="Job title or role")
    date_range: str = Field(description="Date range of employment, e.g., 'Jan 2020 - Present'")
    highlights: List[str] = Field(
        description="3-5 bullet points describing achievements using the STAR (Situation, Task, Action, Result) method. Must be highly professional and action-oriented."
    )

class Education(BaseModel):
    institution: str = Field(description="Name of the university or school")
    degree: str = Field(description="Degree obtained, e.g., 'B.S. in Computer Science'")
    date_range: str = Field(description="Date range of attendance or graduation year")
    gpa: Optional[str] = Field(None, description="GPA if applicable and impressive")

class Project(BaseModel):
    name: str = Field(description="Name of the project")
    technologies: List[str] = Field(description="List of technologies, languages, or tools used")
    description: List[str] = Field(
        description="1-3 bullet points describing the project, focusing on impact and technical complexity."
    )

class ResumeData(BaseModel):
    full_name: str = Field(description="The full name of the candidate")
    professional_title: str = Field(description="A short professional title, e.g., 'Full Stack Developer'")
    summary: str = Field(description="A 2-3 sentence professional summary highlighting top skills and career goals.")
    contact: ContactInfo
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    skills: List[str] = Field(description="A list of core technical and professional skills, maximum 15 items.")
