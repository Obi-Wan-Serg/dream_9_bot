import re
from datetime import date, datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        valid_value = re.sub(r'\D', '', value)
        super().__init__(valid_value)

    def validate(self, value):
        valid_value = re.sub(r'\D', '', value)
        if len(value) != 10 or len(valid_value) != 10:
            raise ValueError('The phone number must consist of 10 digits')


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        pattern = r"[a-zA-Z]{1}[\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}"
        if not re.match(pattern, str(self.value)):
            raise ValueError('The email has an invalid format')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        try:
            b_date = datetime.strptime(str(self.value), '%Y.%m.%d').date()
            today = date.today()
            if b_date > today:
                raise ValueError('The birthday date cannot be in the future!')
            self.value = b_date
        except ValueError as e:
            raise ValueError(
                'The birthday date must be entered in format: YYYY.MM.DD') from e

# працює з вхідними даними що приведено нижче
# try:
#     phone = Phone("1234567890")
#     print(f"Phone: {phone}")

#     email = Email("test@test.net")
#     print(f"Email: {email}")

#     birthday = Birthday("1975.05.29")
#     print(f"Birthday: {birthday}")
# except ValueError as e:
#     print(f"Error: {e}")
