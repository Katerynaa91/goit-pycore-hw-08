"""Завдання. Додати поле birthday для дня народження в клас Record. Це поле має бути класу Birthday. Це поле не обов'язкове, але може бути тільки одне.
Додати функцію add_birthday у клас Record, яка додає день народження (клас Birthday) до контакту. Додати перевірки правильності наведених значень для полів Phone, Birthday.
Додати та адаптувати до класу AddressBook функцію з четвертого домашнього завдання, тиждень 3, get_upcoming_birthdays, яка для контактів адресної книги повертає список користувачів, 
яких потрібно привітати по днях на наступному тижні.
"""

from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису"""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    """Клас для зберігання імені контакту. Наслідується від класу Field. Мість перевірку на довжину введеного імені."""
    def __init__(self, value):
        super().__init__(value)
        if len(str(value)) < 2:
            raise ValueError("The name should have at least 2 letters. Please use a different name")
        else: self.value = str(value).title()


class Phone(Field):
    """Клас для зберігання номера телефону. Для валідації формату (10 цифр) використовується модуль re. Наслідується від класу Field."""
    phone_pattern = r'\b[0-9]{10}\b'

    def __init__(self, value):
        super().__init__(value)
        if re.match(Phone.phone_pattern, str(value)):
            self.value = value
        else: raise ValueError("Incorrect phone format")
            #self.value = None


class Birthday(Field):
    """Клас для зберігання дня народження. Мість перевірку правильності введеної дати - атрибуту класу"""
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Клас для зберігання імені та списку телефонів контакту."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    

    def add_birthday(self, value):
        """Метод для додавання дати народження - об'єкту класу Birthday."""
        try:
            self.birthday = Birthday(value)
        except ValueError: 
            print("Invalid date format. Use DD.MM.YYYY")

    
    def add_phone(self, phone):
        """Метод для додавання номерів телефонів для певного контакту. Якщо фомат номеру невірний (повертається None) 
        або якщо телефон вже є у списку телефонів, виводиться відповідне повідомлення."""
        if Phone(phone) in self.phones:
            print(f"The phone number {phone} is already in your Contacts list")
        else:
            if Phone(phone):
                self.phones.append(Phone(phone))
                # print(f"Phone {phone} added to the Contacts list")
                return self.phones
            
            else: print(f"Unsupported format of the phone number {phone}. Please enter a valid number.")
    

    def remove_phone(self, phone):
        """Метод для видалення телефонів контакту. Якщо номер не знайдено у списку телефонів, виводиться відповідне повідомлення."""
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                # print(f"Phone number {str(p)} removed from the Contacts list.")
            else:
                print(f"Couldn't remove the phone. Phone number {phone} not in the Contacts list")


    def edit_phone(self, old_phone, new_phone):
        """Метод для редагування телефонів контакту. Якщо новий номер не відповідає формату телефону, повертається попередній список телефонів.
        Перевіряється, чи номер телефону, який потрібно змінити, існує у списку телефонів даного контакту."""
        
        if not Phone(new_phone).value:
            print("Unsupported format of the new number")
            
        else:
            if old_phone in [p.value for p in self.phones]:
                self.phones[[p.value for p in self.phones].index(old_phone)] = Phone(new_phone)
                
            else: print("The number you are trying to replace is not in your Contacts list")
    

    def find_phone(self, phone):
        """Метод для пошуку номера телефону контакту у списку його телефонів. Якщо телефон не знайдено, викликається виключення."""
        if phone in [p.value for p in self.phones]:
            return Phone(phone)
        else: 
            raise ValueError("Phone number not in your Contacts list")


    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

class AddressBook(UserDict):
    """Клас для зберігання та управління записами про всі контакти. Наслудється від класу UserDict. 
    Атрибут класу - словник, де ключем є ім'я контакту, значення - список його номерів телефонів."""
    def __init__(self, **kwargs):
        self.data = dict(kwargs)


    def add_record(self, key):
        """Метод для додавання записів до словника-атрибута класу. 
        У якості ключа - ім'я об'єкта класу Record, значення - список зі списків номерів телефонів (об'єкти класу Record) та дати народження.
        """
        try:
            self.data[key.name.value] = []
            self.data[key.name.value].append([p.value for p in key.phones])
            self.data[key.name.value].append(datetime.strftime(key.birthday.value, "%d.%m.%Y"))

        except (KeyError, AttributeError):
            return f"No Record found for {key}"
        

    def find (self, key):
        """Метод для пошуку запису за ім'ям-ключем у словнику контактів. Обробляється помилка, якщо імені немає у словнику контактів.""" 
        try:
            return self.data[key.title()]if key.title() in [k for k in self.data.keys()] else None
        except KeyError: print(f"Name '{key}' not found")
        # не зрозуміла із завдання, чи треба залишити, як було у попередньому завданні, і виводити тільки номери телефону, чи 
        # виводити разом із датою народження. Якщо треба без дати народження, тільки телефон, то 
        # замість self.data[key.title()] треба використати self.data[key.title()][0]        
       

    def delete(self, key):
        """Метод для видалення запису за ім'ям-ключем у словнику контактів. Виводиться відповідне помідомлення,
        якщо ім'я вудсутнє у словнику контактів і не може бути видалене.""" 
        if key.title() in self.data:
            del self.data[key.title()]
            print(f"{key} deleted")
        else: print(f"Cannot delete name {key} as it was not found in your Contacts list")


    def get_upcoming_birthdays(self):
        """Метод для виокремлення днів народження, які випадають на найближчі 7 днів. Якщо день народження випадає на вихідні, дата привітання переноситься 
        на понеділок."""

        seven_days_dates_lst = [datetime.today().date() + timedelta(i) for i in range(timedelta(days=7).days)]
        all_birthdays = [datetime.strptime(x[-1], "%d.%m.%Y").date().replace(year=datetime.today().year) for x in self.data.values()]
        congratulations_lst = list(filter((lambda i: i in seven_days_dates_lst), all_birthdays))
        for key, value in self.data.items():
            value[-1] = datetime.strptime(value[-1], "%d.%m.%Y").replace(year=datetime.today().year).date() 
            if value[-1] in congratulations_lst:
                if value[-1].weekday() == 5:
                   value[-1] = value[-1] +timedelta(days = 2)
                elif value[-1].weekday() == 6:
                    value[-1] = value[-1] +timedelta(days = 1)
                yield f"This week B-Days: {key} on {value[-1]}"


if __name__ == "__main__":
    pass


