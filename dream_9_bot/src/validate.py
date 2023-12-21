from datetime import date, datetime
import re
from abc import ABC, abstractmethod

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[0;33m"
BLUE = "\033[94m"
RESET = "\033[0m"


class Record:

    def __init__(self, name, country='', phones='', birthday='', email='', note='', tags=None):

        self.birthday = birthday
        self.name = name
        self.phones = phones
        self.email = email
        self.country = country
        self.note = note
        self.tags = tags if tags else []

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
                self.value = input(
                    f'{RESET}{BLUE}Громадянство (країна): {RESET}{YELLOW}')
            # валідація введеної країни по наявності в списку заборонених країн
            try:
                if self.value.lower() in country_404:
                    raise ValueError
                elif self.value.capitalize():
                    break
                else:
                    raise ValueError
            except ValueError:
                print(f'{RESET}{RED}На щастя, такої країни не існує або вона вже на межі колапсу.\nВаш контакт не буде додано, спробуйте іншу країну для продовження.{
                      RESET}{YELLOW}')

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
                    f"{RESET}{BLUE}Будь ласка введіть номер телефону у форматі 10 чисел, починаючи з нуля\n(для декількох номерів використовуйте пробіл між ними): {RESET}{YELLOW}")
            # перевірка на правильність введенного телефонного номеру
            try:
                for number in self.values.split(' '):
                    if re.match(r'^\d{10}$', number) or number == '':
                        self.value.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print(
                    f'{RESET}{RED}Будь ласка введіть номер правильно; має бути 10 чисел.{RESET}{YELLOW}')
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
                input_value = input(
                    f"{RESET}{BLUE}Дата народження (dd.mm.YYYY): {RESET}{YELLOW}")
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
                    f'{RESET}{RED}Дата народження має бути у форматі: день.місяць.рік.\nДата народження не може бути в майбутньому!{RESET}{YELLOW}')

    def __getitem__(self):
        return self.value


class Email(Field):

    def __init__(self, value=''):
        while True:

            if value:
                self.value = value
            else:
                self.value = input(f"{RESET}{BLUE}Email: {RESET}{YELLOW}")
            try:
                # перевірка правильності введення електронної адреси
                if re.match(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print(f'{RESET}{RED}Будь ласка введіть email в правильному форматі.{
                      RESET}{YELLOW}')

    def __getitem__(self):
        return self.value


class Note(Field):

    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class Tag(Field):

    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input(f"{RESET}{BLUE}Тег: {RESET}{YELLOW}")
            # Additional validation can be added if needed
            if self.value:
                break
            else:
                print(f'{RESET}{RED}Будь ласка, введіть значення тегу.{
                      RESET}{YELLOW}')

    def __getitem__(self):
        return self.value
