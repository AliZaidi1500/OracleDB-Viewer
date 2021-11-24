import tkinter as tk

from OracleDatabase import OracleDatabase
from ConnectionDialog import ConnectionDialog
from Sidebar import Sidebar

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Create the database object
        self.db = OracleDatabase()

        # Initialize the application
        self.initializeApplication()

    def initializeApplication(self):
        self.initializeMainWindow()
        self.initializeSidebar()
        self.updateUI()

    def initializeMainWindow(self):
        self.title('OracleDB Viewer')
        self.geometry('800x600')

        # Create the menu bar
        menuBar = tk.Menu(self)

        # Create the database menu and add entries
        self.databaseMenu = tk.Menu(menuBar, tearoff=0)
        self.databaseMenu.add_command(label='Connect', command=self.showConnectionDialog)
        self.databaseMenu.add_command(label='Disconnect', command=self.disconnect)
        self.databaseMenu.add_separator()
        self.databaseMenu.add_command(label='Exit', command=self.destroy)

        # Add database menu to menu bar
        menuBar.add_cascade(label='Database', menu=self.databaseMenu)
        self.config(menu=menuBar)

    def initializeSidebar(self):
        # Create the sidebar
        self.sidebar = Sidebar(self, width=200, bg='white')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

    def updateUI(self, dbState=None):
        if dbState is None:
            dbState = self.db.isConnected
        # Update the database menu
        self.updateDatabaseMenuItems(dbState)
        # Update the sidebar
        self.sidebar.update(dbState)

    def updateDatabaseMenuItems(self, dbState):
        # Update the menu items
        self.databaseMenu.entryconfig(0, state=tk.NORMAL if not dbState else tk.DISABLED)
        self.databaseMenu.entryconfig(1, state=tk.NORMAL if dbState else tk.DISABLED)

    def showConnectionDialog(self):
        # Create a connection dialog and show it
        connectionDialog = ConnectionDialog(self)
        connectionDialog.mainloop()

    def connect(self, host, port, sid, username, password):
        try:
            # Connect to the database
            self.db.connect(host, port, sid, username, password)
        # Handle connection errors
        except Exception as e:
            return str(e)

        # Update the UI
        self.updateUI()

        return True

    def disconnect(self):
        # Disconnect from the database if connected
        if self.db.isConnected:
            self.db.disconnect()
            # Update the UI
            self.updateUI()

if __name__ == '__main__':
    app = App()
    app.mainloop()
