"""Основний скрипт для запуску бота з командного рядка. Використовує команди з модуля commands та книгу контактів класу Addressbook з модуля phonebook"""
from phonebook import AddressBook #, Record
from commands import parse_input, add_contact, change_contact, show_phone, delete_contact, add_birthday, show_birthday, birthdays, show_all
from commands import load_data, save_data

def main(*args, **kwargs):

    filename="addressbook.pkl"
    book = load_data(filename)

    while True:
        user_input = input("Enter your request: ")
        if parse_input(user_input):
            command, *args = parse_input(user_input)

            if command in ("hello", "hi"):                  #terminal command: hi / hello
                print("Hi. How may I help you?")
            elif command == "add":                          #terminal command example: add John 1234567890
                add_contact(args, book)
            elif command in ("change", "update", "edit"):   #terminal command example: change John 0555333888
                change_contact(args, book)
            elif command == "show":                         #terminal command example: show john
                show_phone(args, book)
            elif command == "all":                                                          #terminal command: all
                print("Type 'all' to check all contacts list") if args else show_all(book)
            elif command in ("delete", "remove"):                                           #terminal command example: delete John
                delete_contact(args, book)
            elif command == "add-birthday":                 #terminal command example: add-birthday John 08.08.2000
                add_birthday(args, book)
            elif command == "show-birthday":                #terminal command example: show-birthday John
                show_birthday(args, book)
            elif command == "birthdays":                    #terminal command: birthdays
                birthdays(book)
            elif command in ("close", "exit", "quit", "q"):   #terminal commands: close / exit / quit / q
                print("Bye!")
                save_data(book, filename)
                break
            else: print("Invalid command", command)
        else: print("Cannot read inputed request. Please try again.")


if __name__ == "__main__":
    main()