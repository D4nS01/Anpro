# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		gSizer1 = wx.GridSizer( 6, 2, 0, 0 )

		self.m_staticTextArtikelnummer = wx.StaticText( self, wx.ID_ANY, u"Artikelnummer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextArtikelnummer.Wrap( -1 )

		gSizer1.Add( self.m_staticTextArtikelnummer, 0, wx.ALL, 5 )

		self.m_textCtrlArtikelnummer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_textCtrlArtikelnummer.Enable( False )

		gSizer1.Add( self.m_textCtrlArtikelnummer, 0, wx.ALL, 5 )

		self.m_staticTextDatum = wx.StaticText( self, wx.ID_ANY, u"Datum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextDatum.Wrap( -1 )

		gSizer1.Add( self.m_staticTextDatum, 0, wx.ALL, 5 )

		self.m_textCtrlDatum = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_textCtrlDatum.Enable( False )

		gSizer1.Add( self.m_textCtrlDatum, 0, wx.ALL, 5 )

		self.m_staticTextName = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextName.Wrap( -1 )

		gSizer1.Add( self.m_staticTextName, 0, wx.ALL, 5 )

		self.m_textCtrlName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer1.Add( self.m_textCtrlName, 0, wx.ALL, 5 )

		self.m_staticTextRegalnummer = wx.StaticText( self, wx.ID_ANY, u"Regalnummer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextRegalnummer.Wrap( -1 )

		gSizer1.Add( self.m_staticTextRegalnummer, 0, wx.ALL, 5 )

		self.m_textCtrlRegalnummer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer1.Add( self.m_textCtrlRegalnummer, 0, wx.ALL, 5 )

		self.m_staticTextBeschreibung = wx.StaticText( self, wx.ID_ANY, u"Beschreibung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBeschreibung.Wrap( -1 )

		gSizer1.Add( self.m_staticTextBeschreibung, 0, wx.ALL, 5 )

		self.m_textCtrlBeschreibung = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer1.Add( self.m_textCtrlBeschreibung, 0, wx.ALL, 5 )

		self.m_staticText_Bereich= wx.StaticText( self, wx.ID_ANY, u"Bereich", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_Bereich.Wrap( -1 )

		gSizer1.Add( self.m_staticText_Bereich
		, 0, wx.ALL, 5 )

		self.m_textCtrlBereich = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		gSizer1.Add( self.m_textCtrlBereich, 0, wx.ALL, 5 )


		bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )

		self.m_buttonAbschicken = wx.Button( self, wx.ID_ANY, u"Abschicken", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_buttonAbschicken, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Anzeigen", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button2, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.setAutomaticValues )
		self.m_buttonAbschicken.Bind( wx.EVT_BUTTON, self.addData )
		self.m_button2.Bind( wx.EVT_BUTTON, self.showAllData )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def setAutomaticValues( self, event ):
		event.Skip()

	def addData( self, event ):
		event.Skip()

	def showAllData( self, event ):
		event.Skip()


###########################################################################
## Class MenuBar
###########################################################################

class MenuBar ( wx.MenuBar ):

	def __init__( self ):
		wx.MenuBar.__init__ ( self, style = 0 )

		self.Options = wx.Menu()
		self.Info = wx.MenuItem( self.Options, wx.ID_ANY, u"Info", wx.EmptyString, wx.ITEM_NORMAL )
		self.Options.Append( self.Info )

		self.Quit = wx.MenuItem( self.Options, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
		self.Options.Append( self.Quit )

		self.Append( self.Options, u"Options" )


		# Connect Events
		self.Bind( wx.EVT_MENU, self.on_show_info, id = self.Info.GetId() )
		self.Bind( wx.EVT_MENU, self.on_qiut, id = self.Quit.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_show_info( self, event ):
		event.Skip()

	def on_qiut( self, event ):
		event.Skip()


###########################################################################
## Class InfoDialog
###########################################################################

class InfoDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 200,250 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, u"This is some Info about this app!\nYou can add new articles!\nYou can view a list of all articles contained in the stash!\nYou can also delete articels from the stash!\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText_info.Wrap( 150 )

		bSizer4.Add( self.m_staticText_info, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_button4 = wx.Button( self, wx.ID_OK, u"Close Window", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( bSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class ListFrame
###########################################################################

class ListFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer2.Add( self.m_listCtrl, 0, wx.ALL, 5 )

		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Entfernen", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button3, 0, wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button3.Bind( wx.EVT_BUTTON, self.deleteDataset )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def deleteDataset( self, event ):
		event.Skip()


