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


def parser() -> list:
    links = link_parser()
    dollar = dollar_value()
    stock_date = []
    for stock_link in links:
        try:
            page = requests.get(stock_link)
            soup = BeautifulSoup(page.text, "lxml")
            stock_dict = dict()
            stock_dict["code"] = soup.find("span", "price-section__category").text.strip().split(" , ")[-1]
            stock_dict["name"] = soup.find("span", "price-section__label").text
            stock_dict["price"] = round(float(soup.find("span", "price-section__current-value").text.replace(',', '')) * dollar, 2)
            stock_dict["P/E"] = float(soup.find("div", "snapshot__data-item padding-right--zero").text.split()[0].replace(',', ''))
            week_lower = float(soup.find("div", "snapshot__data-item snapshot__data-item--small").text.split()[0].replace(',', ''))
            week_higher = float(soup.find("div", "snapshot__data-item snapshot__data-item--small snapshot__data-item--right").text.split()[0].replace(',', ''))
            stock_dict["potential profit"] = round(((week_higher - week_lower) / week_lower) * 100, 2)
            stock_date.append(stock_dict)
        except AttributeError:
            print(f"Ошибка с: {stock_link}")
    return stock_date


def most_expensive(stocks: list) -> list:
    return sorted(stocks, key=lambda x: x['price'], reverse=True)[:10]


def lowest_pe(stocks: list) -> list:
    return sorted(stocks, key=lambda x: x['P/E'])[:10]


def best_growth(stocks: list) -> list:
    return sorted(stocks, key=lambda x: x['potential profit'], reverse=True)[:10]


def create_json(stock: list) -> None:
    with open("most_expensive.json", "w") as file:
        json.dump(most_expensive(stock), file, indent=4)
    with open("lowest_pe.json", "w") as file:
        json.dump(lowest_pe(stock), file, indent=4)
    with open("best_growth.json", "w") as file:
        json.dump(best_growth(stock), file, indent=4)



if __name__ == '__main__':
    # print(*most_expensive(temp), sep='\n')
    # print(*lowest_pe(temp), sep='\n')
    # print(*best_growth(temp), sep='\n')

    # print(*parser(), sep='\n')
    # print(*link_parser(), sep='\n')
    # print(dollar_value())

    stock_date = parser()
    create_json(stock_date)
