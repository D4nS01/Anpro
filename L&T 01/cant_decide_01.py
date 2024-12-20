from random import choice

data = []

while True:
    titel = str(input("Film Titel: "))
    data.append(titel)
    wahl = input("noch einen hinzufügen? (y/n): ")
    if wahl == "n" or wahl == "N":
        break


print(choice(data))
