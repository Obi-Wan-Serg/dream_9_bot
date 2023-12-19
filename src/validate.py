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


class Country(Field):

    def __init__(self, value=''):
        while True:
            country_404 = ['russia', 'rossiya', 'rossiia', 'rossiya',
                           'rasiya', 'rossiya', 'rosija', 'rusia', 'rwsia', 'rwsiya', 'росія', 'россия', 'росия', 'россія', 'руссія', 'русія']
            if value:
                self.value = value
            else:
                self.value = input('Громадянство (країна): ')
            # валідація введеної країни по наявності в списку заборонених країн
            try:
                if self.value.lower() in country_404:
                    raise ValueError
                elif self.value.capitalize():
                    break
                else:
                    raise ValueError
            except ValueError:
                print('На щастя, такої країни не існує або вона вже на межі колапсу. Ваш контакт не буде додано, спробуйте іншу країну для продовження.')

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
                    "Будь ласка введіть номер телефону у форматі 10 чисел, починаючи з нуля (для декількох номерів використовуйте пробіл між ними): ")
            # перевірка на правильність введенного телефонного номеру
            try:
                for number in self.values.split(' '):
                    if re.match(r'^\d{10}$', number) or number == '':
                        self.value.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print(
                    'Будь ласка введіть номер правильно; має бути 10 чисел.')
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
                input_value = input("Дата народження (dd.mm.YYYY): ")
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
                    'Дата народження має бути у форматі: день.місяць.рік. Дата народження не може бути в майбутньому!')

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
                print('Будь ласка введіть email в правильному форматі.')

    def __getitem__(self):
        return self.value


class Note(Field):

    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value
