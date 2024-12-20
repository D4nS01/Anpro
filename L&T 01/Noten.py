def get_percentage():
    percentage = float(input("Geben sie die im Test erhaltenen Prozentzahl an:\n"))
    return percentage


def percentage_to_grade(percentage):
    if percentage > 84.99:
        grade = 1
    elif 72.99 < percentage < 85:
        grade = 2
    elif 58.99 < percentage < 73:
        grade = 3
    elif 44.99 < percentage < 59:
        grade = 4
    elif 26.99 < percentage < 45:
        grade = 5
    else:
        grade = 6
    return grade


def get_grade(grade0, percentage0):
    print(f"Aus dem angegebenen Prozentwert {percentage0}% ergibt sich die Note {grade0}")


percentage0 = get_percentage()
grade0 = percentage_to_grade(percentage0)
get_grade(grade0, percentage0)
