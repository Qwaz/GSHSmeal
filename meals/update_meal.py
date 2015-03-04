from datetime import date, datetime, timedelta
from threading import Thread
import re

from django.db import transaction
from bs4 import BeautifulSoup, Tag
import requests

from meals.models import Update, Food, Meal, Menu
from utils.iso_calendar import iso_to_gregorian


class MealSet():
    def __init__(self, meal_type):
        self._meal_count = 0
        self.meals = []
        self.foods = []

        for i in range(7):
            self.meals.append(Meal())
            self.meals[i].meal_type = meal_type
            self.foods.append([])

    def _count_step(self):
        self._meal_count += 1
        if self._meal_count == 7:
            self._meal_count = 0

    def set_timestamp(self, data):
        setattr(self.meals[self._meal_count], 'date', datetime.strptime(data[0:10], "%Y.%m.%d").date())
        self._count_step()

    def set_foods(self, data):
        for food_name in data.split('<br/>')[:-1]:
            allergy = 0
            allergy_mark = '⑬⑫⑪⑩⑨⑧⑦⑥⑤④③②①'
            for i in range(len(allergy_mark)):
                if food_name[-1] == allergy_mark[i]:
                    allergy ^= 1 << i
                    food_name = food_name[:-1]

            food_name = re.sub(r'([\-=*]|\((초|중|고|조|주식)\))*$', '', food_name)
            food_name = re.sub(r'[0-9]+', '', food_name)

            food = Food.objects.get_or_create(name=food_name, allergy=allergy, is_snack=False)[0]
            self.foods[self._meal_count].append(food)
        self._count_step()

    def set_etc(self, column_name, data):
        if column_name == 'food_from':
            setattr(self.meals[self._meal_count], column_name, data)
        else:
            try:
                setattr(self.meals[self._meal_count], column_name, float(data))
            except ValueError:
                setattr(self.meals[self._meal_count], column_name, 0.0)
        self._count_step()

    def save(self):
        for i in range(7):
            self.meals[i].save()
            for food in self.foods[i]:
                Menu.objects.create(food=food, meal=self.meals[i])


class ParseThread(Thread):
    @transaction.atomic
    def run(self):
        now = self.get_update_start()
        last = self.get_update_end()

        while now < last:
            now += timedelta(days=7)
            self.update_meal(now)

    def update_meal(self, meal_date):
        iso_calendar = meal_date.isocalendar()

        obj, created = Update.objects.get_or_create(iso_year=iso_calendar[0], iso_week=iso_calendar[1])

        if created:
            for i in range(1, 4):
                payload = {
                    'insttNm': '경기과학고등학교',
                    'schulCode': 'J100000447',
                    'schulCrseScCode': '4',
                    'schulKndScCode': '04',
                    'schYmd': meal_date.strftime('%Y.%m.%d'),
                    'schMmealScCode': str(i)
                }
                r = requests.post('http://hes.goe.go.kr/sts_sci_md01_001.do', payload)

                soup = BeautifulSoup(r.text)

                ms = MealSet(i)
                row_func = {
                    0: ms.set_timestamp, 2: ms.set_foods, 15: ms.set_etc,
                    17: ms.set_etc, 18: ms.set_etc, 19: ms.set_etc, 20: ms.set_etc, 21: ms.set_etc,
                    22: ms.set_etc, 23: ms.set_etc, 24: ms.set_etc, 25: ms.set_etc, 26: ms.set_etc
                }

                row_args = {
                    15: 'food_from', 17: 'kcal', 18: 'carbohydrate', 19: 'protein',
                    20: 'fat', 21: 'vitamin_a', 22: 'thiamine', 23: 'riboflavin',
                    24: 'vitamin_c', 25: 'calcium', 26: 'iron'
                }

                row_count = 0
                tr_count = len(soup.findAll('tr'))

                for row in soup.findAll('tr'):
                    if tr_count < 27 and row_count == 2:
                        row_count += 1

                    for data in (row.findAll('th') + row.findAll('td'))[1:]:
                        a = data.contents
                        if len(a):
                            tmp_text = ''.join(map(lambda x: str(x) if type(x) == Tag else x, a))
                        else:
                            tmp_text = ''

                        if row_count in row_func:
                            if row_count in row_args:
                                row_func[row_count](data=tmp_text, column_name=row_args[row_count])
                            else:
                                row_func[row_count](data=tmp_text)
                    row_count += 1

                ms.save()

    def get_update_start(self):
        start_iso = Update.objects.order_by('-iso_year', '-iso_week').first()
        if start_iso is None:
            # 데이터가 존재하지 않는 경우 2014년 2월 17일부터 파싱 시작
            start_iso = date(2014, 2, 17).isocalendar()[:2]
        else:
            # 그렇지 않은 경우 마지막 업데이트부터 파싱 시작
            start_iso = (start_iso.iso_year, start_iso.iso_week)

        return iso_to_gregorian(start_iso[0], start_iso[1], 1)

    def get_update_end(self):
        # 내일 날짜의 년/주를 선택
        last_iso = (date.today()+timedelta(days=1)).isocalendar()[:2]
        return iso_to_gregorian(last_iso[0], last_iso[1], 1)

    def check_date(self):
        return self.get_update_start() < self.get_update_end()

parseThread = ParseThread()


def update_meals():
    global parseThread

    # 현재 급식 업데이트 중인지를 반환
    if parseThread.is_alive():
        return True

    parseThread = ParseThread()
    if parseThread.check_date():
        parseThread.start()
        return True
    else:
        return False
