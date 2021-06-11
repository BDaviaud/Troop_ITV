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
        playing = self.master.lang.evaluate2("print('rasp', Clock.playing)")

        listPlayer = pattern.findall(playing[0])

        if not listPlayer:
            listPlayer = ['None']

        # Nom du player
        Label(self.root, text='Choose a player :').place(x=10, y=10)
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

        btnApply = Button(self.root, text='Apply', command=self.apply_configuration)
        btnApply.place(x=270, y=130)
        
    def apply_configuration(self):
        self.player_name = self.ComboPlayername.get()
        
        if self.player_name != 'None':
            self.param = self.ComboParam.get()
            self.GPIOid = int(self.SpinboxGPIO.get())
            
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.GPIOid, GPIO.IN)
            
            self.update(self.GPIOid)
            # Add an event listener on the gpio input. 
            GPIO.add_event_detect(self.GPIOid, GPIO.BOTH, callback=self.update, bouncetime = 75)

        self.root.destroy() # Close the popup
        
    def update(self, channel):
        # Demande au serveur de l'état du player et récupération de la réponse
        commande = 'print("rasp", ' + self.player_name + '.isplaying)'
        isplaying = self.master.lang.evaluate2(commande)
        isplaying = isplaying[0].rsplit(None, 1)[-1] # Retourne le dernier mot de la chaine de caractères
        
        if isplaying == 'False':
            # Supprime les interruptions sur ce cannal
            GPIO.remove_event_detect(self.GPIOid)
        else:
            self.current_value = GPIO.input(self.GPIOid)
            message = self.player_name + "." + self.param + " = " + str(self.current_value) # player_name.param = current_value
            # On envoie le message (objet MESSAGE) dans la queue pour qu'il soit executé par tous les clients.
            message_server = MSG_EVALUATE_STRING(self.master.text.marker.id , message)
            self.master.add_to_send_queue(message_server)
            
            
            
        
        
"""
Widget for orchestration.
"""
class Orchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.title('Orchestration')
        self.root.geometry('520x450')
        self.root.grab_set() # Interaction with main window impossible
        
        self.listStates = []
        self.listTransitions = []
        
        Label(self.root, text='Code:').place(x=10, y=10)
        self.textCode = Text(self.root, height=20, width=30)
        self.textCode.place(x=10, y=40)
        
        Label(self.root, text='Initials states:').place(x=260, y=10)
        self.textStates = Text(self.root, height=10, width=30)
        self.textStates.place(x=260, y=40)
        self.textStates.configure(state='disabled')
        Button(self.root, text="Add State", command=lambda: StateOrchestration(self)).place(x=415, y=10)
        
        Label(self.root, text='Transitions:').place(x=260, y=230)
        self.textTransitions = Text(self.root, height=10, width=30)
        self.textTransitions.place(x=260, y=260)
        self.textTransitions.configure(state='disabled')
        Button(self.root, text="Add Transition", command=lambda: TransitionOrchestration(self)).place(x=380, y=230)
   

        Button(self.root, text="Read", command=self.getInput).place(x=100, y=400)

        #btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)

    def getInput(self):
        self.codeStates = self.textCode.get("1.0","end")
        
        # Instancier les valeurs des transitions et des Etats initiaux du point de vue de l'interpreter FoxDot.
        self.master.lang.evaluate(self.getCode(self.listTransitions))
        self.master.lang.evaluate(self.getCode(self.listStates))
        
        for state in self.listStates:
            if state.currentValue == 'True':
                self.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.text.marker.id , state.action))
        
        for trans in self.listTransitions:
            GPIO.add_event_detect(trans.gpioId, GPIO.BOTH, callback=self.update, bouncetime = 75)
        
        self.root.destroy()
    
    def update(self, channel):
        # Mise à jour des valeurs de transitions
        for trans in self.listTransitions:
            if trans.gpioId == channel:
                trans.currentValue = GPIO.input(trans.gpioId)
            self.master.lang.evaluate(self.getCode(self.listTransitions))
        
        # Mise à jour des Etats avec nouvelle valeur de transitions
        self.master.lang.evaluate(self.codeStates)
        
        #Récupération des nouvelles valeurs d'etat
        for state in self.listStates:
            commande = 'print("rasp", ' + state.name + ')'
            newValue = self.master.lang.evaluate2(commande) # Warning : return a list of string
            newValue = newValue[0].rsplit(None, 1)[-1] # Retourne le dernier mot de la chaine de caractères
            state.updateState(newValue)
    
    def getCode(self, listItems):
        code = ""
        for item in listItems:
            code += item.name + " = " + str(item.currentValue) + "\n"          
        return code

class StateOrchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup
        self.root.title('Add a state')
        self.root.geometry('360x350')
        self.root.grab_set()
        
        # State name
        Label(self.root, text='Name :').place(x=10, y=10)
        self.entryName = Entry(self.root)
        self.entryName.place(x=150, y=10)

        # Sate inital value
        Label(self.root, text='Initial value :').place(x=10, y=50)
        self.comboValues = ttk.Combobox(self.root, values=["False", "True"])
        self.comboValues.current(0)
        self.comboValues.place(x=150, y=50)
        
        # Action
        Label(self.root, text='FoxDot Code:').place(x=10, y=90)
        self.textAction = Text(self.root, width=40, height=10)
        self.textAction.place(x=10, y=120)
        
        # Buttons

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=310)

        btnSave = Button(self.root, text='Save', command=self.saveState)
        btnSave.place(x=270, y=310)
        
    def saveState(self):
        if self.entryName.get() != "":
            self.name = self.entryName.get()
            self.currentValue = self.comboValues.get()
            self.action = self.textAction.get("1.0","end")
            
            self.master.listStates.append(self)
            
            self.master.textStates.configure(state='normal')
            self.master.textStates.insert(END, self.name + " = " + self.currentValue + "\n")
            self.master.textStates.configure(state='disabled')
        
        self.root.destroy()
        
    def updateState(self, newValue):
        if self.currentValue != newValue:
            self.currentValue = newValue
            if newValue == 'True':
                # Ajout du code FoxDot de l'etat à la queue pour qu'il soit envoyé à tous les clients
                self.master.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.master.text.marker.id , self.action))
        
class TransitionOrchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup
        self.root.title('Add a state')
        self.root.geometry('360x120')
        self.root.grab_set()
        
        # State name
        Label(self.root, text='Name :').place(x=10, y=10)
        self.entryName = Entry(self.root)
        self.entryName.place(x=160, y=10)
        
        # Numéro de pin pour l'entrée GPIO
        Label(self.root, text='Input pin GPIO :').place(x=10, y=50)
        self.spinboxGPIO = Spinbox(self.root, from_=1, to=40)
        self.spinboxGPIO.place(x=160, y=50)
        
        
        # Buttons

        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=90)

        btnSave = Button(self.root, text='Save', command=self.saveTransition)
        btnSave.place(x=270, y=90)
    
    def saveTransition(self):
        if self.entryName.get() != "":
            self.name = self.entryName.get()
            self.gpioId = int(self.spinboxGPIO.get())

            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpioId, GPIO.IN)
            self.currentValue = GPIO.input(self.gpioId)
            
            self.master.listTransitions.append(self)
            
            self.master.textTransitions.configure(state='normal')
            self.master.textTransitions.insert(END, self.name + " => pin " + str(self.gpioId) + "\n")
            self.master.textTransitions.configure(state='disabled')
        
        self.root.destroy()

        
        


        
        