#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OracleDB Viewer, A GUI for Oracle Database
Copyright (C) 2021  Ali Zaidi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk
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
        self.hostLabel = ttk.Label(container, text='Host')
        self.hostLabel.pack(side='top', anchor='nw')
        self.hostEntry = ttk.Entry(container, textvariable=self.host, width=40)
        self.hostEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.portLabel = ttk.Label(container, text='Port')
        self.portLabel.pack(side='top', anchor='nw')
        self.portEntry = ttk.Entry(container, textvariable=self.port, width=40)
        self.portEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.sidLabel = ttk.Label(container, text='SID')
        self.sidLabel.pack(side='top', anchor='nw')
        self.sidEntry = ttk.Entry(container, textvariable=self.sid, width=40)
        self.sidEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.usernameLabel = ttk.Label(container, text='Username')
        self.usernameLabel.pack(side='top', anchor='nw')
        self.usernameEntry = ttk.Entry(container, textvariable=self.username, width=40)
        self.usernameEntry.pack(side='top')

        container = tk.Frame(body)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        self.passwordLabel = ttk.Label(container, text='Password')
        self.passwordLabel.pack(side='top', anchor='nw')
        self.passwordEntry = ttk.Entry(container, show='*', textvariable=self.password, width=40)
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
        self.connectBtn = ttk.Button(self, text='Connect', width=10, state=tk.DISABLED, command=self.connectBtnHandler)
        self.connectBtn.pack(side='left', padx=5, pady=5)

        # Add cancel button
        cancel_button = ttk.Button(self, text='Cancel', width=10, command=self.destroy)
        cancel_button.pack(side='right', padx=5, pady=5)

        # Bind keyboard events
        self.bind('<Return>', lambda event: self.connectBtnHandler if self.connectBtn.cget('state') == 'normal' else None)
        self.bind('<Escape>', lambda event: self.destroy)
