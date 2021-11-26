import tkinter as tk

from MenuBar import MenuBar
from Sidebar import Sidebar
from ConnectionDialog import ConnectionDialog

from OracleDatabase import OracleDatabase

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
        self.menuBar = MenuBar(self)
        # Add menu bar to the main window
        self.config(menu=self.menuBar)

    def initializeSidebar(self):
        # Create the sidebar
        self.sidebar = Sidebar(self, width=200, bg='white')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

    def updateUI(self, dbState=None):
        if dbState is None:
            dbState = self.db.isConnected
        # Update the menu items
        self.menuBar.updateMenuItems(dbState)
        # Update the sidebar
        self.sidebar.update(dbState)

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
