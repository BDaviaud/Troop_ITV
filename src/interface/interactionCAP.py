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
seuil = 0.3

class Orchestration():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root) # Popup -> Toplevel()
        self.root.title('Orchestration')
        self.root.geometry('520x450')
        self.root.grab_set() # Interaction with main window impossible
        
        self.listStates = []
        # List of implemented states
        Label(self.root, text='States:').place(x=260, y=10)
        self.textStates = Text(self.root, height=10, width=30)
        self.textStates.place(x=260, y=40)
        self.textStates.configure(state='disabled')
        Button(self.root, text="Add State", command=lambda: StateOrchestration(self)).place(x=415, y=10)
        ### liste des capteurs et leurs entrées
        
        self.listInputSensor = [SensorCAP('p0'),SensorCAP('p1'),SensorCAP('p2'),SensorCAP('p3'),SensorCAP('p4'),SensorCAP('p5'),SensorCAP('p6'),SensorCAP('p7'),SensorCAP('p8'),SensorCAP('p9'), SensorCAP('p10'),SensorCAP('p11')]
        
        ### Popup Interface
        # Input for the python code 
        Label(self.root, text='Code:').place(x=10, y=10)
        self.textCode = Text(self.root, height=20, width=30)
        self.textCode.place(x=10, y=40)
        
        # List of implemented sensors
        Label(self.root, text='Sensors:').place(x=260, y=230)
        self.textSensors = Text(self.root, height=10, width=30)
        self.textSensors.place(x=260, y=260)
        for inputX in self.listInputSensor :
            self.textSensors.insert(END, inputX.name + "\n")
        self.textSensors.configure(state='disabled')
        #Button(self.root, text="Add Sensor", command=lambda: TransitionOrchestration(self.master)).place(x=380, y=230)
        
        Button(self.root, text="Read", command=self.getInput).place(x=100, y=400)

    def getInput(self):
        """ Method called by the 'Read' button of the Orchestration popup.
            The Orchestration inputs are saved et the orchestration is evaluated."""
        
        # Create MPR121 object and initialize entries
        print("Initialisation mpr")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpr121a = adafruit_mpr121.MPR121(i2c,address=0x5a)
        self.memorize_pins(1)
        
        self.codeStates = self.textCode.get("1.0","end")
        
        # Evaluate the list of transitions
        self.master.lang.evaluate(self.getCode(self.listInputSensor))
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
        
        for j in range(12*lengthMemo):
            # Loop through all 12 inputs (0-11).      
            for i in range(12):
                # Pour capteur A
                if self.mpr121a[i].value:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                    self.listInputSensor[i].vector[j%lengthMemo]=1
                else:
                    self.listInputSensor[i].vector[j%lengthMemo]=0
        
        value = 0
        valueChanged = False
        for i in range(12):
            value = numpy.mean(self.listInputSensor[i].vector)
            if (value > seuil):
                value = 1
            else:
                value = 0
            if (value != self.listInputSensor[i].currentValue):
                self.listInputSensor[i].currentValue = value
                valueChanged = True
        
        if valueChanged and val==0:
            #print("Value Changed")
            self.update()
        
        self.master.root.after(5, self.memorize_pins)
    
    def update(self):
        """ Callback function called when the value changes on the GPIO input.
            Updates the value of the transitions and the states."""
        #print("Update")
        # Update of transitions value.
        self.master.lang.evaluate(self.getCode(self.listInputSensor))
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
        