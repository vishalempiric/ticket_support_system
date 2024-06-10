from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.models.email_model import Email
from src.models.thread import Thread
from src.schemas.email_schema import EmailUpdate
from nylas import Client
import os
import requests



def read_emails_service(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(Email).order_by(desc(Email.created_at)).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching emails") from e


def read_email_service(email_id: str, db: Session):
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        return email
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching email") from e


def update_email_service(email_id: str, email_in: EmailUpdate, db: Session):
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        for field, value in email_in.dict(exclude_unset=True).items():
            setattr(email, field, value)
        email.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(email)
        return email
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating email") from e


def delete_email_service(email_id: str, db: Session):
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        db.delete(email)
        db.commit()
        return {"message": "Email deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting email") from e


def read_threads_service(db: Session, thread_id:str):
    try:
        return db.query(Email).join(Thread, Email.thread_id==thread_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching emails") from e


def get_all_threads_service(db:Session):
    try:
        return db.query(Thread).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching threads") from e


def send_email_service(email:str, subject:str, body:str):
    try:
        nylas = Client(
            os.environ.get('NYLAS_API_KEY'),
            os.environ.get('NYLAS_API_URI')
        )   
        grant_id = os.environ.get("NYLAS_GRANT_ID")

        message = nylas.messages.send(
        grant_id,
        request_body={
            "to": [{ "name": "Name", "email": email}],
            "reply_to": [{ "name": "Name", "email": email}],
            "subject": subject,   
            "body": body,
        }
        )
        return {"message": "Email sent successfully", "response":message}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error sending emails") from e


def add_emails_to_db_service(db:Session):
    url = "https://api.eu.nylas.com/v3/grants/35d17b63-a914-46f0-bb5a-25cbe0e6f6db/messages"
    
    payload = {}
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer nyk_v0_95uvbyB3SffpPvd2MMVpEF4lE6JixKjxW9PhLkD2Hk4Y4YS5aiZlqSkXz07tguYg",
        "Content-Type": "application/json",
    }

    current_date = datetime.utcnow() - timedelta(days=15)

    received_after = int(current_date.timestamp())

    params={'received_after':received_after}


    response = requests.get(url, headers=headers, data=payload, params=params)
    emails = response.json()[
        "data"
    ]  



    for email_data in emails:
        thread = db.query(Thread).filter(Thread.thread_id==email_data["thread_id"]).first()
        if not thread:
            thread = Thread(thread_id = email_data["thread_id"], status = "let me decide", priority="normal")
            db.add(thread)
            db.commit()
            db.refresh(thread) 


        e_id = email_data["id"]
        existing_email = db.query(Email).filter(Email.e_id == e_id).first()
        if not existing_email:
            email = Email(
                thread_model_id = thread.id,
                thread_id=email_data["thread_id"],
                grant_id=email_data["grant_id"],
                e_id=email_data["id"],
                subject=email_data["subject"],
                body=email_data["body"],
                snippet=email_data["snippet"],
                sender_name=email_data["from"][0]["email"],
                sender_email=email_data["from"][0]["email"],
                recipient_name=email_data["to"][0]["email"],
                recipient_email=email_data["to"][0]["email"],
                unread=email_data["unread"],
                starred=email_data["starred"],
                created_at=datetime.fromtimestamp(email_data['created_at']), 
                updated_at=datetime.fromtimestamp(email_data['created_at'])
            )   
            db.add(email)
            db.commit()             
            db.refresh(email)                                                                                         

    return {"message": "Emails added to database"}