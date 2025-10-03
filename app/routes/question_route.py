from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime, UTC
from typing import List

from app.models.question_model import (
    QuizCreate,
    QuizResponse,
    QuestionCreate,
    QuestionResponse,
    QuizSubmitRequest,
    QuizResult,
)
from app.config.database import (
    quizzes_collection,
    questions_collection,
    get_current_user,
    get_current_admin,
)

quiz_router = APIRouter()


def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@quiz_router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz: QuizCreate, current_admin: dict = Depends(get_current_admin)
):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")
    current_quiz = quizzes_collection.find_one({"title": quiz.title})
    if current_quiz:
        raise HTTPException(
            status_code=400, detail="Quiz with this title already exists"
        )
    quiz_doc = {"title": quiz.title, "created_at": datetime.now(UTC)}
    result = quizzes_collection.insert_one(quiz_doc)
    new_quiz = quizzes_collection.find_one({"_id": result.inserted_id})
    return serialize_doc(new_quiz)


@quiz_router.post("/{quiz_id}/questions", response_model=QuestionResponse)
async def add_question(quiz_id: str, question: QuestionCreate):
    if not ObjectId.is_valid(quiz_id):
        raise HTTPException(status_code=400, detail="Invalid quiz ID")

    quiz = quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    q_doc = {
        "quiz_id": quiz_id,
        "text": question.text,
        "options": question.options,
        "correct_answer": question.correct_answer,
    }
    result = questions_collection.insert_one(q_doc)
    new_q = questions_collection.find_one({"_id": result.inserted_id})

    return {
        "_id": str(new_q["_id"]),
        "text": new_q["text"],
        "options": new_q["options"],
    }


@quiz_router.get("/{quiz_id}/questions", response_model=List[QuestionResponse])
async def get_quiz_questions(quiz_id: str):
    if not ObjectId.is_valid(quiz_id):
        raise HTTPException(status_code=400, detail="Invalid quiz ID")

    cursor = questions_collection.find({"quiz_id": quiz_id})
    questions = []
    for q in cursor:
        questions.append(
            {"_id": str(q["_id"]), "text": q["text"], "options": q["options"]}
        )
    return questions


@quiz_router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: str,
    submission: QuizSubmitRequest,
    current_user: dict = Depends(get_current_user),
):
    if not ObjectId.is_valid(quiz_id):
        raise HTTPException(status_code=400, detail="Invalid quiz ID")
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    total = len(submission.answers)
    score = 0

    for ans in submission.answers:
        q = questions_collection.find_one(
            {"_id": ObjectId(ans.question_id), "quiz_id": quiz_id}
        )
        if not q:
            raise HTTPException(
                status_code=404, detail=f"Question {ans.question_id} not found"
            )

        if ans.selected_answer.strip().lower() == q["correct_answer"].strip().lower():
            score += 1

    return {"score": score, "total": total}
