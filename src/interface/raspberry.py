from __future__ import absolute_import

from ..message import *

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

"""
Widget that assigns raspberry input.
"""

class Raspberry():
    def __init__(self, master):
        self.val = 0

        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.geometry('300x300')
        self.root.title('Configuration Raspberry')
        self.root.grab_set() # Interaction with main window impossible
        
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

        label3 = Label(frame_bottom, text='Write player :')
        label3.pack(padx=5, pady=5, side=LEFT)

        self.entry_player = Entry(frame_bottom, width=50)
        self.entry_player.pack(padx=5, pady=5, side=LEFT)
        self.entry_player.focus_force()

        # Buttons

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.pack(padx=5, pady=5, side=LEFT)

        btnApply = Button(self.root, text='Apply', command=self.apply_new_configuration)
        btnApply.pack(padx=5, pady=5, side=RIGHT)
        
    def apply_new_configuration(self):
        message = MSG_EVALUATE_STRING(self.master.text.marker.id , self.entry_player.get())
        print(message)
        self.master.add_to_send_queue(message)
        self.root.destroy()


