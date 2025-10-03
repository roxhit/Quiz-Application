
---

````markdown
# 📝 Online Quiz Application API

A backend API for a simple quiz application built with **FastAPI** and **MongoDB**.  
The API allows user and admin registration/login with JWT authentication, quiz creation, question management, and quiz-taking with scoring.

---

## 🚀 Features

- **User & Admin Authentication**
  - Register and login with JWT tokens.
  - Admins can create quizzes and add questions.

- **Quiz Management**
  - Create a quiz with a title.
  - Add multiple-choice questions (each has a correct answer).

- **Quiz Taking**
  - Fetch all questions for a quiz (without revealing the correct answer).
  - Submit answers and receive a score (`score` and `total`).

- **Test Coverage**
  - Includes sample test cases using `pytest` and `httpx`.

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [MongoDB](https://www.mongodb.com/) – Database
- [Motor](https://motor.readthedocs.io/) – Async Mongo driver
- [PyJWT / python-jose](https://python-jose.readthedocs.io/) – JWT authentication
- [pytest](https://docs.pytest.org/) – Testing framework

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/quiz-api.git
cd quiz-api
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MongoDB

Make sure you have MongoDB running locally:

```bash
mongod
```

(Default URI is `mongodb://localhost:27017` – change in `app/config.py` if needed.)

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

You can explore the Swagger docs here:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/api)

---

## ✅ Running Test Cases

Tests use **pytest** and require MongoDB running.

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

---

## 📌 Assumptions & Design Choices

1. **Role Handling**

   * We don’t store `role` in the database. Instead, we infer it from the collection (`users_collection` vs `admin_collection`).
   * JWT tokens include `"role": "user"` or `"role": "admin"`.

2. **Question Structure**

   * Questions are stored with a `text`, a list of `options`, and one `correct_answer`.
   * When fetching questions for a quiz, the `correct_answer` is **not included** in the response.

3. **Answer Submission**

   * The client sends `{ question_id, selected_answer }`.
   * Scoring is calculated by comparing with the stored `correct_answer`.

4. **ID Handling**

   * Mongo `_id` is always converted to a `str` for responses.

5. **Security**

   * Passwords are hashed before storage (using bcrypt).
   * JWT is used for securing endpoints.

---

## 📚 Example Usage

### Create a Quiz

```bash
POST /quizzes
Authorization: Bearer <token>
{
  "title": "Sports Quiz"
}
```

### Add a Question

```bash
POST /quizzes/{quiz_id}/questions
Authorization: Bearer <token>
{
  "text": "Which country won the FIFA World Cup 2022?",
  "options": ["France", "Argentina", "Brazil", "Germany"],
  "correct_answer": "Argentina"
}
```

### Get Questions

```bash
GET /quizzes/{quiz_id}/questions
Authorization: Bearer <token>
```

### Submit Answers

```bash
POST /quizzes/{quiz_id}/submit
Authorization: Bearer <token>
{
  "answers": [
    { "question_id": "<id>", "selected_answer": "Argentina" }
  ]
}
```

---

## 🏗️ Future Improvements

* Support multiple correct answers per question.
* Add quiz result history per user.
* Admin dashboard endpoints.
* Pagination for quiz/question listing.

---

```
