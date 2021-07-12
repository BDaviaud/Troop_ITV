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
        self.root.grab_set() # Prevents interaction with the main window
        
        # List of FoxDoT players        
        pattern = re.compile(r'(?<=<)\w+')
        playing = self.master.lang.evaluate2("print('rasp', Clock.playing)")

        listPlayers = pattern.findall(playing[0])

        if not listPlayers:
            listPlayers = ['None']
        
        ### Popup interface
        # Drop-down list to choose the player
        Label(self.root, text='Choose a player :').place(x=10, y=10)
        self.ComboPlayername = ttk.Combobox(self.root, values=listPlayers)
        self.ComboPlayername.current(0)
        self.ComboPlayername.place(x=160, y=10)

        # Drop-down list to choose the player parameter
        Label(self.root, text='Choose a attribute:').place(x=10, y=50)
        listParam=["dur","degree", "playstring", "oct","delay", "blur", "amplify", "scale", "bpm", "sample", "sus", "fmod", "pan", "rate", "amp", "vib", "vibdepth", "slide", "sus", "slidedelay", "slidefrom", "bend", "benddelay", "coarse", "striate", "pshift", "hpf", "hpr", "lpf", "lpr", "swell", "bpf", "bits", "crush", "dist", "chop", "tremolo", "echo", "decay", "spin", "cut", "room", "mix", "formant", "shape"]
        self.ComboParam = ttk.Combobox(self.root, values=listParam)
        self.ComboParam.current(0)
        self.ComboParam.place(x=160, y=50)
        
        # Pin number for GPIO input
        Label(self.root, text='Input pin GPIO :').place(x=10, y=90)
        self.SpinboxGPIO = Spinbox(self.root, from_=1, to=40)
        self.SpinboxGPIO.place(x=160, y=90)
        
        # Buttons
        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=130)

        btnApply = Button(self.root, text='Apply', command=self.getInput)
        btnApply.place(x=270, y=130)
        
    def getInput(self):
        """ Method called when the 'Apply' button is activated.
            If a player is selected, the interface inputs are saved
            and the GPIO input is configured.
        """
        self.player_name = self.ComboPlayername.get()
        
        if self.player_name != 'None':
            self.param = self.ComboParam.get()
            self.gpioId = int(self.SpinboxGPIO.get())
            
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpioId, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            self.update(self.gpioId)
            # Add an event listener on the gpio input. 
            GPIO.add_event_detect(self.gpioId, GPIO.BOTH, callback=self.update, bouncetime = 75)

        self.root.destroy() # Close the popup
        
    def update(self, channel):
        """ This method is the callback function called when the value changes on the GPIO input.
            It updates the value of the player parameter.
        """
        # Ask the FoxDot interpreter the state of the player.
        commande = 'print("rasp", ' + self.player_name + '.isplaying)'
        isplaying = self.master.lang.evaluate2(commande)
        isplaying = isplaying[0].rsplit(None, 1)[-1] # returns the last word of the string
        
        if isplaying == 'False':
            # If the player is stopped, the event handler on this channel is removed
            GPIO.remove_event_detect(self.gpioId)
        else:
            self.current_value = GPIO.input(self.gpioId)
            message = self.player_name + "." + self.param + " = " + str(self.current_value) # player_name.param = current_value
            # The message is aded to the queue to be sent to the Troop server.
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
        
        ### Popup Interface
        # Input for the python code 
        Label(self.root, text='Code:').place(x=10, y=10)
        self.textCode = Text(self.root, height=20, width=30)
        self.textCode.place(x=10, y=40)
        
        # List of implemented states
        Label(self.root, text='States:').place(x=260, y=10)
        self.textStates = Text(self.root, height=10, width=30)
        self.textStates.place(x=260, y=40)
        self.textStates.configure(state='disabled')
        Button(self.root, text="Add State", command=lambda: StateOrchestration(self)).place(x=415, y=10)
        
        # List of implemented transitions
        Label(self.root, text='Transitions:').place(x=260, y=230)
        self.textTransitions = Text(self.root, height=10, width=30)
        self.textTransitions.place(x=260, y=260)
        self.textTransitions.configure(state='disabled')
        Button(self.root, text="Add Transition", command=lambda: TransitionOrchestration(self)).place(x=380, y=230)
   

        Button(self.root, text="Read", command=self.getInput).place(x=100, y=400)

    def getInput(self):
        """ Method called by the 'Read' button of the Orchestration popup.
            The Orchestration inputs are saved et the orchestration is evaluated."""
        self.codeStates = self.textCode.get("1.0","end")
        
        # Instantiates values of the transitions and the states by the interpreter.
        self.master.lang.evaluate(self.getCode(self.listTransitions))
        self.master.lang.evaluate(self.getCode(self.listStates))
        
        # Evaluation of the FoxDot code of the active state (initial state)
        for state in self.listStates:
            if state.currentValue == 'True':
                self.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.text.marker.id , state.action))
        
        # Active an event handler on the gpio input of each transition.
        for trans in self.listTransitions:
            GPIO.add_event_detect(trans.gpioId, GPIO.BOTH, callback=self.update, bouncetime = 75)
        
        self.root.destroy()
    
    def update(self, channel):
        """ Callback function called when the value changes on the GPIO input.
            Updates the value of the transitions and the states."""
        # Update of transitions value.
        for trans in self.listTransitions:
            if trans.gpioId == channel:
                trans.currentValue = GPIO.input(trans.gpioId)
            self.master.lang.evaluate(self.getCode(self.listTransitions))
        
        # Update of states value with the new transitions.
        self.master.lang.evaluate(self.codeStates)
        
        # Ask the new state value to the interpreter.
        for state in self.listStates:
            commande = 'print("rasp", ' + state.name + ')'
            newValue = self.master.lang.evaluate2(commande) # Warning : return a list of string
            newValue = newValue[0].rsplit(None, 1)[-1] # Returns the last word of the string.
            state.updateState(newValue)
    
    def getCode(self, listItems):
        """ Take a list of States or Transitions and a returns a python code in string form."""
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

        btnSave = Button(self.root, text='Save', command=self.getInput)
        btnSave.place(x=270, y=310)
        
    def getInput(self):
        """ Method called by the 'Save' button of the StateOrchestration popup.
            Saved the interface inputs and add to the list of states of the Orchestration class. """
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
        """ Updates the value of the state, and if it becomes active, evaluates its FoxDot code (action). """
        if self.currentValue != newValue:
            self.currentValue = newValue
            if newValue == 'True':
                # Adds the FoxDot code to the queue to be sent to all clients.
                self.master.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.master.text.marker.id , self.action))
        
class TransitionOrchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup
        self.root.title('Add a transition')
        self.root.geometry('360x120')
        self.root.grab_set()
        
        # State name
        Label(self.root, text='Name :').place(x=10, y=10)
        self.entryName = Entry(self.root)
        self.entryName.place(x=160, y=10)
        
        # Pin number for GPIO input
        Label(self.root, text='Input pin GPIO :').place(x=10, y=50)
        self.spinboxGPIO = Spinbox(self.root, from_=1, to=40)
        self.spinboxGPIO.place(x=160, y=50)
        
        # Buttons
        btnCancel = Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.place(x=10, y=90)

        btnSave = Button(self.root, text='Save', command=self.getInput)
        btnSave.place(x=270, y=90)
    
    def getInput(self):
        """ Method called by the 'Save' button of the TransitionOrchestration popup.
            Saved the interface inputs and add to the list of transitions of the Orchestration class. """
        if self.entryName.get() != "":
            self.name = self.entryName.get()
            self.gpioId = int(self.spinboxGPIO.get())

            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpioId, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.currentValue = GPIO.input(self.gpioId)
            
            self.master.listTransitions.append(self)
            
            self.master.textTransitions.configure(state='normal')
            self.master.textTransitions.insert(END, self.name + " => pin " + str(self.gpioId) + "\n")
            self.master.textTransitions.configure(state='disabled')
        
        self.root.destroy()

        
        


        
        