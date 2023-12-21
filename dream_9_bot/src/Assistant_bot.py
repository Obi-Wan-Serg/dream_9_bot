import cmd
from rich.console import Console
from rich.table import Table
from rich.text import Text
from pathlib import Path
from .get_weather_module import get_weather, format_weather
from .AddressBook import AddressBook, Record, Name, Phone, Birthday, Email, Country, Note, Tag
from .main import main
from .game import GuessNumberGame

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[0;33m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


class AddressBookCLI(cmd.Cmd):
    intro = f'{RESET}{
        BLUE}Щоб побачити доступні команди наберіть {YELLOW}help{BLUE} чи {YELLOW}?{BLUE}.\nЩоб побачити інформацію про конкретну команду наберіть help [назва_команди]{RESET}{YELLOW}'
    prompt = f'{YELLOW}>>>>>>>  '
    console = Console()

    def __init__(self):
        super().__init__()
        self.book = AddressBook()

    def default(self, line):
        self.stdout.write(f"{RESET}{RED}Невідома команда:{
                          RESET} {MAGENTA}{line}\n{RESET}{YELLOW}")

    def do_play_game(self, arg):
        'Запустити гру "Вгадай число"'
        game = GuessNumberGame()
        game.play()
        self.console.print("Дякуємо за гру!", style="bold green")

    def do_sort_files(self, args):
        'Sort files in a directory'
        folder_path = input(
            f"{RESET}{BLUE}Будь ласка вкажіть шлях до папки\nв якій необхідно відсортувати файли: {RESET}{YELLOW}")
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            self.console.print(
                "Вказано невірний шлях. Спробуйте ще раз.", style="italic red")
            return
        try:
            # Виклик функції сортування
            main(folder_path.resolve())
            self.console.print(f"Файли за шляхом {
                               folder_path} були відсортовані.", style="italic blue")
        except Exception as e:
            self.console.print(f"An error occurred: {e}", style="italic red")

    def do_add(self, arg):
        'Add a new contact: add'
        name = Name(input(f"{RESET}{BLUE}Ім'я: {RESET}{YELLOW}")).value.strip()
        country = Country().value.capitalize()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        note = Note(input(f"{RESET}{BLUE}Нотатка: {RESET}{YELLOW}")).value
        tags_input = input(
            f"{RESET}{BLUE}Теги (через пробіл): {RESET}{YELLOW}")
        tags = [Tag(tag.strip()).value for tag in tags_input.split()]
        record = Record(name, country, phones, birth, email, note, tags)
        self.book.add(record)
        self.console.print("Контакт успішно додано.", style="bold green")

    def do_search(self, arg):
        'Search contacts: search'
        print(f"{RESET}{BLUE}Є наступні категорії: \nName \nCountry \nPhones \nBirthday \nEmail \nNote \nTags{
              RESET}{YELLOW}")
        category = input(f'{RESET}{BLUE}Пошук за категорією: {RESET}{YELLOW}')
        pattern = input(
            f'{RESET}{BLUE}Введіть текст для пошуку: {RESET}{YELLOW}')

        if category.lower() == 'tags':
            # Searching based on tags
            result = self.book.search_by_tags(pattern)
        else:
            result = self.book.search(pattern, category)

        if not result:
            self.console.print(
                "Такий контакт відсутній в книзі контактів!", style="bold red")
            return

        table = Table(show_header=True, header_style="bold white")

        # Додаємо стовпці до таблиці
        table.add_column("Ім'я")
        table.add_column("Країна")
        table.add_column("Телефон")
        table.add_column("Дата народження", justify="right")
        table.add_column("Електронна пошта", justify="right")
        table.add_column("Примітка", justify="right")
        table.add_column("Теги", justify="right")

        # Додаємо результати пошуку до таблиці з використанням Text для форматування
        for account in result:
            name = Text(account['name'], style="blue")
            country = Text(account['country'], style="yellow")
            phone = Text(
                ', '.join(account['phones']) if account['phones'] else "", style="blue")
            birth = Text(account['birthday'].strftime(
                '%d.%m.%Y') if account['birthday'] else "", style="yellow")
            email = Text(account['email'], style="blue")
            note = Text(account['note'], style="yellow")
            tags = Text(
                ', '.join(account['tags']) if account['tags'] else "", style="bold blue")

            table.add_row(name, country, phone, birth, email, note, tags)

        self.console.print(table)

    def do_edit(self, arg):
        'Edit a contact: edit'
        contact_name = input(f"{RESET}{BLUE}Ім'я контакту: {RESET}{YELLOW}")
        parameter = input(
            f'{RESET}{BLUE}Оберіть параметр для редагування\n(name, country, phones, birthday, email, note): {RESET}{YELLOW}').strip()
        new_value = input(f"{RESET}{BLUE}Нове значення: {RESET}{YELLOW}")
        self.book.edit(contact_name, parameter, new_value)
        self.console.print("Контакт успішно відредаговано.",
                           style="bold green")

    def do_remove(self, arg):
        'Remove a contact: remove'
        pattern = input(
            f"{RESET}{BLUE}Видалити (ім'я контакту чи номер телефону): {RESET}{YELLOW}")
        self.book.remove(pattern)
        self.console.print("Контакт успішно видалено.", style="bold green")

    def do_save(self, arg):
        'Save address book to a file: save'
        file_name = input(f"{RESET}{BLUE}Ім'я файла: {RESET}{YELLOW}")
        self.book.save(file_name)
        self.console.print(
            "Книга контактів успішно збережена.", style="bold green")

    def do_load(self, arg):
        'Load address book from a file: load'
        file_name = input(f"{RESET}{BLUE}Ім'я файла: {RESET}{YELLOW}")
        self.book.load(file_name)
        self.console.print(
            "Книга контактів успішно завантажена.", style="bold green")

    def do_congratulate(self, arg):
        'Congratulate contacts: congratulate'
        self.console.print(self.book.congratulate(), style="bold magenta")

    def do_view(self, arg):
        'View all contacts: view'
        table = Table(show_header=True, header_style="bold white")

        # Додаємо стовпці до таблиці
        table.add_column("Ім'я")
        table.add_column("Країна")
        table.add_column("Телефон")
        table.add_column("Дата народження", justify="right")
        table.add_column("Електронна пошта", justify="right")
        table.add_column("Примітка", justify="right")
        table.add_column("Теги", justify="right")

        # Додаємо дані контактів до таблиці з використанням Text для форматування
        for account in self.book.data:
            name = Text(account['name'], style="blue")
            country = Text(account['country'], style="yellow")
            phone = Text(
                ', '.join(account['phones']) if account['phones'] else "", style="blue")
            birth = Text(account['birthday'].strftime(
                '%d.%m.%Y') if account['birthday'] else "", style="yellow")
            email = Text(account['email'], style="blue")
            note = Text(account['note'], style="yellow")
            tags = Text(
                ', '.join(account['tags']) if account['tags'] else "", style="bold blue")

            table.add_row(name, country, phone, birth, email, note, tags)

        self.console.print(table)

    def do_weather(self, arg):
        'Get weather for a city: weather [city_name]'
        city = arg or input(
            f"{RESET}{BLUE}Введіть назву міста: {RESET}{YELLOW}")
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
