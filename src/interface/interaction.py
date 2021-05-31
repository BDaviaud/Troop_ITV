from __future__ import absolute_import

from ..message import *
import random
import re
from FoxDot import *
import RPi.GPIO as GPIO

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter import ttk

"""
Widget for raspberry input.
"""

class SensorInteraction():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup
        self.root.title('Sensor and Player Configuration')
        self.root.geometry('360x170')
        self.root.grab_set() # Empêche d'interagir avec la fenêtre principale
        
        # Liste des players en cours d'execution        
        pattern = re.compile(r'(?<=<)\w+')
        playing = self.master.lang.evaluate2("print('re', Clock.playing)")

        listPlayer = pattern.findall(playing[0])

        if not listPlayer:
            listPlayer = ['None']

        # Nom du player
        Label(self.root, text='Chose a player :').place(x=10, y=10)
        self.ComboPlayername = ttk.Combobox(self.root, values=listPlayer)
        self.ComboPlayername.current(0)
        self.ComboPlayername.place(x=160, y=10)

        # Paramêtre
        Label(self.root, text='Choose a attribute:').place(x=10, y=50)
        listParam=["dur","degree", "playstring", "oct","delay", "blur", "amplify", "scale", "bpm", "sample", "sus", "fmod", "pan", "rate", "amp", "vib", "vibdepth", "slide", "sus", "slidedelay", "slidefrom", "bend", "benddelay", "coarse", "striate", "pshift", "hpf", "hpr", "lpf", "lpr", "swell", "bpf", "bits", "crush", "dist", "chop", "tremolo", "echo", "decay", "spin", "cut", "room", "mix", "formant", "shape"]
        self.ComboParam = ttk.Combobox(self.root, values=listParam)
        self.ComboParam.current(0)
        self.ComboParam.place(x=160, y=50)
        
        # Numéro de pin pour l'entrée GPIO
        Label(self.root, text='Input pin GPIO :').place(x=10, y=90)
        self.SpinboxGPIO = Spinbox(self.root, from_=1, to=40)
        self.SpinboxGPIO.place(x=160, y=90)
        
        # Buttons

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=130)

        btnApply = Button(self.root, text='Apply', command=self.apply_new_configuration)
        btnApply.place(x=270, y=130)
        
    def apply_new_configuration(self):
        self.player_name = self.ComboPlayername.get()
        
        if self.player_name != 'None':
            self.param = self.ComboParam.get()
            self.GPIOid = int(self.SpinboxGPIO.get())
            
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.GPIOid, GPIO.OUT)

            self.current_value = GPIO.input(self.GPIOid)
            #Param
            message = self.player_name + "." + self.param + " = " + str(self.current_value) 
            message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
            self.master.add_to_send_queue(message_server)

            self.update_player() # Lance la méthode récursive

        self.root.destroy() # Close the popup
    
    def update_player(self):
        
        # Récupératinon de la variable isplaying du player (La valeur est retournée sous forme d'un tableau de string)
        commande = 'print("re", ' + self.player_name + '.isplaying)'
        isplaying = self.master.lang.evaluate2(commande)

        if isplaying[0] == 're False':
            return
        else:
            if GPIO.input(self.GPIOid) != self.current_value:
                self.current_value = GPIO.input(self.GPIOid)
                message = self.player_name + "." + self.param + " = " + str(self.current_value)
                message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
                self.master.add_to_send_queue(message_server)
            
            self.master.root.after(200, self.update_player)
        
"""
Widget for orchestration.
"""
class Orchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.title('Orchestration')
        self.root.geometry('700x450')
        self.root.grab_set() # Interaction with main window impossible

        Label(self.root, text='Initial state:').pack()
        self.textBox1 = Text(self.root, height=10)
        self.textBox1.pack()
        Label(self.root, text='Body:').pack()
        self.textBox2 = Text(self.root, height=10)
        self.textBox2.pack()

        btnRead = Button(self.root, text="Read", command=self.getTextInput).pack()

        #btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)

    def getTextInput(self):
        self.code_initialState = self.textBox1.get("1.0","end")
        self.code_body = self.textBox2.get("1.0","end")
        # Evaluation du code
        self.master.lang.evaluate(self.code_initialState)
        self.master.lang.evaluate(self.code_body)

        self.master.listOrchestrations.append([len(self.master.listOrchestrations), self])

        self.update()

        self.root.destroy()

    def update(self):
        # Méthode récursive qui réexécute le corps du code.
        
        self.master.lang.evaluate(self.code_body)

        self.master.root.after(200, self.update)