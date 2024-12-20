import Artikellager
import wx
import database
import datetime


class MyDialog(Artikellager.InfoDialog):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.SetTitle(title)


class Menubar(Artikellager.MenuBar):
    def __init__(self, parent):
        super().__init__()
        quit_id = self.Quit.GetId()
        info_id = self.Info.GetId()
        self.Bind(wx.EVT_MENU, self.close_window, id=quit_id)
        self.Bind(wx.EVT_MENU, self.show_info, id=info_id)
        self.parent = parent

    def close_window(self, event):
        # print("close")
        self.parent.Close()

    def show_info(self, event):
        # print("info")
        dlg = MyDialog(self.parent, "Info")
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()


class ArticleListFrame(Artikellager.ListFrame):
    def __init__(self, parent, parent_database):
        super().__init__(parent)
        self.database = parent_database
        self.article_list = self.m_listCtrl
        for i, item in enumerate(("artikelnummer", "name", "regalnummer", "beschreibung", "bereich", "datum")):
            self.article_list.InsertColumn(i, item)
        self.update_list_data()

    def update_list_data(self) -> None:
        all_data = self.database.get_all_articles()
        self.article_list.DeleteAllItems()
        for article in all_data:
            values = [article.id,
                      article.name,
                      article.regalnummer,
                      article.beschreibung,
                      article.bereich,
                      article.datum]
            index = self.article_list.Append(values)
            # self.article_list.SetItemData(index, article.id)

        self.article_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.article_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.article_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.article_list.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        self.article_list.SetColumnWidth(4, wx.LIST_AUTOSIZE)

        pass

    def deleteDataset(self, event):
        if self.article_list.GetSelectedItemCount() == 1:
            selected_item = self.article_list.GetFirstSelected()
            article_id = self.article_list.GetItemText(selected_item, 0)
            # article_id = self.article_list.GetItemData(selected_item)
            self.database.delete_article(article_id)
        self.update_list_data()
        pass


class MainFrame(Artikellager.MainFrame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.SetTitle(title)
        self.menu = Menubar(self)
        self.SetMenuBar(self.menu)
        self.database = database.Database("maindb.sqlite")  # MainFrame knows the database
        self.set_next_article_id()
        self.set_current_date()

    def addData(self, event):
        name = self.m_textCtrlName.GetValue()
        regalnummer = self.m_textCtrlRegalnummer.GetValue()
        bereich = self.m_textCtrlBereich.GetValue()
        beschreibung = self.m_textCtrlBeschreibung.GetValue()
        datum = self.m_textCtrlDatum.GetValue()
        entry_flag = True
        if not (name and bereich and beschreibung):
            entry_flag = False
        if not regalnummer.isdecimal():
            entry_flag = False
        if entry_flag:
            self.database.add_article(name, int(regalnummer), beschreibung, datum, bereich)
            self.reset_article_values()
        else:
            print("values missing")
        pass

    def reset_article_values(self):
        self.set_current_date()
        self.set_next_article_id()
        self.m_textCtrlName.SetValue("")
        self.m_textCtrlRegalnummer.SetValue("")
        self.m_textCtrlBeschreibung.SetValue("")
        self.m_textCtrlBereich.SetValue("")

    def showAllData(self, event):
        ArticleListFrame(self, self.database).Show()

    def set_next_article_id(self):
        next_id = str(self.database.get_next_id())
        self.m_textCtrlArtikelnummer.SetValue(next_id)

    def set_current_date(self):
        self.m_textCtrlDatum.SetValue(self.get_current_date())

    def get_current_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')


if __name__ == "__main__":
    app = wx.App()
    frm = MainFrame(None, title="Artikellager")
    frm.Show()
    app.MainLoop()
