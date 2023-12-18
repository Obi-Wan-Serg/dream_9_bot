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
