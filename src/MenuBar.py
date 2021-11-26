import tkinter as tk

class MenuBar(tk.Menu):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Initialize the menu
        self.initalizeMenu()

    def initalizeMenu(self):
        # Create the database menu and add entries
        self.databaseMenu = tk.Menu(self, tearoff=0)
        self.databaseMenu.add_command(label='Connect', command=self.parent.showConnectionDialog)
        self.databaseMenu.add_command(label='Disconnect', command=self.parent.disconnect)
        self.databaseMenu.add_separator()
        self.databaseMenu.add_command(label='Exit', command=self.parent.destroy)
        # Add database menu to menu bar
        self.add_cascade(label='Database', menu=self.databaseMenu)

    def updateMenuItems(self, dbState):
        # Update the database menu items
        self.databaseMenu.entryconfig(0, state=tk.NORMAL if not dbState else tk.DISABLED)
        self.databaseMenu.entryconfig(1, state=tk.NORMAL if dbState else tk.DISABLED)
