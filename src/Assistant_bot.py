from AddressBook import *


class Bot:
    def __init__(self):
        self.book = AddressBook()

    def handle(self, action):
        if action == 'add':
            name = Name(input("Name: ")).value.strip()
            phones = Phone().value
            birth = Birthday().value
            email = Email().value.strip()
            status = Status().value.strip()
            note = Note(input("Note: ")).value
            record = Record(name, phones, birth, email, status, note)
            return self.book.add(record)
        elif action == 'search':
            print("Choose a group: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
            group = input('Search group: ')
            sample = input('Search sample: ')
            result = (self.book.search(sample, group))
            for contact in result:
                if contact['birthday']:
                    birth = contact['birthday'].strftime("%d/%m/%Y")
                    result = "_" * 50 + "\n" + f"Name: {contact['name']} \nPhones: {', '.join(contact['phones'])} \nBirthday: {birth} \nEmail: {contact['email']} \nStatus: {contact['status']} \nNote: {contact['note']}\n" + "_" * 50
                    print(result)
        elif action == 'edit':
            contact_name = input('Contact name: ')
            parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
            new_value = input("New Value: ")
            return self.book.edit(contact_name, parameter, new_value)
        elif action == 'remove':
            sample = input("Remove (contact name or phone): ")
            return self.book.remove(sample)
        elif action == 'save':
            file_name = input("File name: ")
            return self.book.save(file_name)
        elif action == 'load':
            file_name = input("File name: ")
            return self.book.load(file_name)
        elif action == 'congratulate':
            print(self.book.congratulate())
        elif action == 'view':
            print(self.book)
        elif action == 'exit':
            pass
        else:
            print("There is no such command!")
=======
import cmd
from rich.console import Console
from rich.table import Table
from rich.text import Text
from get_weather import get_weather, format_weather
from AddressBook import AddressBook, Record, Name, Phone, Birthday, Email, Status, Note

class AddressBookCLI(cmd.Cmd):
    intro = 'Welcome to the Address Book. Type help or ? to list commands.\n'
    prompt = '>>>>>>>'
    console = Console()

    def __init__(self):
        super().__init__()
        self.book = AddressBook()

    def do_add(self, arg):
        'Add a new contact: add'
        name = Name(input("Name: ")).value.strip()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        status = Status().value.strip()
        note = Note(input("Note: ")).value
        record = Record(name, phones, birth, email, status, note)
        self.book.add(record)
        self.console.print("Contact added successfully.", style="bold green")

    

    def do_search(self, arg):
        'Search contacts: search'
        print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
        category = input('Search category: ')
        pattern = input('Search pattern: ')
        result = self.book.search(pattern, category)

        if not result:
            self.console.print("There is no such contact in address book!", style="bold red")
            return

        table = Table(show_header=True, header_style="bold magenta")

        # Додаємо стовпці до таблиці
        table.add_column("Ім'я")
        table.add_column("Телефон")
        table.add_column("Дата народження", justify="right")
        table.add_column("Електронна пошта", justify="right")
        table.add_column("Статус", justify="right")
        table.add_column("Примітка", justify="right")

        # Додаємо результати пошуку до таблиці з використанням Text для форматування
        for account in result:
            name = Text(account['name'], style="cyan")
            phone = Text(', '.join(account['phones']) if account['phones'] else "", style="magenta")
            birth = Text(account['birthday'].strftime("%d/%m/%Y") if account['birthday'] else "", style="green")
            email = Text(account['email'], style="blue")
            status = Text(account['status'], style="yellow")
            note = Text(account['note'], style="red")

            table.add_row(name, phone, birth, email, status, note)

        self.console.print(table)

    def do_edit(self, arg):
        'Edit a contact: edit'
        contact_name = input('Contact name: ')
        parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
        new_value = input("New Value: ")
        self.book.edit(contact_name, parameter, new_value)
        self.console.print("Contact edited successfully.", style="bold green")

    def do_remove(self, arg):
        'Remove a contact: remove'
        pattern = input("Remove (contact name or phone): ")
        self.book.remove(pattern)
        self.console.print("Contact removed successfully.", style="bold green")

    def do_save(self, arg):
        'Save address book to a file: save'
        file_name = input("File name: ")
        self.book.save(file_name)
        self.console.print("Address book saved successfully.", style="bold green")

    def do_load(self, arg):
        'Load address book from a file: load'
        file_name = input("File name: ")
        self.book.load(file_name)
        self.console.print("Address book loaded successfully.", style="bold green")

    def do_congratulate(self, arg):
        'Congratulate contacts: congratulate'
        self.console.print(self.book.congratulate(), style="bold yellow")

    def do_view(self, arg):
        'View all contacts: view'
        table = Table(show_header=True, header_style="bold magenta")

        # Додаємо стовпці до таблиці
        table.add_column("Ім'я")
        table.add_column("Телефон")
        table.add_column("Дата народження", justify="right")
        table.add_column("Електронна пошта", justify="right")
        table.add_column("Статус", justify="right")
        table.add_column("Примітка", justify="right")

        # Додаємо дані контактів до таблиці з використанням Text для форматування
        for account in self.book.data:
            name = Text(account['name'], style="cyan")
            phone = Text(', '.join(account['phones']) if account['phones'] else "", style="magenta")
            birth = Text(account['birthday'].strftime("%d/%m/%Y") if account['birthday'] else "", style="green")
            email = Text(account['email'], style="blue")
            status = Text(account['status'], style="yellow")
            note = Text(account['note'], style="red")

            table.add_row(name, phone, birth, email, status, note)

        self.console.print(table)

    def do_weather(self, arg):
        'Get weather for a city: weather [city_name]'
        city = arg or input("Enter city name: ")
        api_key = '16bfe776fb8afe007ed1f21a6277aba2'  # Ваш API-ключ
        try:
            weather_data = get_weather(city, api_key)
            weather_report = format_weather(weather_data)
            self.console.print(weather_report, style="bold blue")
        except Exception as e:
            self.console.print(f"Error: {str(e)}", style="bold red")


    def do_exit(self, arg):
        'Exit the application: exit'
        return True

if __name__ == '__main__':
    AddressBookCLI().cmdloop()