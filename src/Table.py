import tkinter as tk
import tksheet as tks

class Table(tks.Sheet):

    def __init__(self, parent, table=None, editable=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.table = table
        self.editable = editable
