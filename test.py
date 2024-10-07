from dynamodb_fsm import FSMDynamodb
import asyncio
# from handlers.question import Shedule
from app.api.user_api import Shedule
from datetime import datetime

async def all():
    result = FSMDynamodb().all_value()
    print(result)

def delete():
    data = ['fsm:980314213:980314213:aiogd:stack:', 'fsm:980314213:980314213:aiogd:context:oeMKX9', 'fsm:980314213:980314213:aiogd:context:lTGyx2', 'fsm:980314213:980314213:aiogd:context:F95JG6', 'fsm:980314213:980314213:aiogd:context:9vpGP4', 'fsm:980314213:980314213:aiogd:context:8P1sD9', 'fsm:980314213:980314213:aiogd:context:0eHBo4']
    for i in data:
        FSMDynamodb().delete_note(key=i)

# asyncio.run(all())
# delete()
exp = datetime.now().strftime("%d.%m.%Y")
print(exp)
