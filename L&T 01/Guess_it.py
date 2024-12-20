import random


def get_first_number():
    value_1 = int(input("Gebe die kleinere Zahl der Reichweite an: "))
    return value_1


def get_second_number():
    value_2 = int(input("Gebe die größer Zahl der Reichweite an: "))
    return value_2


def reichweite(value_1, value_2):
    secret_num = random.randint(value_1, value_2)
    return secret_num


def game(secret_num):
    game_won = False
    while not game_won:
        guess = int(input("Errate die von mir ausgedachte Zahl:\n"))
        if guess == secret_num:
            print(f"Glückwunsch du hast die Zahl {secret_num} erraten.")
            game_won = True
        elif guess > secret_num:
            print("Du bist drüber!")
        elif guess < secret_num:
            print("Du bist drunter!")


secret_num = reichweite(get_first_number(), get_second_number())
game(secret_num)
