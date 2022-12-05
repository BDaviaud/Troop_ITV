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

lengthMemo = 10
seuil = 0.3
    
class Orchestration:
    def __init__(self, master):
        self.master = master.master
        self.id = len(self.master.listOrchestrations)
        self.isplaying = False
        self.listStates = []
        self.listSensors = []

    def set_state(self, master):
        if master.entryName.get() != "":
            name = master.entryName.get()
            currentValue = master.comboValues.get()
            action = master.textAction.get("1.0","end")
                
            state = State(self, name, currentValue, action)
            self.listStates.append(state)
                
            master.textStates.configure(state='normal')
            master.textStates.insert(END, state.name + " = " + state.currentValue + "\n")
            master.textStates.configure(state='disabled')
            
            master.rootState.destroy()
    
    def set_sensor(self, master):
        sensor_name = master.comboBox.get()
        
        for sensor in master.master.listSensorsConfig:
            if sensor_name == sensor.name:
                self.listSensors.append(sensor)
                master.textSensors.configure(state='normal')
                master.textSensors.insert(END, sensor.name + " current value " + str(sensor.currentValue) + "\n")
                master.textSensors.configure(state='disabled')
        
        master.rootSensor.destroy()
        
    def save(self,master):
        #self.name
        self.transitions = master.textCode.get("1.0","end")
        master.master.listOrchestrations.append(self)
        master.rootOrches.destroy()
    
    def play(self):
        for sensor in self.listSensors:
            sensor.set_orchestration(self)        
        
        """ Evaluation of the FoxDot code of the active state (initial state) """
        for state in self.listStates:
            if state.currentValue == 'True':
                self.master.add_to_send_queue(MSG_EVALUATE_STRING(self.master.text.marker.id , state.action))
        self.isplaying = True
        print('Orchestration number '+ str(self.id) + " is playing")
        
    def getCode(self, listItems):
        """ Take a list of States or Transitions and a returns a python code in string form."""
        code = ""
        for item in listItems:
            code += item.name + " = " + str(item.currentValue) + "\n"          
        return code
    
    def update(self):
        """ Update of sensors and states value """
        loc = {}
        command = self.getCode(self.listSensors) + "\n" + self.getCode(self.listStates) + "\n" + self.transitions
        exec(command, globals(), loc)
        """ Get the new value of each state """
        for state in self.listStates:
            newValue = loc[state.name]
            state.update(newValue)

            
    def stop(self):
        for sensor in self.listSensors:
            sensor.delete_orchestration(self)
        self.isplaying=False
        
        
class State:
    def __init__(self, orchestration, name, currentValue, action):
        self.orchestration = orchestration
        self.name = name
        self.currentValue = currentValue
        self.action = action
    def update(self, newValue):
        """ Updates the value of the state, and if it becomes active, evaluates its FoxDot code (action). """
        if self.currentValue != newValue:
            self.currentValue = newValue
            if newValue == True:
                # Adds the FoxDot code to the queue to be sent to all clients.
                self.orchestration.master.add_to_send_queue(MSG_EVALUATE_STRING(self.orchestration.master.text.marker.id , self.action))

class Sensor:
    def __init__(self, master):
        self.master = master.master
        self.listOrchestrations = []
        self.name = master.entryLabelSensor.get()
    def play(self):
        print(self.name + 'listening \n')
    

class SensorGPIO(Sensor):
    def __init__(self, master):
        Sensor.__init__(self, master)
        self.gpioId = int(master.spinboxGPIO.get())

        #GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpioId, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.currentValue = GPIO.input(self.gpioId)
        
    def play(self, orchestration):
        GPIO.add_event_detect(self.gpioId, GPIO.BOTH, callback=orchestration.update, bouncetime = 75)
    
    def set_orchestration(self, orches):
        self.listOrchestrations.append(orches)
        self.play(orches)
    
    def delete_orchestration(self, orches):
        self.listOrchestrations.remove(orches)
        GPIO.remove_event_detect(self.gpioId)
        for orchestration in self.listOrchestrations:
            self.play(orchestration)

class SensorI2C(Sensor):
    def __init__(self, master, Id, data):
        Sensor.__init__(self, master)
        self.name = self.name + str(Id)
        self.data = data
        self.memo = numpy.zeros(lengthMemo)
        self.currentValue = 0
        self.play()
        
    def play(self):
        for j in range(lengthMemo):
            if self.data.value:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                self.memo[j]=1
            else:
                self.memo[j]=0
        
        value = numpy.mean(self.memo)
        if (value > seuil):
            value = 1
        else:
            value = 0
        if (value != self.currentValue):
            self.currentValue = value
            for orches in self.listOrchestrations:
                orches.update()
        
        self.master.root.after(5, self.play)
        
    def set_orchestration(self, orches):
        self.listOrchestrations.append(orches)
    def delete_orchestration(self, orches):
        self.listOrchestrations.remove(orches)