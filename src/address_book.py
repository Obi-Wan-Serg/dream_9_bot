from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __str__(self):
        return f"Name: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    # поки так залишаю, але думаю, що тут можна зробити імпорт усіх перевірок з validate.py
    def validate(self, value):
        pass


class Phone(Field):
    def __str__(self):
        return f"Phone: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        pass


class Birthday(Field):
    def __str__(self):
        return f"Birthday: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        pass


class Email(Field):
    def __str__(self):
        return f"Email: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        pass


class Address(Field):
    def __str__(self):
        return f"Address: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.addresses = []

    def __str__(self):
        result = f"{self.name}"
        if self.phones:
            result += f"\nContact name: {self.name.value}, phones: {', '.join(p.value for p in self.phones)}"
        if self.birthday:
            result += f"\n{self.birthday}"
        if self.emails:
            result += f"\nEmail: {'; '.join(e.value for e in self.emails)}"
        if self.addresses:
            result += f"\nAddress: {'; '.join(a.value for a in self.addresses)}"
        return result

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        self.birthday.validate(birthday)

    def add_email(self, email):
        email_field = Email(email)
        email_field.validate(email)
        if email_field not in self.emails:
            self.emails.append(email_field)

    def add_address(self, address):
        address_field = Address(address)
        address_field.validate(address)
        if address_field not in self.addresses:
            self.addresses.append(address_field)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

#для тестування
# book = AddressBook()
#
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_birthday("1986-12-23")
# john_record.add_email("mail@gmail.com")
# john_record.add_address("Kyiv, Zdolbunivska 12 St")
# book.add_record(john_record)
#
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_birthday("2003-05-16")
# jane_record.add_email("mail200@gmail.com")
# jane_record.add_address("Poltava, Hohol 43 St")
# book.add_record(jane_record)
#
# for name, record in book.data.items():
#     print(record)
#     print("---------------")