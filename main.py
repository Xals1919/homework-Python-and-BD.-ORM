#Импортируем необходимые библиотеки
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

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

#Варианты из json: O’Reilly | Pearson | Microsoft Press | No starch press
namepublisher = input('Введите Имя автора: ') 
for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == namepublisher).all():
    d = c[3].split('T')
    print(f'{c[0]} | {c[1]} | {c[2]} | {d[0]}')
