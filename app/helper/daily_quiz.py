import requests
from datetime import datetime
from app.config.database import quizzes_collection  # your Mongo collection
from app.models.question_model import Question, DailyQuestionSet
import random


def fetch_and_store_questions():
    url = "https://opentdb.com/api.php?amount=50"
    response = requests.get(url)
    data = response.json()

    if data.get("response_code") != 0:
        raise ValueError("Failed to fetch questions from API")

    for item in data["results"]:
        q_type = "multiple_choice" if item["type"] == "multiple" else "true_false"

        # merge options and shuffle
        options = item["incorrect_answers"] + [item["correct_answer"]]
        random.shuffle(options)

        question_doc = {
            "text": item["question"],
            "type": q_type,
            "options": options,
            "correct_answer": item["correct_answer"],
            "date": datetime.utcnow().date().isoformat(),  # for daily grouping
        }

        quizzes_collection.insert_one(question_doc)

    return {"message": "Questions stored successfully"}
