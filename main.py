#Импортируем необходимые библиотеки
import json
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from pprint import pprint

#data source name
DSN = 'postgresql://postgres:lakI1003@localhost:5432/homeworkORM'
engine = sqlalchemy.create_engine(DSN)

#вызываем функцию создания аблиц
create_tables(engine)

#Создаем ссесию
Session = sessionmaker(bind=engine)
session=Session()

#Открываем файл json и сохраняем в переменную
with open('homework Python и БД. ORM/tests_data.json', encoding='utf-8') as f:
    data = json.load(f)

for n in data:#Перебираем переменную
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[n.get('model')]
    session.add(model(id=n.get('pk'), **n.get('fields')))
session.commit()

def get_shop(namepublisher):
    all_tables = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Sale.stock).\
        join(Stock.shop).\
        join(Stock.book).\
        join(Book.publisher)
    if namepublisher.isdigit():
        dasd = all_tables.filter(Publisher.id == namepublisher).all()
    else:
        dasd = all_tables.filter(Publisher.name == namepublisher).all()
    for c in dasd:
        print(f'{c[0]: <40} | {c[1]: <10} | {c[2]: <8} | {datetime.strftime(datetime.strptime(c[3], "%Y-%m-%dT%H:%M:%S.%fZ"), "%d-%m-%Y")}')

#Варианты из json: O’Reilly | Pearson | Microsoft Press | No starch press
if __name__ == '__main__':
    namepublisher = input('Введите Имя или номер автора: ') 
    get_shop(namepublisher)

    __pucache__