import json
import os
import re
import time
from sys import platform
from random import randint

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class Parsing:
    def __init__(self):
        self.num = 0
        self.data_car = []

        if platform == 'win32':
            self.path = f'{os.getcwd()}\\geckodriver.exe'
        else:
            self.path = f'{os.getcwd()}/geckodriver.exe'

        self.list_error = []

    def start_brawser(self, headless=True):
        '''
        Запуск браузера

        :param headless: bool -- наличие графического инерфейса (True - без графического интерфейса)'''
        self.options = FirefoxOptions()
        self.options.headless = headless
        self.browser = webdriver.Firefox(options=self.options)

    def __print_error(self, name: str, url: str):
        '''
        Вывод ошибок

        :param num_page: int -- номер страницы
        '''
        print(f'[Error] {name} = None')
        print(f'url: {url}')
        self.list_error.append(f'Error {name}: {url}')

    def car_info(self, url):
        '''
        Сбор информации об авто

        :param url: str -- URL страницы
        '''

        self.list_error.clear()

        while True:
            try:
                self.browser.get(url)
            except:
                with open(f"links_car_error.txt", "a", encoding="utf-8") as file:
                    file.write(url + '\n')
            else:
                break
        try:
            soup = bs(self.browser.page_source, "lxml")
        except:
            with open(f"error_load.txt", "a", encoding="utf-8") as file:
                file.write(url + '\n')
        else:

            description = []
            image = []

            try:
                body_type = soup.find('li', class_='CardInfoRow CardInfoRow_bodytype').find('a').text.strip()
            except:
                body_type = None
                self.__print_error(name='body_type', url=url)

            try:
                brand = url.split('/')[6].strip()
            except:
                brand = None
                self.__print_error(name='brand', url=url)

            try:
                color = soup.find('li', class_='CardInfoRow CardInfoRow_color').find('a').text.strip()
            except:
                color = None
                self.__print_error(name='color', url=url)

            try:
                complectation_dict = soup.find('script', id='initial-state').text
                complectation_dict = re.findall(r'"equipmentGroups":\[{.*?\]}\]}', complectation_dict)
            except:
                complectation_dict = None
                self.__print_error(name='complectation_dict', url=url)

            try:
                description_span = soup.find('div', class_='CardDescription__textInner CardDescription__textInner_cut') \
                    .find_all('span')
                for item in description_span:
                    description.append(item.text.strip())
                description_li = soup.find('div', class_='CardDescription__textInner CardDescription__textInner_cut') \
                    .find_all('li')
                for item in description_li:
                    description.append(item.text.strip())
                description = "\n".join(description)
            except:
                try:
                    description_span = soup.find('div', class_='CardDescription CardOfferBody__contentIsland') \
                        .find_all('span')
                    for item in description_span:
                        description.append(item.text.strip())
                    description_li = soup.find('div', class_='CardDescription CardOfferBody__contentIsland') \
                        .find_all('li')
                    for item in description_li:
                        description.append(item.text.strip())
                    description = "\n".join(description)
                except:
                    try:
                        description_span = soup.find('div', class_='CardDescription__textInner') \
                            .find_all('span')
                        for item in description_span:
                            description.append(item.text.strip())
                        description_li = soup.find('div', class_='CardDescription__textInner') \
                            .find_all('li')
                        for item in description_li:
                            description.append(item.text.strip())
                        description = "\n".join(description)
                    except:
                        description = None
                        self.__print_error(name='description', url=url)

            try:
                fuel_type = soup.find('li', class_='CardInfoRow CardInfoRow_engine') \
                    .find('a', class_='Link Link_color_black').text.strip()
            except:
                try:
                    fuel_type = soup.find('li', class_='CardInfoRow CardInfoRow_engine') \
                        .find('a', class_='CardInfoRow__cell').text.strip()
                except:
                    fuel_type = None
                    self.__print_error(name='fuel_type', url=url)

            try:
                engine_displacement = soup.find('li', class_='CardInfoRow CardInfoRow_engine').find('div').text
                engine_displacement = re.sub(r'\xa0', ' ', engine_displacement)
                engine_displacement = re.sub(fuel_type, '', engine_displacement).strip()
            except:
                engine_displacement = None
                self.__print_error(name='engine_displacement', url=url)

            try:
                engine_power = soup.find('script', id='initial-state').text
                engine_power = str(re.findall(r'"power":.*?,', engine_power))[10:-3:]
            except:
                engine_power = None
                self.__print_error(name='engine_power', url=url)

            try:
                equipment_dict = soup.find('script', id='initial-state').text
                equipment_dict = re.findall(r'"equipment":{.*?}', equipment_dict)
            except:
                equipment_dict = None
                self.__print_error(name='equipment_dict', url=url)

            try:
                tmp = soup.find('div', class_='ImageGalleryDesktop__image-container').find_all('img')
                for i in tmp:
                    image.append('https:' + str(re.findall(r'"//.*?"/', str(i)))[3:-5])
            except:
                image = None
                self.__print_error(name='image', url=url)

            try:
                mileage = soup.find('li', class_='CardInfoRow CardInfoRow_kmAge').find_all('span')[1].text
                mileage = re.sub(r'\xa0', '', mileage)
                mileage = re.sub(r'км', '', mileage)
            except:
                mileage = None
                self.__print_error(name='mileage', url=url)

            try:
                model_date = soup.find('li', class_='CardInfoRow CardInfoRow_year').find_all('span')[1].text
            except:
                model_date = None
                self.__print_error(name='model_date', url=url)

            try:
                model_info = soup.find('script', id='initial-state').text
                model_info = str(re.findall(r'"mark_info":.*?:{', model_info))[15:-4:]
            except:
                model_info = None
                self.__print_error(name='model_info', url=url)

            try:
                model_name = soup.find('h1', class_='CardHead__title').text
            except:
                model_name = None
                self.__print_error(name='model_name', url=url)

            try:
                name = soup.find('div', class_='CardBreadcrumbs') \
                           .find_all('a', class_='Link Link_color_gray CardBreadcrumbs__itemText')[-1].text
            except:
                name = None
                self.__print_error(name='name', url=url)

            try:
                number_of_doors = soup.find('script', id='initial-state').text
                number_of_doors = str(re.findall(r'"doors_count":.*?,', number_of_doors))[16:-3:]
            except:
                number_of_doors = None
                self.__print_error(name='number_of_doors', url=url)

            try:
                price_currency = soup.find(id='ruble').get('id')
            except:
                price_currency = 'other'
                print(f'\033[31mprice_currency = other???\033[0m')
                self.list_error.append(f'Error price_currency: {url}')

            try:
                production_date = soup.find('script', type='application/ld+json').text
                production_date = str(re.findall(r'"productionDate":.*?,', production_date))[19:-3:]
            except:
                production_date = None
                self.__print_error(name='production_date', url=url)

            try:
                sell_id = soup.find('script', id='initial-state').text
                sell_id = str(re.findall(r'"sale_id".*?,', sell_id)[0]).strip()[:-1]
            except:
                sell_id = None
                self.__print_error(name='sell_id', url=url)

            try:
                super_gen = soup.find('script', id='initial-state').text
                super_gen = str(re.findall(r'"super_gen":{.*?}', super_gen)[0]).strip()[12::]
            except:
                super_gen = None
                self.__print_error(name='super_gen', url=url)

            try:
                vehicle_configuration = soup.find('script', type='text/javascript').text
                vehicle_configuration = str(re.findall(r'"transmission":.*?,', vehicle_configuration))[18:-4]
            except:
                vehicle_configuration = None
                self.__print_error(name='vehicle_configuration', url=url)

            try:
                vendor = soup.find('script', id='initial-state').text.strip()
                vendor = str(re.findall(r'"vendor".*?,', vendor)[0]).strip()[10:-2:]
            except:
                vendor = None
                self.__print_error(name='vendor', url=url)

            try:
                owners = soup.find('li', class_='CardInfoRow CardInfoRow_ownersCount') \
                    .find_all('span', class_='CardInfoRow__cell')[1].text.strip()
            except:
                owners = None
                self.__print_error(name='owners', url=url)

            try:
                pts = soup.find('li', class_='CardInfoRow CardInfoRow_pts') \
                    .find_all('span', class_='CardInfoRow__cell')[1].text.strip()
            except:
                pts = None
                self.__print_error(name='pts', url=url)

            try:
                wheel = soup.find('li', class_='CardInfoRow CardInfoRow_wheel') \
                    .find_all('span', class_='CardInfoRow__cell')[1].text.strip()
            except:
                wheel = None
                self.__print_error(name='wheel', url=url)

            try:
                state_car = soup.find('li', class_='CardInfoRow CardInfoRow_state') \
                    .find_all('span', class_='CardInfoRow__cell')[1].text
            except:
                state_car = None
                self.__print_error(name='state_car', url=url)

            try:
                drive_car = soup.find('li', class_='CardInfoRow CardInfoRow_drive') \
                    .find_all('span', class_='CardInfoRow__cell')[1].text
            except:
                drive_car = None
                self.__print_error(name='row_drive', url=url)

            try:
                customs = soup.find('li', class_='CardInfoRow CardInfoRow_customs') \
                    .find_all('span', class_='CardInfoRow__cell')[1].text
            except:
                customs = None
                self.__print_error(name='customs', url=url)

            try:
                price = soup.find('span', class_='OfferPriceCaption__price').text
            except:
                price = None
                self.__print_error(name='price', url=url)

            try:
                price2 = soup.find('script', type='application/ld+json').text
                price2 = str(re.findall(r'"price":.*?,', price2)[0]).strip()[8:-1:]
            except:
                price2 = None
                self.__print_error(name='price2', url=url)

            try:
                vehicle_transmission = soup.find('li', class_='CardInfoRow CardInfoRow_transmission') \
                                          .find_all('span', class_='CardInfoRow__cell')[1].text.strip()
            except:
                vehicle_transmission = None
                self.__print_error(name='vehicle_transmission', url=url)

            if body_type == brand == url == color == complectation_dict == description == fuel_type:
                self.list_error = [f'Ошибка чтения: {url}']
                with open(f"load_error.txt", "a", encoding="utf-8") as file:
                    file.write(url + '\n')

            else:
                self.data_car.append(
                    {
                        'bodyType': body_type,
                        'brand': brand,
                        'car_url': url,
                        'color': color,
                        'complectation_dict': complectation_dict,
                        'description': description,
                        'engineDisplacement': engine_displacement,
                        'enginePower': engine_power,
                        'equipment_dict': equipment_dict,
                        'fuelType': fuel_type,
                        'image': image,
                        'mileage': mileage,
                        'modelDate': model_date,
                        'model_info': model_info,
                        'model_name': model_name,
                        'name': name,
                        'numberOfDoors': number_of_doors,
                        'parsing_unixtime': int(time.time()),
                        'priceCurrency': price_currency,
                        'productionDate': production_date,
                        'sell_id': sell_id,
                        'super_gen': super_gen,
                        'vehicleConfiguration': vehicle_configuration,
                        'vehicleTransmission': vehicle_transmission,
                        'vendor': vendor,
                        'Владельцы': owners,
                        'ПТС': pts,
                        'Руль': wheel,
                        'Привод': drive_car,
                        'Таможня': customs,
                        'Состояние': state_car,
                        'Стоимость': price,
                        'Стоимость второй источник': price2
                    }
                )

            with open(f"error.txt", "a", encoding="utf-8") as file:
                for row in self.list_error:
                    file.write(row + '\n')
                self.list_error.clear()

            self.num += 1
            print(f'Обработанно ссылок на машины {self.num}')

def main():
    try:
        print('Загружаем фаил car_links.txt')
        with open('car_links.txt', 'r') as f:
            list_links = f.read().splitlines()
    except:
        print('Проверте файл car_links.txt')
    else:
        parser = Parsing()
        parser.start_brawser(headless=True)
        print(f'Начинаем обработку ссыдок')

        for url in list_links:
            parser.car_info(url)
            time.sleep(0.1 * randint(10, 15))

        with open(f"data.json", "a", encoding="utf-8") as file:
            json.dump(parser.data_car, file, indent=4, ensure_ascii=False)

        parser.browser.close()
        parser.browser.quit()

        print('Работа парсера успешно завершена')


if __name__ == '__main__':
    main()
