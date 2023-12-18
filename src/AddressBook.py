from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from info import *
import os


class AddressBook(UserList):
    def __init__(self):
        self.data = []
        self.counter = -1

    def __str__(self):
        result = []
        for contact in self.data:
            if contact['birthday']:
                birth = contact['birthday'].strftime("%d/%m/%Y")
            else:
                birth = ''
            if contact['phones']:
                new_value = []
                for phone in contact['phones']:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append(
                "_" * 50 + "\n" + f"Name: {contact['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {contact['email']} \nStatus: {contact['status']} \nNote: {contact['note']}\n" + "_" * 50 + '\n')
        return '\n'.join(result)

    def __next__(self):
        phones = []
        self.counter += 1
        if self.data[self.counter]['birthday']:
            birth = self.data[self.counter]['birthday'].strftime("%d/%m/%Y")
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]['phones']:
            if number:
                phones.append(number)
        result = "_" * 50 + "\n" + f"Name: {self.data[self.counter]['name']} \nPhones: {', '.join(phones)} \nBirthday: {birth} \nEmail: {self.data[self.counter]['email']} \nStatus: {self.data[self.counter]['status']} \nNote: {self.data[self.counter]['note']}\n" + "_" * 50
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
        contact = {'name': record.name,
                   'phones': record.phones,
                   'birthday': record.birthday,
                   'email': record.email,
                   'status': record.status,
                   'note': record.note}
        self.data.append(contact)
        self.log(f"Contact {record.name} has been added.")

    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)
        self.log("Addressbook has been saved!")

    def load(self, file_name):
        emptyness = os.stat(file_name + '.bin')
        if emptyness.st_size != 0:
            with open(file_name + '.bin', 'rb') as file:
                self.data = pickle.load(file)
            self.log("Addressbook has been loaded!")
        else:
            self.log('Adressbook has been created!')
        return self.data

#Шукає контакти за зразком та групою.
    def search(self, sample, group):
        result = []
        group_new = group.strip().lower().replace(' ', '')
        sample_new = sample.strip().lower().replace(' ', '')

        for contact in self.data:
            if group_new == 'phones':

                for phone in contact['phones']:

                    if phone.lower().startswith(sample_new):
                        result.append(contact)
            elif contact[group_new].lower().replace(' ', '').startswith(sample_new):
                result.append(contact)
        if not result:
            print('There is no such contact in address book!')
        return result

#Редагує вказані параметри контакту.
    def edit(self, contact_name, param, new_value):
        names = []
        try:
            for contact in self.data:
                names.append(contact['name'])
                if contact['name'] == contact_name:
                    if param == 'birthday':
                        new_value = Birthday(new_value).value
                    elif param == 'email':
                        new_value = Email(new_value).value
                    elif param == 'status':
                        new_value = Status(new_value).value
                    elif param == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                            new_value.append(Phone(number).value)
                    if parameter in contact.keys():
                        contact[parameter] = new_value
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

#Видаляє контакт за вказаним ім'ям.
    def remove(self, sample):
        flag = False
        for contact in self.data:
            if contact['name'] == sample:
                self.data.remove(contact)
                self.log(f"Contact {contact['name']} has been removed!")
                flag = True
            '''if sample in contact['phones']:
                        contact['phones'].remove(sample)
                        self.log.log(f"Phone number of {contact['name']} has been removed!")'''
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
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        for contact in self.data:
            if contact['birthday']:
                new_birthday = contact['birthday'].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(contact['name'])
                    else:
                        congratulate['Monday'].append(contact['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50

