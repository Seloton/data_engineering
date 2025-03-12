from bs4 import BeautifulSoup
import requests
import datetime
import json


def dollar_value() -> float:
    # Получает текущий курс доллара по данным ЦБ РФ
    date = datetime.date.today()
    page = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime('%d/%m/%Y')}")
    soup = BeautifulSoup(page.text, "xml")
    return float(soup.find('Valute', ID='R01235').find('Value').text.replace(',', '.'))


def link_parser() -> list:
    # Парсер доступных страниц и ссылок на акции с каждой страницы
    links = list()
    page = requests.get(f"https://markets.businessinsider.com/index/components/s&p_500")
    soup = BeautifulSoup(page.text, "lxml")
    # Находим доступное количество страниц для sp500
    number_pages = len(soup.find("div", "finando_paging margin-top--small").find_all("a"))
    # Проходимся по каждой странице и собираем ссылки в список
    for i in range(1, number_pages + 1):
        page = requests.get(f"https://markets.businessinsider.com/index/components/s&p_500?p={i}")
        soup = BeautifulSoup(page.text, "lxml")
        table = soup.find("tbody", "table__tbody")
        links += [f'https://markets.businessinsider.com{link.get("href")}' for link in table.find_all("a")]
    return links


def parser() -> dict:
    links = link_parser()
    stock_date = []
    for stock_link in links:
        page = requests.get(stock_link)
        soup = BeautifulSoup(page.text, "lxml")
        stock_dict = dict()
        stock_dict["code"] = soup.find("span", "price-section__category").text.strip().split(" , ")[-1]
        stock_dict["name"] = soup.find("span", "price-section__label").text
        stock_dict["price"] = round(float(soup.find("span", "price-section__current-value").text) * dollar_value(), 2)
        stock_dict["P/E"] = float(soup.find("div", "snapshot__data-item padding-right--zero").text.split()[0])
        # stock_dict["growth"] = None  # Сделать!!!
        week_lower = float(soup.find("div", "snapshot__data-item snapshot__data-item--small").text.split()[0])
        week_higher = float(soup.find("div", "snapshot__data-item snapshot__data-item--small snapshot__data-item--right").text.split()[0])
        stock_dict["potential profit"] = round((week_lower / week_higher) * 100, 2)  # Перевести в проценты и переписать чтобы брал за 52 недели
        stock_date.append(stock_dict)
    return stock_date


def create_json():
    pass


def write_json():
    pass


if __name__ == '__main__':
    # print(*parser(), sep='\n')
    print(*link_parser(), sep='\n')
    # print(dollar_value())
