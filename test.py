from dynamodb_fsm import FSMDynamodb
import asyncio

async def all():
    result = await FSMDynamodb().all_value()
    print(result)


asyncio.run(all())
