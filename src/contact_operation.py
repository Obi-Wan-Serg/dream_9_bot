from collections import UserDict


class Record:

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def find_phone(self, phone):
        found_phones = [p.value for p in self.phones if str(p) == phone]
        return found_phones[0] if found_phones else None

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone.value) == old_phone:
                phone.value = new_phone
                break
        else:
            raise ValueError("Phone number does not exist in the record")

    def get_phones(self):
        return [str(phone.value) for phone in self.phones]

    def remove_email(self, email):
        self.emails = [p for p in self.emails if str(p) != email]

    def find_email(self, email):
        found_emails = [p.value for p in self.emails if str(p) == email]
        return found_emails[0] if found_emails else None

    def edit_email(self, old_email, new_email):
        for email in self.emails:
            if str(email.value) == old_email:
                email.value = new_email
                break
        else:
            raise ValueError("Email does not exist in the record")

    def get_emails(self):
        return [str(email.value) for email in self.emails]

    def remove_address(self, address):
        self.addresses = [p for p in self.addresses if str(p) != address]

    def find_address(self, address):
        found_addresses = [p.value for p in self.addresses if str(p) == address]
        return found_addresses[0] if found_addresses else None

    def edit_address(self, old_address, new_address):
        for email in self.emails:
            if str(email.value) == old_address:
                email.value = new_address
                break
        else:
            raise ValueError("Address does not exist in the record")

    def get_address(self):
        return [str(address.value) for address in self.addresses]





class AddressBook(UserDict):

    def find(self, name):
        name_lower = name.lower()
        return next((record for record in self.data.values() if record.name.value.lower() == name_lower), None)

    def delete(self, name):
        record = next((record for record in self.data.values() if record.name.value.lower() == name.lower()), None)
        if record:
            del self.data[record.name.value]

    def change_phone(self, name, old_phone, new_phone):
        name_lower = name.lower()
        record = self.find(name_lower)
        if record:
            record.edit_phone(old_phone, new_phone)
        else:
            raise ValueError(f"Contact {name} not found")

    def change_email(self, name, old_email, new_email):
        name_lower = name.lower()
        record = self.find(name_lower)
        if record:
            record.edit_email(old_email, new_email)
        else:
            raise ValueError(f"Contact {name} not found")

    def change_address(self, name, old_address, new_address):
        name_lower = name.lower()
        record = self.find(name_lower)
        if record:
            record.edit_address(self, old_address, new_address)
        else:
            raise ValueError(f"Contact {name} not found")
          
    def search(self, query):
        query = query.lower()
        results = []
        for record in self.data.values():
            if (
                query in record.name.value.lower() or
                any(query in str(phone.value) for phone in record.phones)
            ):
                results.append(str(record))
        return results



def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"

    return wrapper


contacts = AddressBook()



@input_error
def delete_contact(command):
    name = command[1]
    contacts.delete(name)
    return f"Contact {name} deleted"


@input_error
def change_phone(name, new_phone):
    contact = contacts.find(name)
    if contact:
        contact.edit_phone(contact.phones[0].value, new_phone)
        return f"Phone number for {name} changed to {new_phone}"
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def change_email(name, new_email):
    contact = contacts.find(name)
    if contact:
        contact.edit_phone(contact.phones[0].value, new_email)
        return f"Phone number for {name} changed to {new_email}"
    else:
        raise ValueError(f"Contact {name} not found")

    
@input_error
def change_address(name, new_address):
    contact = contacts.find(name)
    if contact:
        contact.edit_phone(contact.phones[0].value, new_address)
        return f"Phone number for {name} changed to {new_address}"
    else:
        raise ValueError(f"Contact {name} not found")
    
    
@input_error
def get_phones(command):
    name = split(command)[1]
    contact = next((record for record in contacts.data.values() if record.name.value.lower() == name.lower()), None)
    if contact and contact.phones:
        return f"Phone numbers for {contact.name.value}: {', '.join(map(str, contact.get_phones()))}"
    else:
        raise ValueError(f"Contact {name.capitalize()} not found")


@input_error
def show_all():
    page = contacts.get_page(contacts.current_page)
    result = "\n".join(str(record) for record in page)
    return f"Page {contacts.current_page}:\n{result}"


@input_error
def show_n_records(n):
    records = contacts.get_n_records(n)
    result = "\n".join(records)
    return f"{n} records:\n{result}"


@input_error
def search_contacts(command):
    query = split(command)[1]
    results = contacts.search(query)
    if results:
        return f"Search results for '{query}':\n" + "\n".join(results)
    else:
        return f"No results found for '{query}'."



