import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from temporalio.client import Client
import asyncio
from src.temp.workflow import MyCronWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    # # Schedule the workflow to run every 2 minutes using cron expression
    cron_schedule = "* * * * *"   


    await client.start_workflow(
        MyCronWorkflow.run,
        id="my-cron-workflow-id",
        task_queue="my-task-queue",
        cron_schedule=cron_schedule,
    )

asyncio.run(main())
