import tkinter as tk
from tkinter.simpledialog import Dialog
from tkinter.messagebox import showinfo, showerror

class ConnectionDialog(Dialog):

    def __init__(self, parent):
        # Database connection variables
        self.host = tk.StringVar()
        self.port = tk.StringVar()
        self.sid = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # Add trace to the database connection variables
        self.host.trace('w', self.updateConnectBtnState)
        self.port.trace('w', self.updateConnectBtnState)
        self.sid.trace('w', self.updateConnectBtnState)
        self.username.trace('w', self.updateConnectBtnState)
        self.password.trace('w', self.updateConnectBtnState)

        # Initialize the dialog
        self.parent = parent
        super().__init__(parent, title='Connect to database')

    def body(self, master):
        # Create body container
        body = tk.Frame(master)
        body.pack(padx=5, pady=5)

        # Add text entries
        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.hostLabel = tk.Label(container, text='Host')
        self.hostLabel.pack(side='top', anchor='nw')
        self.hostEntry = tk.Entry(container, textvariable=self.host)
        self.hostEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.portLabel = tk.Label(container, text='Port')
        self.portLabel.pack(side='top', anchor='nw')
        self.portEntry = tk.Entry(container, textvariable=self.port)
        self.portEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.sidLabel = tk.Label(container, text='SID')
        self.sidLabel.pack(side='top', anchor='nw')
        self.sidEntry = tk.Entry(container, textvariable=self.sid)
        self.sidEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.usernameLabel = tk.Label(container, text='Username')
        self.usernameLabel.pack(side='top', anchor='nw')
        self.usernameEntry = tk.Entry(container, textvariable=self.username)
        self.usernameEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.passwordLabel = tk.Label(container, text='Password')
        self.passwordLabel.pack(side='top', anchor='nw')
        self.passwordEntry = tk.Entry(container, textvariable=self.password)
        self.passwordEntry.pack(side='top')

        return super().body(master)

    def updateConnectBtnState(self, *args):
        # Enable the connect button if all fields are filled
        if self.host.get() and self.port.get() and self.sid.get() and self.username.get() and self.password.get():
            self.connectBtn.config(state=tk.NORMAL)
        else:
            self.connectBtn.config(state=tk.DISABLED)

    def connectBtnHandler(self):
        # Connect to database
        dbStatus = self.parent.connect(
            self.host.get(),
            self.port.get(),
            self.sid.get(),
            self.username.get(),
            self.password.get())
        
        # If connection was successful, destroy the dialog
        if dbStatus == True:
            showinfo('Connection Successful',
                f'Successfully connected to the database.\nOracle Version: {self.parent.db.version}')
            self.destroy()
        else:
            showerror('Connection Error', f'An error occured while connecting to the database:\n"{dbStatus}"')

    def buttonbox(self):
        # Add connect button
        self.connectBtn = tk.Button(self, text='Connect', width=10, state=tk.DISABLED, command=self.connectBtnHandler)
        self.connectBtn.pack(side='left', padx=5, pady=5)

        # Add cancel button
        cancel_button = tk.Button(self, text='Cancel', width=10, command=self.destroy)
        cancel_button.pack(side='right', padx=5, pady=5)

        # Bind keyboard events
        self.bind('<Return>', lambda event: self.connectBtnHandler if self.connectBtn.cget('state') == 'normal' else None)
        self.bind('<Escape>', lambda event: self.destroy)
