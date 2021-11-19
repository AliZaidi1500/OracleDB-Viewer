import tkinter as tk

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("OracleDB Viewer")
        self.geometry("800x600")

        # Create the menu bar
        menuBar = tk.Menu(self)

        # Database Menu
        databaseMenu = tk.Menu(menuBar, tearoff=0)
        databaseMenu.add_command(label="Connect", command=self.connect)
        databaseMenu.add_command(label="Disconnect", command=self.disconnect, state=tk.DISABLED)
        databaseMenu.add_separator()
        databaseMenu.add_command(label="Exit", command=self.destroy)

        # Add database menu to menu bar
        menuBar.add_cascade(label="Database", menu=databaseMenu)
        self.config(menu=menuBar)

    def connect(self):
        pass

    def disconnect(self):
        pass

if __name__ == '__main__':
    app = App()
    app.mainloop()
