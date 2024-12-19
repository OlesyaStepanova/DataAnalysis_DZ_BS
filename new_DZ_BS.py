import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def getFlats(page):
    flats = []
    url = f'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={page}&region=1&room2=1'
    response = requests.get(url) #получаем ответ от сайта
    if response.status_code != 200:
        print(f"Ошибка при получении страницы {page}: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "lxml")

    for data in soup.find_all("div", attrs={"data-testid" : "offer-card"}):
        data2 = data.find("div", attrs={"data-name": "GeneralInfoSectionRowComponent"})
        link = data2.find("a")
        link = link['href']
        name = data2.find("span", attrs={"data-mark": "OfferTitle"})
        name = name.find("span")
        if name:
            name = name.text
        else:
            name = "Информация отсутствует"
        # data2 = data.find('a', href=lambda href: href and href.startswith('https://www.cian.ru/sale/flat/'))
        # link = data2['href']
        # name = data2.find("span", class_= "").text
        name2 = data2.find("span", attrs={"data-mark": "OfferSubtitle"})
        if name2:
            name2 = name2.text
        else:
            name2 = "Информация отсутствует"

        geo = data.find("div", attrs={"data-name" : "SpecialGeo"})
        if geo:
            geo = geo
            metro = geo.find('a', href=lambda href: href and href.startswith('https://www.cian.ru/'))
            if metro:
                metro = metro.text
            else:
                metro = "Информация отсутствует"
            how_to_go = geo.find('div', class_=lambda x: x and 'remoteness' in x)
            if how_to_go:
                how_to_go = how_to_go.text
            else:
                how_to_go = "Информация отсутствует"
        else:
            metro = "Информация отсутствует"
            how_to_go = "Информация отсутствует"

        address = data.find('div', class_=lambda x: x and 'labels' in x)
        if address:
            address = address.text
        else:
            address = "Информация отсутствует"

        price = data.find("span", attrs={"data-mark" : "MainPrice"})
        if price:
            price = price.text
        else:
            price = "Информация отсутствует"
        price_per_metr = data.find("p", attrs={"data-mark" : "PriceInfo"})
        if price_per_metr:
            price_per_metr = price_per_metr.text
        else:
            price_per_metr = "Информация отсутствует"

        flats.append(
            {"Ссылка": link, "Название": name, "Описание": name2,
             "Метро": metro, "Дальность от метро": how_to_go, "Адрес": address,
             "Стоимость": price, "Стоимость за метр": price_per_metr})
        time.sleep(1) #Чтобы сайт не блокировал запросы

    return flats


def main():
    all_flats = []
    pages_to_fetch = 25
    for page in range(1, pages_to_fetch + 1):
        print(f"Сбор предложений со страницы {page}...")
        flat = getFlats(page)
        all_flats.extend(flat)
    df = pd.DataFrame(all_flats) #сохраняем в файл
    df.to_csv('flats5.csv', index=False, encoding='utf-8')
print(f"Собрано предложений. Данные сохранены в файл flats.csv.")
if __name__ == '__main__':
    main()


    # print(data.prettify())
