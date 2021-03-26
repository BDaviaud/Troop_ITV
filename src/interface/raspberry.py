from __future__ import absolute_import

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

"""
Widget that assigns raspberry input.
"""

class Raspberry():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.geometry('300x100')
        self.root.title('Configuration Raspberry')
        Button(self.root, text='Quitter', command=self.root.destroy).pack(padx=10, pady=10)
        self.root.grab_set() # Interaction with main window impossible

