import requests
from datetime import datetime, timedelta
from os import getenv

from app.config.config import TGbot, StudyConfig

class UserApi():
    def __init__(self, path='/'):
        pass

    def schedule(self, week: int, day: str):
        response = requests.get(TGbot().shedule)
        data: dict = response.json()
        return data[str(week)][day.upper()]

    # def contingent(self, name: str) -> dict | bool:
    #     response = requests.get(bot_config.contingent)
    #     data: dict = response.json()
    #     search_name = name.title()
    #     return data.get(search_name, False)

    # def get_task(self, category='mechanic', level=10, num=0):
    #     token = bot_config.task_api_token
    #     api_url = bot_config.task_api_url
    #     url = f'{api_url}/task_book/token={token}category={category}_level={level}num={num}'
    #     response = requests.get(url)
    #     return response.json()

class Shedule:
    def __init__(self, connect=UserApi()) -> None:
        self.study = StudyConfig()
        self.connect = connect
        self.weekdays = self.study.weekday

    def data(self) -> str:
        return [self._shedule_day(day=item) for item in self.study.select_day]

    def _shedule_day(self, day: str = 'today') -> dict:
        date_to = self.study.select_day.index(day)
        calendar, data = self.go_day(date_to)
        shedule: dict = self.connect.schedule(week=((calendar.week+1) % 2),
                              day=self.weekdays[calendar.weekday])
        text = '\n'.join([f'<i>{key}</i>: {value}' for key, value in shedule.items()])
        return {
            'text': f'<b>{self.weekdays[calendar.weekday]}, {data}</b>\n\n{text}',
            'day': day,
            'id': self.keyboard(day, self.study)
            }

    @staticmethod
    def go_day(day: int):
        need_day = datetime.now() + timedelta(days=day)
        return need_day.isocalendar(), need_day.strftime("%d.%m.%Y")

    @staticmethod
    def keyboard(day: str, study: StudyConfig):
        days: list = study.select_day.copy()
        days.remove(day)
        return days
