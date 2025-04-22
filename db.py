'''
Write a wrapper class TableData for database table,
that when initialized with database name and table acts as collection object (implements Collection protocol).
Assume all data has unique values in 'name' column.
So, if presidents = TableData(database_name='example.sqlite', table_name='presidents')

then

    - len(presidents) will give current amount of rows in presidents table in database
    - presidents['Yeltsin'] should return single data row for president with name Yeltsin
    - 'Yeltsin' in presidents should return if president with same name exists in table
    - object implements iteration protocol. i.e. you could use it in for loops:: for president
        in presidents: print(president['name'])
    - all above mentioned calls should reflect most recent data.
        If data in table changed after you created collection instance, your calls should return updated data.
Avoid reading entire table into memory. When iterating through records, start reading the first record,
then go to the next one, until records are exhausted. When writing tests,
it's not always neccessary to mock database calls completely.
Use supplied example.sqlite file as database fixture file.
'''

import sqlite3


class TableData:
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def _connect_db(self):
        # Подключение к бд
        return sqlite3.connect(self.database_name)

    def __len__(self):
        # Число записей
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) from {self.table_name};')
        return cursor.fetchone()[0]

    def __getitem__(self, item: str):
        # Данные по имени
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * from {self.table_name} WHERE name=?;', (item, ))
        return cursor.fetchone()

    def __contains__(self, item: str):
        # Проверка наличия
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * from {self.table_name} WHERE name=?;', (item,))
        return cursor.fetchone() is not None

    def __iter__(self):
        # Итератор
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * from {self.table_name};')
        column = [key[0] for key in cursor.description]
        for row in cursor:
            yield dict(zip(column, row))


if __name__ == "__main__":
    # Тесты
    # Создание класса
    presidents = TableData(database_name='example.sqlite', table_name='presidents')

    print(len(presidents)) # 3

    print(presidents['Yeltsin']) # ('Yeltsin', 999, 'Russia')

    print('Yeltsin' in presidents) # True

    for president in presidents:
        print(president['name']) # Yeltsin -> Trump -> Big Man Tyrone