from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from src.database.models import Users
from src.schemas import UserModel, UserEmailModel


async def get_users(db: Session):
    users = db.query(Users).all()
    return users


async def get_user(user_id: int, db: Session):
    user = db.query(Users).filter_by(id=user_id).first()
    return user


async def create_user(body: UserModel, db: Session):
    user = Users(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(body: UserModel, user_id: int, db: Session):
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.email = body.email
        user.phone_number = body.phone_number
        user.born_date = body.born_date
        user.description = body.description
        db.commit()
    return user


async def update_user_email(body: UserEmailModel, user_id: int, db: Session):
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        user.email = body.email
        db.commit()
    return user


async def remove_user(user_id: int, db: Session):
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def search_user(db: Session, q: str, skip: int, limit: int):
    query = db.query(Users)
    if q:
        query = query.filter(
            or_(
                Users.first_name.ilike(f"%{q}%"),
                Users.last_name.ilike(f"%{q}%"),
                Users.email.ilike(f"%{q}%"),
            )
        )
    users = query.offset(skip).limit(limit)
    return users


async def birthdays_per_week(db: Session, days: int, skip: int, limit: int):
    today = datetime.now().date()
    date_to = today + timedelta(days=days)

    upcoming_birthdays_filter = (
        func.to_char(Users.born_date, "MM-DD") >= today.strftime("%m-%d")
    ) & (func.to_char(Users.born_date, "MM-DD") <= date_to.strftime("%m-%d"))

    birthday_users = (
        db.query(Users)
        .filter(upcoming_birthdays_filter)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return birthday_users
