from bs4 import BeautifulSoup
import requests
import json


URL = "https://markets.businessinsider.com/index/components/s&p_500"


page = requests.get(URL)
bs = BeautifulSoup(page.text, "html.parser")
temp = []
table = bs.find("tbody", "table__tbody")
rows = table.find_all("tr")
for row in rows:
    name = row.find("a").text.strip()  # Имя
    prices = row.find_all("td", class_="table__td")[1].text.strip().split()  # Цены
    changes = row.find_all("td", class_="table__td")[2].text.strip().split()  # Изменения
    changes_percent = row.find_all("td", class_="table__td")[3].text.strip().split()  # Проценты
    date = row.find_all("td", class_="table__td")[4].text.strip().split()  # Дата и время
    mo_3 = row.find_all("td", class_="table__td")[5].text.strip().split()  # 3 месяца
    mo_6 = row.find_all("td", class_="table__td")[6].text.strip().split()  # 6 месяца
    year = row.find_all("td", class_="table__td")[7].text.strip().split()  # 1 год

    print(f"{name=}")
    print(f"{prices=}")
    print(f"{changes=}")
    print(f"{changes_percent=}")
    print(f"{date=}")
    print(f"{mo_3=}")
    print(f"{mo_6=}")
    print(f"{year=}")
    print("-" * 40)
