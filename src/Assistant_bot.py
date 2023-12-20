import cmd
from rich.console import Console
from rich.table import Table
from rich.text import Text
from .get_weather_module import get_weather, format_weather
from .AddressBook import AddressBook, Record, Name, Phone, Birthday, Email, Country, Note, Tag


class AddressBookCLI(cmd.Cmd):
    intro = 'Для користування книгою контактів наберіть help чи ?.\n'
    prompt = '>>>>>>>'
    console = Console()

    def __init__(self):
        super().__init__()
        self.book = AddressBook()

    def do_add(self, arg):
        'Add a new contact: add'
        name = Name(input("Ім'я: ")).value.strip()
        country = Country().value.capitalize()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        note = Note(input("Нотатка: ")).value
        tags_input = input ( "Теги (через пробіл): " )
        tags = [Tag ( tag.strip ( ) ).value for tag in tags_input.split ( )]
        record = Record(name, country, phones, birth, email, note, tags)
        self.book.add(record)
        self.console.print("Контакт успішно додано.", style="bold green")

    def do_search(self, arg):
        'Search contacts: search'
        print ( "Є наступні категорії: \nName \nCountry \nPhones \nBirthday \nEmail \nNote \nTags" )
        category = input ( 'Пошук за категорією: ' )
        pattern = input ( 'Введіть текст для пошуку: ' )

        if category.lower ( ) == 'tags':
            # Searching based on tags
            result = self.book.search_by_tags ( pattern )
        else:
            result = self.book.search ( pattern, category )

        if not result:
            self.console.print(
                "Такий контакт відсутній в книзі контактів!", style="bold red")
            return

        table = Table(show_header=True, header_style="bold magenta")

        # Додаємо стовпці до таблиці
        table.add_column("Ім'я")
        table.add_column("Країна")
        table.add_column("Телефон")
        table.add_column("Дата народження", justify="right")
        table.add_column("Електронна пошта", justify="right")
        table.add_column("Примітка", justify="right")
        table.add_column ( "Теги", justify="right" )


        # Додаємо результати пошуку до таблиці з використанням Text для форматування
        for account in result:
            name = Text(account['name'], style="cyan")
            country = Text(account['country'], style="yellow")
            phone = Text(
                ', '.join(account['phones']) if account['phones'] else "", style="magenta")
            birth = Text(account['birthday'].strftime(
                '%d.%m.%Y') if account['birthday'] else "", style="green")
            email = Text(account['email'], style="blue")
            note = Text(account['note'], style="red")
            tags = Text ( ', '.join ( account['tags'] ) if account['tags'] else "", style="bold white" )

            table.add_row ( name, country, phone, birth, email, note, tags )

        self.console.print(table)

    def do_edit(self, arg):
        'Edit a contact: edit'
        contact_name = input("Ім'я контакту: ")
        parameter = input(
            'Оберіть параметр для редагування (name, country, phones, birthday, email, note): ').strip()
        new_value = input("Нове значення: ")
        self.book.edit(contact_name, parameter, new_value)
        self.console.print("Контакт успішно відредаговано.",
                           style="bold green")

    def do_remove(self, arg):
        'Remove a contact: remove'
        pattern = input("Видалити (ім'я контакту чи номер телефону): ")
        self.book.remove(pattern)
        self.console.print("Контакт успішно видалено.", style="bold green")

    def do_save(self, arg):
        'Save address book to a file: save'
        file_name = input("Ім'я файла: ")
        self.book.save(file_name)
        self.console.print(
            "Книга контактів успішно збережена.", style="bold green")

    def do_load(self, arg):
        'Load address book from a file: load'
        file_name = input("Ім'я файла: ")
        self.book.load(file_name)
        self.console.print(
            "Книга контактів успішно завантажена.", style="bold green")

    def do_congratulate(self, arg):
        'Congratulate contacts: congratulate'
        self.console.print(self.book.congratulate(), style="bold yellow")

    def do_view(self, arg):
        'View all contacts: view'
        table = Table(show_header=True, header_style="bold magenta")

        # Додаємо стовпці до таблиці
        table.add_column("Ім'я")
        table.add_column("Країна")
        table.add_column("Телефон")
        table.add_column("Дата народження", justify="right")
        table.add_column("Електронна пошта", justify="right")
        table.add_column("Примітка", justify="right")
        table.add_column ( "Теги", justify="right" )

        # Додаємо дані контактів до таблиці з використанням Text для форматування
        for account in self.book.data:
            name = Text(account['name'], style="cyan")
            country = Text(account['country'], style="yellow")
            phone = Text(
                ', '.join(account['phones']) if account['phones'] else "", style="magenta")
            birth = Text(account['birthday'].strftime(
                '%d.%m.%Y') if account['birthday'] else "", style="green")
            email = Text(account['email'], style="blue")
            note = Text(account['note'], style="red")
            tags = Text ( ', '.join ( account['tags'] ) if account['tags'] else "", style="bold white" )

            table.add_row ( name, country, phone, birth, email, note, tags )

        self.console.print(table)

    def do_weather(self, arg):
        'Get weather for a city: weather [city_name]'
        city = arg or input("Введіть назву міста: ")
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
