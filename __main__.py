import os
from src.Assistant_bot import AddressBookCLI
from rich.console import Console

if __name__ == "__main__":
    console = Console()

    console.print('Привіт. Я ваш помічник з контактами.', style="bold green")
    console.print('Що я маю зробити з вашими контактами?', style="bold blue")

    cli = AddressBookCLI()

    file_path = os.path.join('src', 'auto_save.bin')

    # Перевіряємо, чи існує файл перед його завантаженням
    if os.path.exists(file_path):
        cli.book.load("auto_save")
        console.print("Завантажено існуючу адресну книгу.",
                      style="italic yellow")
    else:
        console.print(
            "Жодного збереженого адресного книги не знайдено. Починаємо з порожньої книги.", style="italic red")

    cli.cmdloop()

    # Зберігаємо адресну книгу при виході
    cli.book.save("auto_save")
    console.print("До побачення!", style="bold magenta")
