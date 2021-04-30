from __future__ import absolute_import

from ..message import *
import random
from FoxDot import *

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

        isplaying = self.master.lang.evaluate2("print(Clock.playing)")  
        print(isplaying)

        ## Player Name
        Label(self.root, text='Enter the player name :').place(x=10, y=10)
        self.entry_player_name = Entry(self.root)
        self.entry_player_name.place(x=160, y=10)

        # Param
        Label(self.root, text='Choose a attribute:').place(x=10, y=50)
        listParam=["dur","degree", "playstring", "oct","delay", "blur", "amplify", "scale", "bpm", "sample", "sus", "fmod", "pan", "rate", "amp", "vib", "vibdepth", "slide", "sus", "slidedelay", "slidefrom", "bend", "benddelay", "coarse", "striate", "pshift", "hpf", "hpr", "lpf", "lpr", "swell", "bpf", "bits", "crush", "dist", "chop", "tremolo", "echo", "decay", "spin", "cut", "room", "mix", "formant", "shape"]
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

        #Param
        message = self.player_name + "." + self.param + " = " + str(val) 
        message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
        self.master.add_to_send_queue(message_server)

        self.update_player() # Lance la méthode récursive
        self.root.destroy() # Close the popup
    
    def update_player(self):
        # Récupératinon de la variable isplaying du player (La valeur est retournée sous forme d'un tableau de string)
        commande = 'print(' + self.player_name + '.isplaying)'
        isplaying = self.master.lang.evaluate2(commande)

        # Nouvelle valeur (random)
        val = int(self.min + random.random() * (self.max - self.min))

        if isplaying[0] == 'False':
            return
        else:         
            message = self.player_name + "." + self.param + " = " + str(val)
            message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
            self.master.add_to_send_queue(message_server)
            
            self.master.root.after(self.refreshTime*100, self.update_player)
        


