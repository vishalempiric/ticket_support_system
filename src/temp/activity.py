import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from temporalio import activity

from temporalio import workflow
from sqlalchemy.orm import Session
with workflow.unsafe.imports_passed_through():
    from src.routers.email_router import get_db
    from src.services.email_service import add_emails_to_db_service

@activity.defn
async def my_recurring_activity():
    db: Session = next(get_db())  # Get the DB session
    result = add_emails_to_db_service(db)
    return result
