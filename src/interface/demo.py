from __future__ import absolute_import

from ..message import *
import random
import re as regex
from FoxDot import *
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_mpr121
import numpy

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter import ttk
"""
Widget for raspberry input.
"""
lengthMemo = 10
seuil = 0.5

class Orchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.title('Orchestration')
        self.root.geometry('520x450')
        self.root.grab_set() # Interaction with main window impossible
        
        self.listStates = [State(self, 'E0', True, ''),State(self, 'E1', False, 'p1 >> play("x-o{-[--][-o][---]}")'),State(self, 'E1b', False, 'p1 >> play("x-o{o[--][-o][---]}")'),State(self, 'E2', False, 'p2 >> pluck([0,1,2,[3,7,5]], chop=4, amp=0.5, dur=1)'),State(self, 'E2b', False, 'p2 >> pluck([0,2,3,1,[4,6]], chop=4, amp=0.5, dur=1)'),State(self, 'E3', False, 'p3 >> blip(oct=4, dur=[1/2, 1/2, 1/4])'),State(self, 'E3b', False, 'p3 >> blip(oct=3, dur=[1/2, 1/2, 1/4])'),State(self, 'E4', False, 'Clock.clear()')]
        self.listTempo = [State(self, 'memo1', True, ''), State(self, 'memo2', True, ''),State(self, 'memo3', True, '')]
        ### liste des capteurs et leurs entrées
        self.listSensors = [SensorCAP('e0'),SensorCAP('e1'),SensorCAP('e2'),SensorCAP('e3'),SensorCAP('e4'),SensorCAP('e5'),SensorCAP('e6'),SensorCAP('e7'),SensorCAP('e8'),SensorCAP('e9'), SensorCAP('e10'),SensorCAP('e11')]

        ### Popup Interface
        # Input for the python code 
        Label(self.root, text='Transitions:').place(x=10, y=10)
        self.textCode = Text(self.root, height=20, width=30)
        self.textCode.place(x=10, y=40)
        self.textCode.insert(INSERT, "if E0 and e0 and memo1:\n\tE0 = False\n\tE1 = True\n\nif E0 and e0 and not memo1:\n\tE0 = False\n\tE1b = True\n\nif E1 and not e0 and memo1:\n\tmemo1 = False\n\tE1 = False\n\tE0 = True\n\nif E1b and not e0 and not memo1:\n\tmemo1 = True\n\tE1b = False\n\tE0 = True\n\nif E0 and e1 and memo2:\n\tE0 = False\n\tE2 = True\n\nif E0 and e1 and not memo2:\n\tE0 = False\n\tE2b = True\n\nif E2 and not e1 and memo2:\n\tmemo2 = False\n\tE2 = False\n\tE0 = True\n\nif E2b and not e1 and not memo2:\n\tmemo2 = True\n\tE2b = False\n\tE0 = True\n\nif E0 and e2 and memo3:\n\tE0 = False\n\tE3 = True\n\nif E0 and e2 and not memo3:\n\tE0 = False\n\tE3b = True\n\nif E3 and not e2 and memo3:\n\tmemo3 = False\n\tE3 = False\n\tE0 = True\n\nif E3b and not e2 and not memo3:\n\tmemo3 = True\n\tE3b = False\n\tE0 = True\n\nif E0 and e3:\n\tE0 = False\n\tE4 = True\n\nif E4 and not e3:\n\tE4 = False\n\tE0 = True")
        
        # List of implemented states
        Label(self.root, text='States:').place(x=260, y=10)
        self.textStates = Text(self.root, height=10, width=30)
        self.textStates.place(x=260, y=40)
        #print(len(self.listStates))
        for state in self.listStates :
            self.textStates.insert(END, state.name + " = " + str(state.currentValue) + "\n")
        self.textStates.configure(state='disabled')
        #Button(self.root, text="Add State", command=lambda: StateOrchestration(self)).place(x=415, y=10)
        
        # List of implemented sensors
        Label(self.root, text='Sensors:').place(x=260, y=230)
        self.textSensors = Text(self.root, height=10, width=30)
        self.textSensors.place(x=260, y=260)
        for gpio in self.listSensors :
            self.textSensors.insert(END, gpio.name +"\n")
        self.textSensors.configure(state='disabled')
        #Button(self.root, text="Add Sensor", command=lambda: TransitionOrchestration(self.master)).place(x=380, y=230)
   

        Button(self.root, text="Read", command=self.getInput).place(x=100, y=400)

    def getInput(self):
        """ Method called by the 'Read' button of the Orchestration popup.
            The Orchestration inputs are saved et the orchestration is evaluated."""
        self.master.lang.evaluate("play=FileSynthDef('play2');play.add();")
        self.master.lang.evaluate(self.getCode(self.listTempo))
        self.codeStates = self.textCode.get("1.0","end")
        
        # Create MPR121 object and initialize entries
        print("Initialisation mpr")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpr121 = adafruit_mpr121.MPR121(i2c,address=0x5a)
        self.memorize_pins(1)
        
        # Evaluate the list of transitions
        self.master.lang.evaluate(self.getCode(self.listSensors))
        # Evaluate the list of states
        self.master.lang.evaluate(self.getCode(self.listStates))
        print("Code Evalue")
        
        # Evaluation of the FoxDot code of the active state (initial state)
        for state in self.listStates:
            if state.currentValue == 'True':
                self.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.text.marker.id , state.action))
                
        #self.update()

        self.root.destroy() # Close the popup
    
    def memorize_pins(self, val=0):
        """ This method is the callback function called when the value changes on the GPIO input.
            It updates the value of the player parameter.
        """
        
        for j in range(lengthMemo):
            # Loop through all 12 inputs (0-11).      
            for i in range(12):
                # Pour capteur
                if self.mpr121[i].value:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                    self.listSensors[i].vector[j]=1
                else:
                    self.listSensors[i].vector[j]=0
        
        value = 0
        valueChanged = False
        for i in range(12):
            # Pour capteur A
            value = numpy.mean(self.listSensors[i].vector)
            if (value > seuil):
                value = 1
            else:
                value = 0
            if (value != self.listSensors[i].currentValue):
                self.listSensors[i].currentValue = value
                valueChanged = True
        
        if valueChanged and val==0:
            #print("Value Changed")
            self.update()
        
        self.master.root.after(5, self.memorize_pins)
    
    def update(self):
        """ Callback function called when the value changes on the GPIO input.
            Updates the value of the transitions and the states."""
        # Update of transitions value.
        self.master.lang.evaluate(self.getCode(self.listSensors))
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
    
class SensorCAP():
    def __init__(self, name):
        self.name = name
        self.currentValue = 0
        self.vector = numpy.zeros(lengthMemo)

class State():
    def __init__(self, master, name, value, action):
        self.master = master
        self.name = name
        self.currentValue = value
        self.action = action
        
    def updateState(self, newValue):
        """ Updates the value of the state, and if it becomes active, evaluates its FoxDot code (action). """
        if self.currentValue != newValue:
            self.currentValue = newValue
            if newValue == 'True':
                # Adds the FoxDot code to the queue to be sent to all clients.
                self.master.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.master.text.marker.id , self.action))
        
