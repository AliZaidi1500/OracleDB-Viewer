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
        # Add data to the treeview
        self.body.insert('', tk.END, text='Tables', iid='tables', open=False)
        self.body.insert('', tk.END, text='Views', iid='views', open=False)
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
                self.body.insert('tables', tk.END, text=tableName, iid=tableName, open=False)
                # Add table columns to the treeview
                for columnName, dataType, dataLength in self.parent.db.getColumnData(tableName):
                    self.body.insert(tableName, tk.END, text=columnName, open=False)
            # Add views to the treeview
            for viewName in self.parent.db.getViews():
                self.body.insert('views', tk.END, text=viewName, iid=viewName, open=False)
                # Add view columns to the treeview
                for columnName, dataType, dataLength in self.parent.db.getColumnData(viewName):
                    self.body.insert(viewName, tk.END, text=columnName, open=False)
