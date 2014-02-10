import wx
import wartarge
import PyQt4
from array import array

#following imports needed to run Py2exe
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4.QtWebKit import *
 
########################################################################
#   This Panel handels the login for Eve Gate
########################################################################
class LoginPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
       
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        loginText = wx.StaticText(self, label='Please Login to Eve Gate')
        hbox0.Add(loginText, flag=wx.BOTTOM, border=10)
        vbox.Add(hbox0, flag=wx.ALIGN_CENTER|wx.TOP|wx.RIGHT|wx.LEFT, border=10)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        usernameLabel = wx.StaticText(self, label='Username:')
        hbox1.Add(usernameLabel, flag=wx.RIGHT|wx.TOP, border=3)
        self.usernameTextBox = wx.TextCtrl(self)
        hbox1.Add(self.usernameTextBox, proportion=1)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        passwordLabel = wx.StaticText(self, label='Password:')
        hbox2.Add(passwordLabel, flag=wx.RIGHT|wx.TOP, border=3)
        self.passwordTextBox = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        hbox2.Add(self.passwordTextBox, proportion=1)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER| wx.ALL, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.loginButton = wx.Button(self, label='Login')
        hbox3.Add(self.loginButton, flag=wx.ALL, border = 10)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER)

        self.SetSizer(vbox)
 
########################################################################
#   This Panel handels adding the Corp/Alliance to the watchlist
########################################################################
class ContactPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.dropBox = wx.ComboBox(self, choices = ['Corporation', 'Alliance'], style=wx.CB_READONLY, value='Corporation')
        hbox0.Add(self.dropBox)
        vbox.Add(hbox0, flag=wx.ALIGN_CENTER|wx.ALL, border = 10)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        contactLable = wx.StaticText(self, label="Corp/Alliance Name:")
        hbox1.Add(contactLable, flag=wx.RIGHT|wx.TOP, border=3)
        self.contactNameBox = wx.TextCtrl(self, size=(150, 25), style=wx.TE_PROCESS_ENTER)
        hbox1.Add(self.contactNameBox, proportion = 1)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER|wx.ALL, border = 10)


        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.addButton = wx.Button(self, label='Add to Watch List')
        self.stopButton = wx.Button(self, label='Stop')
        hbox3.Add(self.addButton, flag=wx.ALL, border = 10)
        hbox3.Add(self.stopButton, flag=wx.ALL, border = 10)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER)
        self.stopButton.Disable()


        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 0 ) 
        
        hbox4.Add(self.m_gauge1, flag=wx.ALL, border = 10)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER)
        self.m_gauge1.Disable()


        self.SetSizer(vbox)
 
########################################################################
#   The Main window of the program, contains all frames and widgets
########################################################################
class MainFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,"Wartarge", size=(600,300))

        self.Center()
 
        #Create the panels
        self.loginPanel = LoginPanel(self)
        self.contactPanel = ContactPanel(self)  
        self.contactPanel.Hide()
    
        #Create the sizer for the panels
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.loginPanel, 1, wx.EXPAND)
        self.sizer.Add(self.contactPanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
 
        #Create the Menue Bar 
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        self.m_statusBar1.SetFieldsCount(2)
        self.m_statusBar1.SetStatusWidths([-1, -2])
        self.m_statusBar1.SetStatusText('Ready', 0)

        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY, "Log Out", "Log out of current character")
        about_menu_item = fileMenu.Append(wx.ID_ANY, "About", "What the hell is this shit?")
        self.Bind(wx.EVT_MENU, self.onLogOut, switch_panels_menu_item)
        self.Bind(wx.EVT_MENU, self.onAbout, about_menu_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        #Setup events for the panels
        self.loginPanel.loginButton.Bind(wx.EVT_BUTTON, self.onLogin) #Login Button
        self.contactPanel.addButton.Bind(wx.EVT_BUTTON, self.onAddWatchList) #Add Watch List Button
        self.contactPanel.stopButton.Bind(wx.EVT_BUTTON, self.onStopAddWatchList)
 
    #----------------------------------------------------------------------
    def onLogOut(self, event):
        if self.loginPanel.IsShown():
            self.loginPanel.usernameTextBox.Clear()
            self.loginPanel.passwordTextBox.Clear()
            self.m_statusBar1.SetStatusText('Logged Out', 0)
        else:
            self.loginPanel.Show()
            self.contactPanel.Hide()
            self.loginPanel.usernameTextBox.Clear()
            self.loginPanel.passwordTextBox.Clear()
            self.m_statusBar1.SetStatusText('Logged Out', 0)
        self.Layout()

    def onAbout(self, event):
        info = wx.AboutDialogInfo()

        info.SetName('Wartarge')
        info.SetDescription('A simple scritp to add contacts to you watchlist \n create by: trumpet7347 and Roriii')

        wx.AboutBox(info)


    def onLogin(self, event):
        username = self.loginPanel.usernameTextBox.GetValue()
        password = self.loginPanel.passwordTextBox.GetValue()

        self.loginPanel.loginButton.Disable()
        try:
            self.m_statusBar1.SetStatusText('Please wait, Logging in...', 0)
            wartarge.loginEveGate(username, password)
            self.m_statusBar1.SetStatusText('Hi ' + username, 0)

            self.loginPanel.loginButton.Enable()

            self.loginPanel.Hide()
            self.contactPanel.Show()
            self.Layout()
            self.Refresh()

        except:
            self.m_statusBar1.SetStatusText('ERROR: unable to login', 0)
            self.loginPanel.loginButton.Enable()
                

    def onStopAddWatchList(self, event):
        self.stoppingAddWatchList = True


    def onAddWatchList(self, event):
        self.stoppingAddWatchList = False
        
        contactType = self.contactPanel.dropBox.GetValue()
        contactName = self.contactPanel.contactNameBox.GetValue()
        
        self.contactPanel.addButton.Disable()
        self.contactPanel.stopButton.Enable()

        self.m_statusBar1.SetStatusText('Looking up: ' + contactType + ' - ' + contactName, 1)

        contactID = 0

        try:
            if contactType == 'Alliance':
                contactID = wartarge.getAllianceId(contactName)
            else:
                contactID = wartarge.getCorpId(contactName)
        except:
            self.m_statusBar1.SetStatusText('Error looking up ' + contactName, 1)
            return

        if contactID == 0:
            self.m_statusBar1.SetStatusText('Can\'t find ' + contactName, 1)
        else:

            self.m_statusBar1.SetStatusText('Getting members list for ' + contactName, 1)
            print "ID: " + contactID


            labelID = wartarge.createNewLable(contactName)
            print 'LabelID: ' + labelID
            #return

            try:
                #allilist
                if contactType == 'Alliance':
                    members = wartarge.getMemberList('allilist', contactID)
                else:
                    members = wartarge.getMemberList('corplist', contactID)


                self.contactPanel.m_gauge1.SetRange(len(members))
                self.contactPanel.m_gauge1.SetValue(1)
                self.contactPanel.m_gauge1.Enable()


                dlg = wx.MessageDialog(self,
                    "You are about to add " + str(len(members)) + " pilots to your watchlist, continue?",
                    "Confirm Add", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()

                if result != wx.ID_OK:
                    return


                y = 0
                for x in range (1, len(members)+1):

                    if self.stoppingAddWatchList == True:
                        break

                    self.m_statusBar1.SetStatusText('Adding %s to contact list' %(members[x]), 1)
                    wartarge.addContact(members[x])
                    self.contactPanel.m_gauge1.SetValue(x)

                    y = y + 1
                    if y >= 5 :
                        print 'Moving Neutral Contacts to a new label'
                        try:
                            wartarge.moveToLabel(contactName, labelID)
                        except:
                            print 'Prolly a time out moving to label... FUCK'

                        y = 1

                wartarge.moveToLabel(contactName, labelID)
                self.contactPanel.m_gauge1.Disable()
                if self.stoppingAddWatchList == False:
                    self.m_statusBar1.SetStatusText('Fished adding ' + contactName, 1)
                else:
                    self.m_statusBar1.SetStatusText('Cancelled', 1)

            except Exception as inst:
                 self.m_statusBar1.SetStatusText('Error looking up members...', 1)
                 self.contactPanel.m_gauge1.Disable()
                 print inst


        
        self.stoppingAddWatchList = False
        self.contactPanel.addButton.Enable()
        self.contactPanel.stopButton.Disable()

 
 
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

