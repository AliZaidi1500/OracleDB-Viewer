import tkinter as tk
import cx_Oracle as cx

from ConnectionDialog import ConnectionDialog

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.db = None

        self.initializeMainWindow()

    def initializeMainWindow(self):
        self.title("OracleDB Viewer")
        self.geometry("800x600")

        # Create the menu bar
        menuBar = tk.Menu(self)

        # Create the database menu and add entries
        self.databaseMenu = tk.Menu(menuBar, tearoff=0)
        self.databaseMenu.add_command(label="Connect", command=self.showConnectionDialog)
        self.databaseMenu.add_command(label="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.databaseMenu.add_separator()
        self.databaseMenu.add_command(label="Exit", command=self.destroy)

        # Add database menu to menu bar
        menuBar.add_cascade(label="Database", menu=self.databaseMenu)
        self.config(menu=menuBar)

    def showConnectionDialog(self):
        # Create a connection dialog and show it
        connectDialog = ConnectionDialog(self)
        connectDialog.mainloop()

    def updateDatabaseMenuItems(self, dbState):
        # Update the database menu item states
        self.databaseMenu.entryconfig(0, state=tk.NORMAL if not dbState else tk.DISABLED)
        self.databaseMenu.entryconfig(1, state=tk.NORMAL if dbState else tk.DISABLED)

    def connect(self, host, port, sid, username, password):
        # Connect to the database
        try:
            self.db = cx.connect(username, password, cx.makedsn(host, port, sid))
            # Update the database menu
            self.updateDatabaseMenuItems(True)
            return True
        # Handle errors
        except cx.DatabaseError as e:
            return str(e)

    def disconnect(self):
        # Disconnect from the database if connected
        if self.db:
            self.db.close()
            self.db = None
            # Update the database menu
            self.updateDatabaseMenuItems(False)

if __name__ == '__main__':
    app = App()
    app.mainloop()
