import sqlobject as so

class Obstkorb(so.SQLObject):
    name = so.StringCol()
    preis = so.FloatCol()

class Database:
    def __init__(self):
        so.sqlhub.processConnection = so.connectionForURI('sqlite:mydata.sqlite')
        Obstkorb.createTable(ifNotExists=True)

    def get_all_obst(self):
        return Obstkorb.select()

    def get_all_obst_as_list(self):
        return list(Obstkorb.select())

    def get_obst_by_id(self, id):
        return Obstkorb.get(id=id)

    def delete_obst(self, id):
        Obstkorb.delete(id=id)

    def add_obst(self, name, preis):
        Obstkorb(name=name, preis=preis)

    def edit_obst(self, id, name, preis):
        OT = self.get_obst_by_id(id)
        OT.name = name
        OT.preis = preis

if __name__ == "__main__":
    db = Database()