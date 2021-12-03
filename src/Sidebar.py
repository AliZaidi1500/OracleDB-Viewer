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
import tkinter.ttk as ttk

class Sidebar(tk.Frame):

    def __init__(self, parent=None, **kw):
        super().__init__(parent, **kw)

        self.parent = parent

        # Initialize the sidebar
        self.intialize()

    def intialize(self):
        # Disable pack propagation
        self.pack_propagate(0)
        # Create the sidebar header
        self.header = tk.Label(self, bg='white')
        self.header.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        # Create the sidebar body treeview
        self.body = ttk.Treeview(self, show='tree', selectmode='none')
        self.body.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Add double click event to the body treeview
        self.body.bind('<Double-1>', self.onDoubleClick)
        # Add data to the treeview
        self.body.insert('', tk.END, text='Tables', iid='TABLES', open=False)
        self.body.insert('', tk.END, text='Views', iid='VIEWS', open=False)
        # Create the sidebar footer
        self.footer = tk.Label(self, bg='white')
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def update(self, dbState):
        # Update the header
        self.header.config(
            text=f'Connected to {self.parent.db.host} as {self.parent.db.username}'
                if dbState else 'Not connected')
        # Update the body
        self.updateBody(dbState)
        # Update the footer
        self.footer.config(
            text=f'Oracle Version: {self.parent.db.version}' if dbState else 'Oracle Version:')

    def updateBody(self, dbState):
        # Clear treeview data
        for (i, child) in enumerate(self.body.get_children()):
            for (i, child) in enumerate(self.body.get_children(child)):
                self.body.delete(child)

        # Add data to the treeview if database is connected
        if dbState:
            # Add tables to the treeview
            for tableName in self.parent.db.getTables():
                tableIID = f'TABLE_{tableName}'
                self.body.insert('TABLES', tk.END, text=tableName, iid=tableIID, open=False)
                # Add table columns to the treeview
                for columnName, dataType, dataLength in self.parent.db.getColumnData(tableName):
                    self.body.insert(tableIID, tk.END, text=columnName, open=False)
            # Add views to the treeview
            for viewName in self.parent.db.getViews():
                viewIID = f'VIEW_{viewName}'
                self.body.insert('VIEWS', tk.END, text=viewName, iid=viewIID, open=False)
                # Add view columns to the treeview
                for columnName, dataType, dataLength in self.parent.db.getColumnData(viewName):
                    self.body.insert(viewIID, tk.END, text=columnName, open=False)

    def onDoubleClick(self, event):
        item = self.body.identify('item', event.x, event.y)
        # If the item is a table or view
        if item.startswith('TABLE_') or item.startswith('VIEW_'):
            # Get the table or view name
            tableName = self.body.item(item, 'text')
            # Open the table or view
            self.parent.openTable(tableName, f'SELECT * FROM {tableName}', True)
