from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config import SessionLocal
from src.schemas.email_schema import EmailUpdate, EmailResponse
    

from src.services.email_service import (
    read_emails_service,
    read_email_service,
    update_email_service,
    delete_email_service,
    read_threads_service,
    send_email_service,
    get_all_threads_service,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


email_router = APIRouter()


@email_router.get("/emails/", response_model=list[EmailResponse])
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return read_emails_service(db, skip, limit)


@email_router.get("/emails/{email_id}")
def read_email(email_id: str, db: Session = Depends(get_db)):
    return read_email_service(email_id, db)


@email_router.put("/emails/{email_id}")
def update_email(email_id: str, email_in: EmailUpdate, db: Session = Depends(get_db)):
    return update_email_service(email_id, email_in, db)


@email_router.delete("/emails/{email_id}")
def delete_email(email_id: str, db: Session = Depends(get_db)):
    return delete_email_service(email_id, db)


@email_router.get("/threads/{thread_id}")
def read_threads(thread_id: str, db: Session = Depends(get_db)):
    return read_threads_service(db, thread_id)


@email_router.post("/send-mail/")
def send_mail(email: str, subject: str, body: str):
    return send_email_service(email, subject, body)

        
@email_router.get("/all-threads/")
def get_all_threads(db: Session = Depends(get_db)):
    return get_all_threads_service(db)


# @email_router.post("/add_emails_to_db/")
# def add_emails_to_db(db: Session = Depends(get_db)):
#     return add_emails_to_db_service(db)
