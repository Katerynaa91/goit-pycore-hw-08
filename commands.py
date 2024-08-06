"""Завдання. Додати до функціоналу бота функції обробники з наступними командами:
•	add-birthday - додаємо до контакту день народження в форматі DD.MM.YYYY
•	show-birthday - показуємо день народження контакту
•	birthdays - повертає список користувачів, яких потрібно привітати по днях на наступному тижні

Створити функції для збереження та завантаження даних, отриманих під час роботи застосунку за допомогою
модуля pickle"""

from phonebook import Record, Phone, AddressBook
from typing import Callable
from functools import wraps
import pickle


def input_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError, IndexError):
            print("Invalid request. Make sure to enter command/name/phone/birthday in the correct format")
        except (KeyError): 
            print("Name not found in the Contacts")
    return wrapper


@input_error
def parse_input(input_val: str) -> list:
    """Функція парсить рядок-запит, введений користувачем та обробляє випадок, якщо кількість 
    введених елементів не відповідає очікуваній структурі команди."""

    parsed_input = input_val.lower().split()
    if len(parsed_input) <= 3:
        return parsed_input
    else: raise ValueError
    

@input_error
def add_contact(args: list, book: AddressBook):
    """Функція для додавання номеру телефону до книги контактів. Якщо імені немає в списку контактів - додається ім'я та номер телефону,
    якщо є ім'я і номер телефону - телефон змінюється,
    якщо книга контактів мість ім'я та день народження, додається номер телефону"""

    name, phone, *_ = args
    if Phone(phone):
        if not book.find(name):
            p = Record(name)
            p.add_phone(phone)
            book.add_record(p)
            print("Phone added")
        elif not book.find(name)[0]:
            book.find(name) [0].append(phone)
            print("Phone added")
        else: 
            book.find(name)[0][0] = phone
            print("Phone updated.")
            print(book)
        
    else: raise ValueError


@input_error
def change_contact(args: list, book: AddressBook):
    """Функція для заміни старого номера телефона на новий"""

    name, phone, *_ = args
    if book.find(name):
        book.find(name)[0][0] = Phone(phone)
    print("Contact updated")


@input_error
def show_phone(args:list, book: AddressBook):
    """Функція показує номер телефона за ім'ям, отриманим із запиту"""
    name = args[0]
    if book.find(name):
        print(book.find(name)[0][0])
    else: raise KeyError


@input_error
def show_all(book: AddressBook):
    """Виведення всіх імен та номерів телефонів у книзі контактів"""
    if book:
        for k in book:
            print(f"{k}: {book[k][0][0]}")
    else: print("Contacts list is empty")


@input_error
def delete_contact(args:list, book: AddressBook):
    """"Функція для видалення контакту за ім'ям."""
    book.delete(args[0])
    print("Contact deleted")   
            

@input_error
def add_birthday(args, book: AddressBook):
    """Функція для додавання дня народження. Якщо контакт (ім'я) є у книзі контактів, день народження додається до існуючого контакту;
    якщо імені немає у книзі - створюється новий контакт"""
    name, birthday, *_ = args
    if book.find(name):
        book[Record(name).name.value].append(birthday)
        print(book)

        print("Birthday added")
    else:
        record = Record(name)
        record.add_birthday(birthday)
        book.add_record(record)
        print(book)
        print("Birthday added")

@input_error
def show_birthday(args: list, book: AddressBook):
    """"Виведення дати народження за вказаним ім'ям"""

    name = args[0].title()
    if name in book:
        print(book[name][-1])
    else: print("No birthday record found for this contact.")


@input_error
def birthdays(book: AddressBook): 
    """Функція для виведення імен та дат народження з книги контактів, що випадають на найближчі 7 днів."""
    for bd in book.get_upcoming_birthdays():
        print(bd)


def save_data(book: AddressBook, filename: str):
    """Функція для збереження даних для книги контактів, отриманих під час роботи застосунку"""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str):
    """Функція для завантаження даних з книги контактів, збереженої у форматі pickle"""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 


if __name__ == "__main__":
    pass

