import database
import gui
import wx

class MyDialog1(gui.MyDialog1):
    def __init__(self, parent):
        super().__init__(parent)

class MyFrame1(gui.MyFrame1):
    def __init__(self, parent, database):
        super().__init__(parent)

        self.database = database.Database()

        self.m_listCtrl1.InsertColumn(0, 'Name')
        self.m_listCtrl1.InsertColumn(1, 'Preis')

        self.update_list_data()

    def update_list_data(self):
        self.m_listCtrl1.DeleteAllItems()

        for obst in self.database.get_all_obst():
            werte = [obst.name, obst.preis]
            index = self.m_listCtrl1.Append(werte)
            self.m_listCtrl1.SetItemData(index, obst.id)

    def delete_button( self, event ):
        if self.m_listCtrl1.GetItemCount() == 1:
            selected = self.m_listCtrl1.GetFirstSelected()
            obst_id = self.m_listCtrl1.GetItemData(selected)

            self.database.delete_obst(obst_id)
            self.update_list_data()

    def got_to_add_dialog(self, event):
        dlg = MyDialog1(self)

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.m_textCtrl1_Name.GetValue()
            preis = dlg.m_textCtrl2_preis.GetValue()

            self.database.add_obst(name, float(preis))
            self.update_list_data()

        dlg.Destroy()

    def go_to_edit( self, event ):
        if self.m_listCtrl1.GetItemCount() == 1:
            selected = self.m_listCtrl1.GetFirstSelected()
            obst_id = self.m_listCtrl1.GetItemData(selected)
            obst = self.database.get_obst_by_id(obst_id)
            dlg = MyDialog1(self)

            dlg.m_textCtrl1_Name.SetValue(obst.name)
            dlg.m_textCtrl2_preis.SetValue(str(obst.preis))

            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.m_textCtrl1_Name.GetValue()
                preis = dlg.m_textCtrl2_preis.GetValue()

                self.database.edit_obst(obst_id, name, float(preis))
                self.update_list_data()
            dlg.Destroy()



if __name__ == "__main__":
    app = wx.App()
    frm = MyFrame1(None, database=database)
    frm.Show()
    app.MainLoop()