import json
from typing import Any

from google import genai

from app.config import settings


def _mock_response(goal: str, intensity: str) -> dict[str, Any]:
    return {
        "workout_plan": {
            "title": f"7-Day {goal.title()} Fitness Plan",
            "days": [
                {
                    "day": "Day 1",
                    "workout": "Full Body Strength",
                    "duration": "40 minutes",
                    "notes": f"Intensity: {intensity}",
                },
                {
                    "day": "Day 2",
                    "workout": "Cardio",
                    "duration": "30 minutes",
                    "notes": "Keep a comfortable pace.",
                },
                {
                    "day": "Day 3",
                    "workout": "Lower Body Strength",
                    "duration": "40 minutes",
                    "notes": "Focus on controlled movements.",
                },
                {
                    "day": "Day 4",
                    "workout": "Active Recovery",
                    "duration": "25 minutes",
                    "notes": "Light walking and stretching.",
                },
                {
                    "day": "Day 5",
                    "workout": "Upper Body Strength",
                    "duration": "40 minutes",
                    "notes": "Focus on good form.",
                },
                {
                    "day": "Day 6",
                    "workout": "Cardio + Core",
                    "duration": "35 minutes",
                    "notes": "Finish with light core exercises.",
                },
                {
                    "day": "Day 7",
                    "workout": "Rest and Mobility",
                    "duration": "20 minutes",
                    "notes": "Gentle stretching and recovery.",
                },
            ],
        },
        "nutrition_tip": "Eat balanced meals with enough protein, vegetables, whole grains, and water.",
        "recovery_tip": "Sleep 7-9 hours and allow your body enough time to recover.",
    }


def generate_fitness_plan(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> dict[str, Any]:

    if settings.mock_gemini or not settings.gemini_api_key:
        return _mock_response(goal, intensity)

    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
Create a safe and practical 7-day fitness plan.

User:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Workout intensity: {intensity}

Return ONLY valid JSON in this structure:

{{
  "workout_plan": {{
    "title": "string",
    "days": [
      {{
        "day": "Day 1",
        "workout": "string",
        "duration": "string",
        "notes": "string"
      }}
    ]
  }},
  "nutrition_tip": "string",
  "recovery_tip": "string"
}}

Include exactly 7 days.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def update_fitness_plan(
    original_plan: dict[str, Any],
    feedback: str,
) -> dict[str, Any]:

    if settings.mock_gemini or not settings.gemini_api_key:
        updated = dict(original_plan)
        updated["workout_plan"] = dict(original_plan["workout_plan"])

        days = list(original_plan["workout_plan"]["days"])

        if "cardio" in feedback.lower():
            days.append({
                "day": "Bonus",
                "workout": "Extra Cardio",
                "duration": "20 minutes",
                "notes": "Added based on your feedback.",
            })

        updated["workout_plan"]["days"] = days[:7]
        updated["recovery_tip"] = (
            "Take an additional recovery day if you feel excessive fatigue."
        )

        return updated

    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
Update this fitness plan based on the user's feedback.

Original plan:
{json.dumps(original_plan, indent=2)}

User feedback:
{feedback}

Return ONLY valid JSON using the same structure as the original plan.
Keep exactly 7 workout days.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)