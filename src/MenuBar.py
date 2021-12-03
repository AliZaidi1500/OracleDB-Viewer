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
