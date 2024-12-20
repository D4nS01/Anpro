import os


def check_if_path_exists(path):
    return os.path.exists(path)


def check_file_name(file_name):
    return os.path.isfile(file_name)


def get_file_name_from_input():
    file_name = input("Nennen Sie den Dateinamen: ")
    while check_file_name(file_name) is False:
        print("Diese Datei existiert nicht!")
        file_name = input("Nennen Sie den Dateinamen: ")
    return file_name


def get_file_size(file_name):
    return os.path.getsize(file_name)


def print_file_size(file_name):
    file_size = get_file_size(file_name)
    print(f"Die Datei hat eine Größe von {file_size} kb!")


def get_tail_and_head(file_name):
    tail, head = os.path.split(file_name)
    return tail, head


def get_file_head(file_name):
    head = os.path.split(file_name)[1]
    return head


def get_file_tail(file_name):
    tail = os.path.split(file_name)[0]
    return tail


def print_head_and_tail(file_name):
    print(f"Tail: {get_file_tail(file_name)}")
    print(f"Head: {get_file_head(file_name)}")


def get_file_name_ending(file_name):
    head = get_file_head(file_name)
    ending = head.split(".")[-1]
    return ending


def get_file_base_name(file_name):
    head = get_file_head(file_name)
    base_name_parts = head.split(".")[0:-1]   # file_name could have more than one '.' char
    base_name = ".".join(base_name_parts)    # joins elements from the list to a single string
    return base_name


def print_file_base_name(file_name):
    print(f"Basename: {get_file_base_name(file_name)}")


def print_file_name_extension(file_name):
    print(f"Dateiendung: {get_file_name_ending(file_name)}")


def print_file_base_name_and_file_ending(file_name):
    print_file_base_name(file_name)
    print_file_name_extension(file_name)


def print_menu():
    print()
    print("Wählen Sie eine Option")
    print("1: Dateipfad eingeben")
    print("2: Dateigröße ausgeben")
    print("3: Head und Tail anzeigen")
    print("4: Dateiendung ausgeben")
    print("5: Programm beenden")


def get_user_input():
    while True:
        print_menu()
        user_input = input()
        if user_input in ("1", "2", "3", "4", "5"):
            return int(user_input)


def main():
    path = get_file_name_from_input()
    while True:
        user_input = get_user_input()
        if user_input == 1:
            path = get_file_name_from_input()
        elif user_input == 2:
            print_file_size(path)
        elif user_input == 3:
            print_head_and_tail(path)
        elif user_input == 4:
            print_file_base_name_and_file_ending(path)
        elif user_input == 5:
            print("Auf Wiedersehen!")
            break


main()
