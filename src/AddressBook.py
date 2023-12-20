from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from .validate import *
import os


class AddressBook(UserList):
    def __init__(self):
        self.data = []
        self.counter = -1

    def __str__(self):
        result = []
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime('%d.%m.%Y')
            else:
                birth = ''
            if account['phones']:
                new_value = []
                for phone in account['phones']:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append(
                "_" * 50 + "\n" + f"Name: {account['name']} \nCountry: {account['country']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nNote: {account['note']}\n" + "_" * 50 + '\n')
        return '\n'.join(result)

    def __next__(self):
        phones = []
        self.counter += 1
        if self.data[self.counter]['birthday']:
            birth = self.data[self.counter]['birthday'].strftime('%d.%m.%Y')
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]['phones']:
            if number:
                phones.append(number)
        result = "_" * 50 + "\n" + (f"Name: {self.data[self.counter]['name']} "
                                    f"\nCountry: {self.data[self.counter]['country']} "
                                    f"\nPhones: {', '.join(phones)} \nBirthday: {birth} "
                                    f"\nEmail: {self.data[self.counter]['email']} "
                                    f"\nNote: {self.data[self.counter]['note']}\n") + "_" * 50
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
        log_path = os.path.join('src', 'logs.txt')
        with open(log_path, 'a') as file:
            file.write(f'{message}\n')

    def add(self, record):
        account = {'name': record.name,
                   'country': record.country,
                   'phones': record.phones,
                   'birthday': record.birthday,
                   'email': record.email,
                   'note': record.note,
                   'tags': record.tags}  # Додати теги до запису
        self.data.append(account)
        self.log(f"Contact {record.name} has been added.")

    def save(self, file_name):
        file_path = os.path.join('src', file_name + '.bin')
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)
        self.log("Книгу контактів збережено!")

    def load(self, file_name):
        file_path = os.path.join('src', file_name + '.bin')
        emptyness = os.stat(file_path)
        if emptyness.st_size != 0:
            with open(file_path, 'rb') as file:
                self.data = pickle.load(file)
            self.log("Книгу контактів завантажено!")
        else:
            self.log('Книгу контактів створено!')
        return self.data

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for account in self.data:
            if category_new == 'phones':
                for phone in account['phones']:
                    if phone.lower().replace(' ', '').startswith(pattern_new):
                        result.append(account)
                        break
            elif category_new == 'tags':
                for tag in account.get('tags', []):
                    if tag.lower().replace(' ', '') == pattern_new:
                        result.append(account)
                        break
            else:
                if account.get(category_new, '').lower().replace(' ', '') == pattern_new:
                    result.append(account)

        if not result:
            print(f'There is no such contact in address book with {category}: {pattern}!')
        return result

    def edit(self, contact_name, parameter, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    elif parameter == 'country':
                        new_value = Country(new_value).value
                    elif parameter == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                            new_value.extend(Phone(number).value)
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print('Невірний параметр! Спробуйте знову.')
        except NameError:
            print('Такого контакту не знайдено!')
        else:
            self.log(f"Контакт {contact_name} відредаговано!")
            return True
        return False

    def remove(self, pattern):
        flag = False
        for account in self.data:
            if account['name'] == pattern:
                self.data.remove(account)
                self.log(f"Контакт {account['name']} видалено!")
                flag = True
            '''if pattern in account['phones']:
                        account['phones'].remove(pattern)
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
        result = []
        WEEKDAYS = ['Понеділок', 'Вівторок', 'Середа',
                    'Четвер', "П'ятниця", 'Субота', 'Неділя']
        current_year = dt.now().year
        congratulate = {'Понеділок': [], 'Вівторок': [],
                        'Середа': [], 'Четвер': [], "П'ятниця": []}
        for account in self.data:
            if account['birthday']:
                new_birthday = account['birthday'].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(
                            account['name'])
                    else:
                        congratulate['Понеділок'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50

    def search_by_tags(self, pattern):
        results = []
        for record in self.data:
            if any ( tag.lower ( ) == pattern.lower ( ) for tag in record.get ( 'tags', [] ) ):
                results.append ( record )

        return results
