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
        self.root.geometry('300x300')
        self.root.title('Configuration Raspberry')
        self.root.grab_set() # Interaction with main window impossible
        """
        etiquette = Label(self.root, text='Entry :')
        etiquette.pack(padx=5, pady=5, side=LEFT)

        button = Button(self.root, text='Quitter', command=self.root.destroy).pack(padx=10, pady=10)
        button.pack(padx=5, pady=5)
        """
        # Top : Raspberry Input
        frame_top = LabelFrame(self.root, text="Input", padx=20, pady=20)
        frame_top.pack(fill="both")

        label = Label(frame_top, text='Select :')
        label.pack(padx=5, pady=5, side=LEFT)

        entree = Entry(frame_top, width=50)
        entree.pack(padx=5, pady=5, side=LEFT)
        entree.focus_force()

        # Middle : Set Up 
        frame_middle = LabelFrame(self.root, text="Set up", padx=20, pady=20)
        frame_middle.pack(fill="both")

        sp = Spinbox(frame_middle, from_=0, to=15)
        sp.pack()

        # Bottom : Player
        frame_bottom = LabelFrame(self.root, text="Player", padx=20, pady=20)
        frame_bottom.pack(fill="both")

        label3 = Label(frame_bottom, text='Set up player :')
        label3.pack(padx=5, pady=5, side=LEFT)

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.pack(padx=5, pady=5, side=LEFT)

        btnApply = Button(self.root, text='Apply')
        btnApply.pack(padx=5, pady=5, side=RIGHT)
        
    
        

