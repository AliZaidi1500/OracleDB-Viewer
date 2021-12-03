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

from ConnectionDialog import ConnectionDialog
from MenuBar import MenuBar
from Notebook import Notebook
from OracleDatabase import OracleDatabase
from Sidebar import Sidebar
from Table import Table


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
        # Update the notebook
        self.notebook.update(dbState)

    def openTable(self, tableName, sqlQuery, editable=False):
        # Execute the query
        data = self.db.execute(sqlQuery)
        # Get column names
        columnNames = [column[0] for column in self.db.cursor.description]

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
