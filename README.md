# FitBuddy – AI Fitness Plan Generator

FitBuddy is a web application that generates personalized 7-day fitness plans using AI.

## Features

- Personalized 7-day workout plan
- Nutrition tips
- Recovery tips
- Feedback-based plan updates
- User plan storage using SQLite
- View all generated user plans
- FastAPI backend
- Jinja2 HTML frontend
- Gemini AI integration

## Project Structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── ai_service.py
│   └── routes.py
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── error.html
│   └── all_users.html
├── tests/
│   └── test_app.py
├── data/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md