from datetime import datetime, timedelta


class Contact:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

    def days_until_birthday(self):
        # Отримаємо сьогоднішню дату
        today = datetime.now().date()
        # Обчислити наступний день народження
        next_birthday = datetime(today.year, self.birthday.month, self.birthday.day).date()

        # Перевірка, чи не минув день народження в цьому році
        if today > next_birthday:
            # Якщо минув, обчислити наступний день народження на наступний рік
            days_lefs = datetime(today.year + 1, self.birthday.month, self.birthday.day).date()

        # Обчислити дні, що залишилися до наступного дня народження
        days_lefs = (next_birthday - today).days
        return days_lefs
    

class PersonalAssistant:
    def __init__(self, contacts):
        self.contacts = contacts
    
    def show_upcoming_birthdays(self, days):
        # Отримаємо поточну дату та час
        today = datetime.now()
        # Список для зберігання майбутніх днів народження
        upcoming_birthdays = []

        for contact in self.contacts:
            # Підрахувати дні, що залишилися до дня народження контакту
            days_lefs = contact.days_until_birthday()
            # Перевірка, чи день народження знаходиться в межах вказаної кількості днів
            if 0 < days_lefs <= days:
                # Додайте ім'я контакту та дні, що залишилися, до списку upcoming_birthdays
                upcoming_birthdays.append((contact.name, days_lefs))
        
        return upcoming_birthdays
    

# if __name__ == '__main__':
#     contacts = [
#         Contact('Olha', datetime(2000, 1, 12)),
#         Contact('Sam', datetime(2010, 12, 31)),
#         ]
    
#     assistant = PersonalAssistant(contacts)

#     upcoming_birthdays = assistant.show_upcoming_birthdays(30)

#     if upcoming_birthdays:
#         print('Контакти з наближеними днями народження:')
#         for name, days_left in upcoming_birthdays:
#             print(f'{name}: через {days_left} днів.')
#     else:
#         print('Немає контактів з наближеними днями народження.')