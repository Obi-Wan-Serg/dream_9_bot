from datetime import date, datetime
import re
from abc import ABC, abstractmethod


class Record:

    def __init__(self, name, country='', phones='', birthday='', email='', note=''):

        self.birthday = birthday
        self.name = name
        self.phones = phones
        self.email = email
        self.country = country
        self.note = note

    def days_to_birthday(self):
        current_datetime = datetime.now()
        self.birthday = self.birthday.replace(year=current_datetime.year)
        if self.birthday >= current_datetime:
            result = self.birthday - current_datetime
        else:
            self.birthday = self.birthday.replace(
                year=current_datetime.year + 1)
            result = self.birthday - current_datetime
        return result.days


class Field(ABC):

    @abstractmethod
    def __getitem__(self):
        pass


class Name(Field):

    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class CountryError(Exception):
    pass


class Country(Field):

    def __init__(self, value=''):
        while True:
            self.countries = {
                'Albania': '+355',
                'Andorra': '+376',
                'Austria': '+43',
                'Belarus': '+375',
                'Belgium': '+32',
                'Bosnia and Herzegovina': '+387',
                'Bulgaria': '+359',
                'Croatia': '+385',
                'Cyprus': '+357',
                'Czech Republic': '+420',
                'Denmark': '+45',
                'Estonia': '+372',
                'Faroe Islands': '+298',
                'Finland': '+358',
                'France': '+33',
                'Germany': '+49',
                'Gibraltar': '+350',
                'Greece': '+30',
                'Guernsey': '+44',
                'Hungary': '+36',
                'Iceland': '+354',
                'Ireland': '+353',
                'Isle of Man': '+44',
                'Italy': '+39',
                'Jersey': '+44',
                'Latvia': '+371',
                'Liechtenstein': '+423',
                'Lithuania': '+370',
                'Luxembourg': '+352',
                'Macedonia': '+389',
                'Malta': '+356',
                'Moldova': '+373',
                'Monaco': '+377',
                'Montenegro': '+382',
                'Netherlands': '+31',
                'Norway': '+47',
                'Poland': '+48',
                'Portugal': '+351',
                'Romania': '+40',
                'San Marino': '+378',
                'Serbia': '+381',
                'Slovakia': '+421',
                'Slovenia': '+386',
                'Spain': '+34',
                'Sweden': '+46',
                'Switzerland': '+41',
                'Ukraine': '+380',
                'United Kingdom': '+44',
            }
            if value:
                self.value = value
            else:
                self.value = input('Citizenship: ')
            # валідація введеної країни по наявності в словнику
            try:
                if self.value.lower() == 'russia':
                    raise CountryError
                elif self.value.capitalize() in self.countries:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Please try another country.')
            except CountryError:
                print('Fortunately, there is no such country')

    def __getitem__(self):
        return self.value


class Phone(Field):

    def __init__(self, value=''):
        while True:
            self.value = []
            if value:
                self.values = value
            else:
                self.values = input(
                    "Please enter your phone number as ten digits (for other phones, add spaces between numbers): ")
            # перевірка на правильність введенного телефонного номеру
            try:
                for number in self.values.split(' '):
                    if re.match(r'^\d{10}$', number) or number == '':
                        self.value.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print(
                    'Please input the phone number in the correct format; it must consist of 10 digits.')
            else:
                break

    def __getitem__(self):
        return self.value


class Birthday(Field):

    def __init__(self, value=''):
        while True:
            today = date.today()
            if value:
                input_value = value
            else:
                input_value = input("Birthday date(dd.mm.YYYY): ")
            try:
                # перевірка правильності введення дати народження
                if re.fullmatch(r'^\d{1,2}\.\d{1,2}\.\d{4}$', input_value):
                    birthday_date = datetime.strptime(
                        input_value.strip(), '%d.%m.%Y').date()
                    # перевірка чи не є дата народження в майбутньому
                    if birthday_date > today:
                        raise ValueError
                    self.value = birthday_date
                    break
                elif input_value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print(
                    'The Birthday date must be entered in format: day.month.YEAR. The Birthday date cannot be in the future!')

    def __getitem__(self):
        return self.value


class Email(Field):

    def __init__(self, value=''):
        while True:

            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                # перевірка правильності введення електронної адреси
                if re.match(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Please enter your email address in the correct format.')

    def __getitem__(self):
        return self.value


class Note(Field):

    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value
