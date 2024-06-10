from temporalio import workflow
from datetime import timedelta
from src.temp.activity import my_recurring_activity

from temporalio import workflow

@workflow.defn
class MyCronWorkflow:
    @workflow.run
    async def run(self) -> None:
        result = await workflow.execute_activity(
            my_recurring_activity,
            schedule_to_close_timeout=timedelta(minutes=1),
        )
        print(f"Activity result: {result}")


