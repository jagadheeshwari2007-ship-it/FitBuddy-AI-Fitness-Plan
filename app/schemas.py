from typing import Optional

from pydantic import BaseModel, Field


class FitnessInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=300)
    goal: str = Field(min_length=2, max_length=100)
    intensity: str = Field(min_length=2, max_length=50)


class FeedbackInput(BaseModel):
    feedback: str = Field(min_length=2, max_length=1000)


class WorkoutDay(BaseModel):
    day: str
    workout: str
    duration: str
    notes: Optional[str] = None


class WorkoutPlan(BaseModel):
    title: str
    days: list[WorkoutDay]


class AIPlanResponse(BaseModel):
    workout_plan: WorkoutPlan
    nutrition_tip: str
    recovery_tip: str