import tkinter as tk

from ConnectionDialog import ConnectionDialog
from MenuBar import MenuBar
from Notebook import Notebook
from Sidebar import Sidebar
from Table import Table

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
        self.initializeNotebook()
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

    def initializeNotebook(self):
        # Create the notebook
        self.notebook = Notebook(self)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def updateUI(self, dbState=None):
        if dbState is None:
            dbState = self.db.isConnected
        # Update the menu items
        self.menuBar.updateMenuItems(dbState)
        # Update the sidebar
        self.sidebar.update(dbState)

    def openTable(self, tableName, sqlQuery, editable=False):
        # Execute the query
        self.db.cursor.execute(sqlQuery)
        # Get column names
        columnNames = [column[0] for column in self.db.cursor.description]
        # Get the data
        data = self.db.cursor.fetchall()

        # Create a new table tab
        tableTab = Table(self.notebook, tableName, editable, data=data)
        # Set column names
        tableTab.headers(columnNames)
        # Add the table tab to the notebook
        self.notebook.addTab(tableName, tableTab)

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
