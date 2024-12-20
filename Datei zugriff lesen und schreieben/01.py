import os


Dateiordner = input(str("Gebe den gewünschten Dateipfad an, für welchen eine Dateistatistik erstellt werden soll: "))
Dateiendung_dict = {}
leere_ordner = []
count = 0
for root, dirs, files in os.walk(Dateiordner):

    print(root)

    print(dirs)

    print(files)
    print()
    if len(dirs) == 0:
        leere_ordner.append(root)
        count += 1
    for file in files:
        head = os.path.split(file)[1]
        hi = head.index(".")
        head = head[hi:]
        if head in Dateiendung_dict:
            Dateiendung_dict[head] += 1
        else:
            Dateiendung_dict.update({head: 1})

sorted_dict = dict(sorted(Dateiendung_dict.items(), key=lambda item: item[1], reverse=True))

print(Dateiendung_dict)
print(sorted_dict)
print(f"Es gibt {count} leere Ordner. das sind die Pfade zu den genannten Ordnern {leere_ordner}")
