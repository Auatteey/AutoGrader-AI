from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import json, time

router = APIRouter()

REVIEWS_DIR = Path("data/reviews")
REVIEWS_DIR.mkdir(parents=True, exist_ok=True)

class Review(BaseModel):
    student: str
    exam: str
    problem: str
    details: str

@router.post("/api/reviews/send")
def send_review(review: Review):
    file = REVIEWS_DIR / f"{int(time.time())}_{review.student}.json"
    with open(file, "w") as f:
        json.dump(review.dict(), f, indent=4)
    return {"status":"ok","message":"Review submitted"}

@router.get("/api/reviews/all")
def get_reviews():
    all_reviews=[]
    for f in REVIEWS_DIR.glob("*.json"):
        with open(f) as file:
            all_reviews.append(json.load(file))
    return {"status":"ok","reviews":all_reviews}
