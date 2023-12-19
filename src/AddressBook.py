from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from validate import *
import os


class AddressBook(UserList):
    def __init__(self):
        self.data = []
        self.counter = -1

    def __str__(self):
        # Ініціалізувати порожній список для зберігання відформатованої інформації про обліковий запис
        result = []

        # Перебір кожного акаунта в даних
        for account in self.data:
            # Форматуємо день народження або встановлюємо його в порожній рядок, якщо він не існує
            birth = account['birthday'].strftime(
                "%d.%m.%Y") if account['birthday'] else ''

            # Відформатуємо телефони, відфільтрувавши значення None
            phones = ', '.join(filter(None, account['phones']))

            # Додаємо відформатовану інформацію про акаунт до списку результатів
            result.append("~" * 52 + f"\nName: {account['name']} \nCountry: {account['country']} \nPhones: {phones} \nBirthday: {birth} \n"
                          f"Email: {account['email']} \nNote: {account['note']}\n" + "~" * 52 + '\n')

        # Об'єднати відформатовану інформацію про акаунт в один рядок і повернути
        return '\n'.join(result)

    def __next__(self):
        # Збільшити лічильник для переходу на наступний рахунок
        self.counter += 1

        # Скидаємо лічильник на -1 і викликаємо StopIteration, якщо пройдено всі акаунти
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration

        # Отримати поточний рахунок
        account = self.data[self.counter]
        # Відформатуємо день народження або встановимо його в порожній рядок, якщо він не існує
        birth = account['birthday'].strftime(
            "%d.%m.%Y") if account['birthday'] else ''
        # Відформатуємо телефони, відфільтрувавши значення None
        phones = ', '.join(filter(None, account['phones']))

        # Згенерувати відформатований рядок, що представляє поточний рахунок
        result = "~" * 52 + f"\nName: {account['name']} \nCountry: {account['country']} \nPhones: {phones} \nBirthday: {birth} \n" \
            f"Email: {account['email']} \nNote: {account['note']}\n" + "~" * 52

        # Повернути відформатований рядок
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = {'name': record.name,
                            'phones': record.phones,
                            'birthday': record.birthday}

    def __getitem__(self, index):
        return self.data[index]

    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def add(self, record):
        account = {'name': record.name,
                   'country': record.country,
                   'phones': record.phones,
                   'birthday': record.birthday,
                   'email': record.email,
                   'note': record.note}
        self.data.append(account)
        self.log(f"Contact {record.name} has been added.")

    def save(self, file):
        # зберігає дані адресної книги у бінарний файл за вказаним ім'ям
        with open(file + '.bin', 'wb') as f:
            pickle.dump(self.data, f)
        self.log("Addressbook has been saved!")

    # завантажує дані адресної книги з бінарного файлу
    def load_pickle(self, file):
        try:
            with open(file + '.bin', 'wb') as f:
                self.data = pickle.load(f)
            self.log('Addressbook has been loaded')
        except FileNotFoundError:
            # виникає, якщо файл для адресної книги не знайдено
            self.log("Addressbook file not found. Creating a new one")
        except pickle.UnpicklingError:
            # виникає, якщо сталася помилка під час десеріалізації даних
            self.log("Error unplicking data. Creating a new address book")
        return self.data

# Шукає контакти за зразком та групою.
    def search(self, sample, group):
        result = []
        group_new = group.strip().lower().replace(' ', '')
        sample_new = sample.strip().lower().replace(' ', '')

        for account in self.data:
            if group_new == 'phones':
                for phone in account['phones']:
                    if phone.lower().startswith(sample_new):
                        result.append(account)
            elif account[group_new].lower().replace(' ', '').startswith(sample_new):
                result.append(account)
        if not result:
            print('There is no such contact in address book!')
        return result

# Редагує вказані параметри контакту.
    def edit(self, contact_name, param, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if param == 'birthday':
                        new_value = Birthday(new_value).value
                    elif param == 'email':
                        new_value = Email(new_value).value
                    elif param == 'status':
                        new_value = Country(new_value).value
                    elif param == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                            new_value.append(Phone(number).value)
                    if param in account.keys():
                        account[param] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        else:
            self.log(f"Contact {contact_name} has been edited!")
            return True
        return False

# Видаляє контакт за вказаним ім'ям.
    def remove(self, sample):
        flag = False
        for account in self.data:
            if account['name'] == sample:
                self.data.remove(account)
                self.log(f"Contact {account['name']} has been removed!")
                flag = True
            '''if sample in contact['phones']:
                        account['phones'].remove(sample)
                        self.log.log(f"Phone number of {account['name']} has been removed!")'''
        return flag

    def __get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        # Отримати словник привітань методом __get_congratulations
        result = [
            f"{weekday}: {' '.join(accounts)}"
            for weekday, accounts in self.__get_congratulations().items() if accounts
        ]
        # Відформатуйте та поверніть результат
        return '~' * 52 + '\n' + '\n'.join(result) + '\n' + '~' * 52

    def __get_congratulations(self):
        # Визначте дні тижня та отримайте поточний рік
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year

        # Ініціалізувати порожній словник для зберігання привітальних повідомлень
        congratulate = {weekday: [] for weekday in WEEKDAYS[:5]}

        # Ітерація над кожним обліковим записом у даних
        for account in self.data:
            if account['birthday']:
                # Пристосуйте дату народження до поточного року
                new_birthday = account['birthday'].replace(year=current_year)

                # Перевірте, чи скоригований день народження знаходиться на поточному тижні
                if self.__is_birthday_in_current_week(new_birthday):
                    # Визначте день тижня та додайте назву до відповідного списку
                    weekday = WEEKDAYS[new_birthday.weekday(
                    )] if new_birthday.weekday() < 5 else 'Monday'
                    congratulate[weekday].append(account['name'])

        # Повернути словник з вітальними повідомленнями
        return congratulate

    def __is_birthday_in_current_week(self, birthday):
        # Отримати дати початку та закінчення поточного тижня
        current_week_start = self.__get_current_week()[0]
        current_week_end = self.__get_current_week()[1]

        # Перевірте, чи є день народження на поточному тижні
        return current_week_start <= birthday.date() < current_week_end
