import os
import csv


class PriceMachine():
    product = []

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='price'):
        '''
                    Сканирует указанный каталог. Ищет файлы со словом price в названии.
                    В файле ищет столбцы с названием товара, ценой и весом.
                    Допустимые названия для столбца с товаром:
                        товар
                        название
                        наименование
                        продукт

                    Допустимые названия для столбца с ценой:
                        розница
                        цена

                    Допустимые названия для столбца с весом (в кг.)
                        вес
                        масса
                        фасовка
                '''
        for file in os.listdir(file_path):

            k = file
            if 'price' in file:
                with open(f'price/{file}', 'r', encoding='utf8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        product, price, weight = self.search_product_price_weight(row.keys())
                        if all(len(p)!=0 for p in (product, price, weight)):
                            product_name = row[product[0]]
                            price = row[price[0]]
                            weight = row[weight[0]]
                            price_per_kg = int(price) / int(weight) if int(weight) else 0  # Цена за кг
                            self.data.append((k, product_name, price, weight, price_per_kg))

    def search_product_price_weight(self, headers):
        '''
                    Возвращает названия столбцов
        '''
        product_options = ['товар', 'название', 'наименование', 'продукт']
        price_options = ['розница', 'цена']
        weight_options = ['вес', 'масса', 'фасовка']
        product_col = [header for header in headers if header.lower() in product_options]
        price_col = [header for header in headers if header.lower() in price_options]
        weight_col = [header for header in headers if header.lower() in weight_options]
        return product_col, price_col, weight_col

    def export_to_html(self, fname='output.html'):
        '''
        Экспорт файлов в html файл
        '''
        # Сортировка данных по `price_per_kg` от наименьшего к наибольшему
        self.data.sort(key=lambda x: x[4])  # x[4] - это price_per_kg
        # Генерация HTML-таблицы
        result = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Позиции продуктов</title>
            </head>
            <body>
                <table border="1" style="border-collapse: collapse;">
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Масса</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>'''
        for number, item in enumerate(self.data):
            file_name, product_name, price, weight, price_per_kg = item
            result += f'<tr>'
            result += f'<td>{number + 1}</td>'
            result += f'<td>{product_name}</td>'
            result += f'<td>{price}</td>'
            result += f'<td>{weight}</td>'
            result += f'<td>{file_name}</td>'
            result += f'<td>{price_per_kg:.2f}</td>'
            result += f'</tr>'
        result += '''
                </table>
            </body>
            </html>'''
        with open(fname, 'w', encoding='windows-1251') as f:
            f.write(result)
        print(f'HTML-файл {fname} успешно создан!')

    def find_text(self, name):
        '''
        Поиск товара по названию
        '''
        self.data.sort(key=lambda x: x[4])
        print('_________________________________________________________________')
        print("| Номер | Название  |Цена |Масса  |    Файл   | Цена за кг|")
        k = 1
        for number, item in enumerate(self.data):
            file_name, product_name, price, weight, price_per_kg = item
            if name.lower() in product_name.lower():
                print('|', k, '  |', product_name, '|', price, '|', weight, '   |', file_name, '|',
                      round(price_per_kg, 2), '|')
                k += 1


pm = PriceMachine()
pm.load_prices()
pm.export_to_html()
while (1 != 0):
    name = input('Введите слова для поиска:')
    pm.find_text(name)
    print('Если хотите выйти из поиска наберите "exit"')
    if name == 'exit':
        print('Работа закончена')
        exit()
