from bs4 import BeautifulSoup
import requests
import json


# Парсер ссылок каждой акции
def link_parser():
    page = requests.get("https://markets.businessinsider.com/index/components/s&p_500")
    soup = BeautifulSoup(page.text, "lxml")
    table = soup.find("tbody", "table__tbody")
    links = [f'https://markets.businessinsider.com{i.get("href")}' for i in table.find_all("a")]
    return links


def parser():
    links = link_parser()
    stock_date = []
    for stock_link in links:
        page = requests.get(stock_link)
        soup = BeautifulSoup(page.text, "lxml")
        stock_dict = dict()
        stock_dict["code"] = soup.find("span", "price-section__category").text.strip().split(" , ")[-1]
        stock_dict["name"] = soup.find("span", "price-section__label").text
        stock_dict["price"] = float(soup.find("span", "price-section__current-value").text)
        stock_dict["P/E"] = float(soup.find("div", "snapshot__data-item padding-right--zero").text.split()[0])
        stock_dict["growth"] = None
        stock_dict["potential profit"] = float(soup.find("div", "snapshot__data-item snapshot__data-item--small snapshot__data-item--right").text.split()[0]) - float(soup.find("div", "snapshot__data-item snapshot__data-item--small").text.split()[0])
        print(stock_dict)
        print(soup.find_all("div", "snapshot__data-item snapshot__data-item--small snapshot__data-item--right").text)
        print(soup.find_all("div", "snapshot__data-item snapshot__data-item--small").text)
        return None

def create_json():
    pass


def write_json():
    pass


if __name__ == '__main__':
    parser()
