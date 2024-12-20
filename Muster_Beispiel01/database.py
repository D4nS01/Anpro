"""
Datenbankabstraktion mit sqlobject
"""
from typing import List

import sqlobject as so


class Artikel(so.SQLObject):
    name = so.StringCol()
    regalnummer = so.IntCol()
    beschreibung = so.StringCol()
    datum = so.DateCol()
    bereich = so.StringCol()


class Database:
    def __init__(self, filename="maindb.sqlite"):
        so.sqlhub.processConnection = so.connectionForURI(f"sqlite:{filename}")  # "sqlite:maindb.sqlite"
        Artikel.createTable(ifNotExists=True)

    def get_all_articles(self):
        return Artikel.select()

    # Diese Methode ist für die main.py nicht notwendig.
    # Sie wird genutzt, wenn diese Datei ausgeführt wird. Siehe unten
    def get_all_articles_as_str(self) -> List[str]:
        return [e.text for e in self.get_all_articles()]

    def add_article(self, name: str, regalnummer: int, beschreibung: str, datum: str, bereich: str) -> None:
        Artikel(name=name,
                regalnummer=regalnummer,
                beschreibung=beschreibung,
                datum=datum,
                bereich=bereich)  # new article

    def delete_article(self, article_id: int):
        Artikel.delete(article_id)

    def get_article_by_id(self, article_id: int):
        return Artikel.get(article_id)

    def get_next_id(self):
        all_articles = list(Artikel.select())  # list(self.get_all_articles())
        if all_articles:
            last_article_id = all_articles[-1].id
            return int(last_article_id)+1
        else:
            return 1


if __name__ == "__main__":
    db = Database()
    print(db.get_all_articles_as_str())
