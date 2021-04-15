from __future__ import absolute_import

from ..message import *

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
        self.val = self.current_val = 0 #Simulation de la mesure d'un capteur

        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.title('New Player')
        self.root.geometry('350x300')
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
        Label(self.root, text='Enter a player name :').place(x=10, y=10)
        self.entry_player_name = Entry(self.root)
        self.entry_player_name.place(x=160, y=10)

        # Player 
        """
        Label(self.root, text='Write the player :').place(x=10, y=50)
        self.entry_player = Entry(self.root)
        self.entry_player.place(x=10, y=70)
        """

        Label(self.root, text='Choose a synth:').place(x=10, y=50)
        listSynth=["play", "pads","pluck","jbass", "loop"]
        self.ComboSynth = ttk.Combobox(self.root, values=listSynth)
        self.ComboSynth.current(0)
        self.ComboSynth.place(x=160, y=50)

        # Param
        Label(self.root, text='Choose a attribute:').place(x=10, y=90)
        listParam=["degree", "playstring", "oct","dur","delay", "blur", "amplify", "scale", "bpm", "sample", "sus", "fmod", "pan", "rate", "amp", "vib", "vibdepth", "slide", "sus", "slidedelay", "slidefrom", "bend", "benddelay", "coarse", "striate", "pshift", "hpf", "hpr", "lpf", "lpr", "swell", "bpf", "bits", "crush", "dist", "chop", "tremolo", "echo", "decay", "spin", "cut", "room", "mix", "formant", "shape"]
        self.ComboParam = ttk.Combobox(self.root, values=listParam)
        self.ComboParam.current(0)
        self.ComboParam.place(x=160, y=90)

        Label(self.root, text='Value:').place(x=10, y=120)
        self.EntryValue = Entry(self.root)
        self.EntryValue.place(x=160, y=120)
        
        # Buttons

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=190)

        btnApply = Button(self.root, text='Apply', command=self.apply_new_configuration)
        btnApply.place(x=270, y=190)

        
        
    def apply_new_configuration(self):
        self.player_name = self.entry_player_name.get()

        self.synth = self.ComboSynth.get()

        self.param = self.ComboParam.get()
 
        self.value = self.EntryValue.get()

        #SynthDef
        message = self.player_name + " >> " + self.synth + "()"
        message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
        self.master.add_to_send_queue(message_server)

        #Param
        message = self.player_name + "." + self.param + " = " + self.value 
        message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
        self.master.add_to_send_queue(message_server)

        #self.update_player() 
        self.root.destroy() # Close the popup
    
    def update_player(self):
        self.current_val += 1
        if self.current_val - self.val >= int(self.val_update):
            self.val = self.current_val
            print(self.val)
        self.master.root.after(200, self.update_player)


