from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class EverMarried(str, Enum):
    yes = "Yes"
    no = "No"

class WorkType(str, Enum):
    private = "Private"
    self_employed = "Self-employed"
    govt_job = "Govt_job"
    children = "children"
    never_worked = "Never_worked"

class ResidenceType(str, Enum):
    urban = "Urban"
    rural = "Rural"

class SmokingStatus(str, Enum):
    formerly_smoked = "formerly smoked"
    never_smoked = "never smoked"
    smokes = "smokes"
    unknown = "Unknown"

class Customer(BaseModel):
    age: float = Field(..., example=67.0)
    gender: Gender
    hypertension: int = Field(..., example=0, description="0 = No, 1 = Yes")
    heart_disease: int = Field(..., example=1, description="0 = No, 1 = Yes")
    ever_married: EverMarried
    work_type: WorkType
    residence_type: ResidenceType
    avg_glucose_level: Optional[float] = Field(None, example=106.45)
    bmi: float = Field(..., example=36.6)
    smoking_status: SmokingStatus