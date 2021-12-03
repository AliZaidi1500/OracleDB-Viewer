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

class Notebook(ttk.Notebook):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

    def addTab(self, tabName, tab):
        self.add(tab, text=tabName)

    def getTabID(self, tabName):
        for tabID in self.tabs():
            if self.tab(tabID, 'text') == tabName:
                return tabID

    def isOpen(self, tabName):
        try:
            return self.index(self.getTabID(tabName)) > -1
        except:
            return False

    def selectTab(self, tabName):
        self.select(self.getTabID(tabName))

    def update(self, dbState):
        if not dbState:
            for item in self.winfo_children():
                item.destroy()
