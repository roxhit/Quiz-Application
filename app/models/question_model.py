from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class QuizCreate(BaseModel):
    title: str = Field(..., example="General Knowledge Quiz")


class QuizResponse(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    created_at: datetime


class QuestionCreate(BaseModel):
    text: str = Field(..., example="What is the capital of France?")
    options: List[str] = Field(..., example=["Paris", "London", "Berlin", "Madrid"])
    correct_answer: str = Field(..., example="Paris")

    @field_validator("correct_answer")
    def validate_correct_answer(cls, v, values):
        if "options" in values and v not in values["options"]:
            raise ValueError("Correct answer must be one of the options")
        return v


class QuestionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    text: str
    options: List[str]


class AnswerSubmit(BaseModel):
    question_id: str
    selected_answer: str


class QuizSubmitRequest(BaseModel):
    answers: List[AnswerSubmit]


class QuizResult(BaseModel):
    score: int
    total: int
