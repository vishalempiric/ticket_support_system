import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from temporalio.client import Client
from temporalio.worker import Worker
from activity import my_recurring_activity
from workflow import MyCronWorkflow
import asyncio

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[MyCronWorkflow],
        activities=[my_recurring_activity],
    )
    await worker.run()

asyncio.run(main())
