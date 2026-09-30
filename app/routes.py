import json

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.ai_service import generate_fitness_plan, update_fitness_plan
from app.database import UserPlan, get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )



@router.post("/generate", response_class=HTMLResponse)
def generate_plan(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        plan = generate_fitness_plan(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        user_plan = UserPlan(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            workout_plan=json.dumps(plan["workout_plan"]),
            nutrition_tip=plan["nutrition_tip"],
            feedback="",
        )

        db.add(user_plan)
        db.commit()
        db.refresh(user_plan)

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "plan": plan,
                "record_id": user_plan.id,
                "user": user_plan,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": str(exc),
            },
            status_code=500,
        )


@router.post("/update/{record_id}", response_class=HTMLResponse)
def update_plan(
    record_id: int,
    request: Request,
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    user_plan = db.get(UserPlan, record_id)

    if not user_plan:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "Fitness plan not found.",
            },
            status_code=404,
        )

    try:
        original_plan = {
            "workout_plan": json.loads(user_plan.workout_plan),
            "nutrition_tip": user_plan.nutrition_tip,
            "recovery_tip": "Follow a suitable recovery routine.",
        }

        updated_plan = update_fitness_plan(
            original_plan=original_plan,
            feedback=feedback,
        )

        user_plan.workout_plan = json.dumps(
            updated_plan["workout_plan"]
        )
        user_plan.nutrition_tip = updated_plan["nutrition_tip"]
        user_plan.feedback = feedback

        db.commit()
        db.refresh(user_plan)

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "plan": updated_plan,
                "record_id": user_plan.id,
                "user": user_plan,
                "updated": True,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": str(exc),
            },
            status_code=500,
        )


@router.get("/nutrition-tip", response_class=HTMLResponse)
def nutrition_tip(
    request: Request,
    goal: str = "general fitness",
):
    tips = {
        "weight loss": (
            "Focus on vegetables, lean protein, whole grains, "
            "hydration, and reasonable portion sizes."
        ),
        "muscle gain": (
            "Include sufficient protein, complex carbohydrates, "
            "healthy fats, and adequate hydration."
        ),
        "general fitness": (
            "Eat a balanced diet with vegetables, fruits, "
            "protein, whole grains, and enough water."
        ),
    }

    tip = tips.get(
        goal.lower(),
        tips["general fitness"],
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "nutrition_only": True,
            "nutrition_tip": tip,
            "goal": goal,
        },
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db),
):
    users = (
        db.query(UserPlan)
        .order_by(UserPlan.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users,
        },
    )


@router.get("/api/users")
def api_users(db: Session = Depends(get_db)):
    users = (
        db.query(UserPlan)
        .order_by(UserPlan.created_at.desc())
        .all()
    )

    return [
        {
            "id": user.id,
            "user_id": user.user_id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "created_at": user.created_at.isoformat(),
        }
        for user in users
    ]