import tkinter as tk
import tkinter.ttk as ttk

from OracleDatabase import OracleDatabase
from ConnectionDialog import ConnectionDialog

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
        self.sidebar = tk.Frame(self, width=200, bg='white')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(0)
        # Create the sidebar header
        self.sidebarHeader = tk.Label(self.sidebar, bg='white')
        self.sidebarHeader.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        # Create the sidebar body treeview
        self.sidebarBody = ttk.Treeview(self.sidebar, show='tree', selectmode='none')
        self.sidebarBody.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Add data to the treeview
        self.sidebarBody.insert('', tk.END, text='Tables', iid='tables', open=False)
        self.sidebarBody.insert('', tk.END, text='Views', iid='views', open=False)
        # Create the sidebar footer
        self.sidebarFooter = tk.Label(self.sidebar, bg='white')
        self.sidebarFooter.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def updateUI(self, dbState=None):
        if dbState is None:
            dbState = self.db.isConnected
        # Update the database menu
        self.updateDatabaseMenuItems(dbState)
        # Update the sidebar
        self.updateSidebar(dbState)

    def updateDatabaseMenuItems(self, dbState):
        # Update the menu items
        self.databaseMenu.entryconfig(0, state=tk.NORMAL if not dbState else tk.DISABLED)
        self.databaseMenu.entryconfig(1, state=tk.NORMAL if dbState else tk.DISABLED)

    def updateSidebar(self, dbState):
        # Update the header
        self.sidebarHeader.config(
            text=f'Connected to {self.db.host} as {self.db.username}'
                if dbState else 'Not connected')
        # Update the body
        self.updateSidebarBody(dbState)
        # Update the footer
        self.sidebarFooter.config(
            text=f'Oracle Version: {self.db.version}' if dbState else 'Oracle Version:')

    def updateSidebarBody(self, dbState):
        # Clear treeview data
        for (i, child) in enumerate(self.sidebarBody.get_children()):
            for (i, child) in enumerate(self.sidebarBody.get_children(child)):
                self.sidebarBody.delete(child)

        # Add data to the treeview if database is connected
        if dbState:
            # Add tables to the treeview
            for table in self.db.getTables():
                self.sidebarBody.insert('tables', tk.END, text=table, open=False)
            # Add views to the treeview
            for view in self.db.getViews():
                self.sidebarBody.insert('views', tk.END, text=view, open=False)

    def showConnectionDialog(self):
        # Create a connection dialog and show it
        connectionDialog = ConnectionDialog(self)
        connectionDialog.mainloop()

    def connect(self, host, port, sid, username, password):
        try:
            # Connect to the database
            self.db.connect(host, port, sid, username, password)
            # Update the UI
            self.updateUI()
            return True
        # Handle errors
        except Exception as e:
            return str(e)

    def disconnect(self):
        # Disconnect from the database if connected
        if self.db.isConnected:
            self.db.disconnect()
            # Update the UI
            self.updateUI()

if __name__ == '__main__':
    app = App()
    app.mainloop()
