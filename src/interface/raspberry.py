from __future__ import absolute_import

from ..message import *
import random

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter import ttk

"""
Widget that assigns raspberry input.
"""

class Raspberry():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.title('New Player')
        self.root.geometry('350x250')
        self.root.grab_set() # Interaction with main window impossible
        """
        label = Label(frame_top, text='Select :')
        label.pack(padx=5, pady=5, side=LEFT)

        entree = Entry(frame_top)
        entree.pack(padx=5, pady=5, side=LEFT)
        entree.focus_force()
        """
 #       self.sp = Spinbox(frame_middle, from_=1, to=20)
 #       self.sp.pack()

        # Bottom : Player
        #frame_bottom = Frame(self.root, padx=20, pady=20)
        #frame_bottom.pack(fill="both")

        ## Player Name
        Label(self.root, text='Enter the player name :').place(x=10, y=10)
        self.entry_player_name = Entry(self.root)
        self.entry_player_name.place(x=160, y=10)

        # Param
        Label(self.root, text='Choose a attribute:').place(x=10, y=50)
        listParam=["degree", "playstring", "oct","dur","delay", "blur", "amplify", "scale", "bpm", "sample", "sus", "fmod", "pan", "rate", "amp", "vib", "vibdepth", "slide", "sus", "slidedelay", "slidefrom", "bend", "benddelay", "coarse", "striate", "pshift", "hpf", "hpr", "lpf", "lpr", "swell", "bpf", "bits", "crush", "dist", "chop", "tremolo", "echo", "decay", "spin", "cut", "room", "mix", "formant", "shape"]
        self.ComboParam = ttk.Combobox(self.root, values=listParam)
        self.ComboParam.current(0)
        self.ComboParam.place(x=160, y=50)

        Label(self.root, text='Max value:').place(x=10, y=90)
        self.EntryMaxValue = Entry(self.root)
        self.EntryMaxValue.place(x=160, y=90)

        Label(self.root, text='Min value:').place(x=10, y=130)
        self.EntryMinValue = Entry(self.root)
        self.EntryMinValue.place(x=160, y=130)

        Label(self.root, text='Refresh Time (in second):').place(x=10, y=170)
        self.SpinboxTime = Spinbox(self.root, from_=10, to=120)
        self.SpinboxTime.place(x=160, y=170)
        
        # Buttons

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=210)

        btnApply = Button(self.root, text='Apply', command=self.apply_new_configuration)
        btnApply.place(x=270, y=210)

        
        
    def apply_new_configuration(self):
        self.player_name = self.entry_player_name.get()
        self.param = self.ComboParam.get()
        self.max = float(self.EntryMaxValue.get())
        self.min = float(self.EntryMinValue.get())
        self.refreshTime = int(self.SpinboxTime.get())

        val = int(self.min + random.random() * (self.max - self.min))
        print(val)

        #Param
        message = self.player_name + "." + self.param + " = " + str(val) 
        message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
        self.master.add_to_send_queue(message_server)

        self.update_player() 
        self.root.destroy() # Close the popup
    
    def update_player(self):
        val = int(self.min + random.random() * (self.max - self.min))
        print(val)
        
        message = self.player_name + "." + self.param + " = " + str(val)
        message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
        self.master.add_to_send_queue(message_server)
        
        self.master.root.after(self.refreshTime*100, self.update_player)


