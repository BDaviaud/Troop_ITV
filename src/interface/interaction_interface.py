from __future__ import absolute_import

#from ..message import *
#import random
#import re as regex
#from FoxDot import *
#import time
#import numpy
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_mpr121
from .orchestration import *

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter import ttk
    
class IOrchestration:
    """ Class for displaying and managing Orchestration """
    def __init__(self, master):
        self.master = master
        self.rootMain = Toplevel(master.root) # Popup -> Toplevel()
        self.rootMain.title('Orchestrations')
        self.rootMain.geometry('350x120')
        self.rootMain.grab_set() # Interaction with main window impossible
        self.demo()
        listId = []
        for orches in self.master.listOrchestrations:
            listId.append(orches.id)
        comboBox = ttk.Combobox(self.rootMain, values=listId)
        comboBox.place(x=10, y=10)
        
        Button(self.rootMain, text="New", command=self.newOrchestration).place(x=270, y=10)
        Button(self.rootMain, text="Import", state= DISABLED).place(x=270, y=45)
        Button(self.rootMain, text="Show", command=lambda:self.showOrchestration(int(comboBox.get()))).place(x=270, y=80)
        
    
    def newOrchestration(self):
        self.rootMain.destroy()
        self.rootOrches = Toplevel(self.master.root) # Popup -> Toplevel()
        self.rootOrches.title('Orchestration')
        self.rootOrches.geometry('520x450')
        self.rootOrches.grab_set() # Interaction with main window impossible
        
        orchestration = Orchestration(self)
        
        # List of implemented states
        Label(self.rootOrches, text='States:').place(x=260, y=10)
        self.textStates = Text(self.rootOrches, height=10, width=30)
        self.textStates.place(x=260, y=40)
        self.textStates.configure(state='disabled')
        Button(self.rootOrches, text="Add State", command=lambda: self.newState(orchestration)).place(x=415, y=10)
        ### liste des capteurs et leurs entrées
        
        #self.listInputSensor = [SensorCAP('p0'),SensorCAP('p1'),SensorCAP('p2'),SensorCAP('p3'),SensorCAP('p4'),SensorCAP('p5'),SensorCAP('p6'),SensorCAP('p7'),SensorCAP('p8'),SensorCAP('p9'), SensorCAP('p10'),SensorCAP('p11')]
        self.listInputSensor =[]
        ### Popup Interface
        # Input for the python code 
        Label(self.rootOrches, text='Code:').place(x=10, y=10)
        self.textCode = Text(self.rootOrches, height=20, width=30)
        self.textCode.place(x=10, y=40)
        
        # List of implemented sensors
        Label(self.rootOrches, text='Sensors:').place(x=260, y=230)
        self.textSensors = Text(self.rootOrches, height=10, width=30)
        self.textSensors.place(x=260, y=260)
        self.textSensors.configure(state='disabled')
        Button(self.rootOrches, text="Add Sensor", command=lambda: self.addSensor(orchestration)).place(x=380, y=230)
        
        Button(self.rootOrches, text="Save", command=lambda: orchestration.save(self)).place(x=100, y=400)
        
    def newState(self, orchestration):
        self.rootState = Toplevel(self.rootOrches) # Popup
        self.rootState.title('Add a state')
        self.rootState.geometry('360x350')
        self.rootState.grab_set()
        
        # State name
        Label(self.rootState, text='Name :').place(x=10, y=10)
        self.entryName = Entry(self.rootState)
        self.entryName.place(x=150, y=10)

        # Sate inital value
        Label(self.rootState, text='Initial value :').place(x=10, y=50)
        self.comboValues = ttk.Combobox(self.rootState, values=["False", "True"])
        self.comboValues.current(0)
        self.comboValues.place(x=150, y=50)
        
        # Action
        Label(self.rootState, text='FoxDot Code:').place(x=10, y=90)
        self.textAction = Text(self.rootState, width=40, height=10)
        self.textAction.place(x=10, y=120)
        
        # Buttons
        btnCancel = Button(self.rootState, text='Cancel', command=self.rootState.destroy)
        btnCancel.place(x=10, y=310)

        btnSave = Button(self.rootState, text='Save', command=lambda: orchestration.set_state(self))
        btnSave.place(x=270, y=310)
        
    def addSensor(self, orchestration):
        self.rootSensor = Toplevel(self.rootOrches) # Popup
        self.rootSensor.title('Add a sensor')
        self.rootSensor.geometry('360x150')
        self.rootSensor.grab_set()
        
        listSensorsName = []
        for sensor in self.master.listSensorsConfig:
            listSensorsName.append(sensor.name)
        self.comboBox = ttk.Combobox(self.rootSensor, values=listSensorsName)
        self.comboBox.place(x=10, y=10)
         
        # Buttons
        btnCancel = Button(self.rootSensor, text='Cancel', command=self.rootSensor.destroy)
        btnCancel.place(x=10, y=100)

        btnSave = Button(self.rootSensor, text='Add', command=lambda: orchestration.set_sensor(self))
        btnSave.place(x=270, y=100)
        
    def showOrchestration(self, orchestration_id):
        if orchestration_id != "":
            self.rootMain.destroy()
            self.rootOrches = Toplevel(self.master.root) # Popup -> Toplevel()
            self.rootOrches.title('Orchestration')
            self.rootOrches.geometry('520x450')
            self.rootOrches.grab_set() # Interaction with main window impossible
            
            orchestration = self.master.listOrchestrations[orchestration_id]
            
            # List of implemented states
            Label(self.rootOrches, text='States:').place(x=260, y=10)
            self.textStates = Text(self.rootOrches, height=10, width=30)
            self.textStates.place(x=260, y=40)
            for state in orchestration.listStates:
                self.textStates.insert(END, state.name + " = " + str(state.currentValue) + "\n")
            self.textStates.configure(state='disabled')
            
            # Input for the python code 
            Label(self.rootOrches, text='Code:').place(x=10, y=10)
            self.textCode = Text(self.rootOrches, height=20, width=30)
            self.textCode.place(x=10, y=40)
            self.textCode.insert(END, orchestration.transitions)
            self.textCode.configure(state='disabled')
            
            # List of implemented sensors
            Label(self.rootOrches, text='Sensors:').place(x=260, y=230)
            self.textSensors = Text(self.rootOrches, height=10, width=30)
            self.textSensors.place(x=260, y=260)
            for sensor in orchestration.listSensors:
                self.textSensors.insert(END, sensor.name + " current value " + str(sensor.currentValue) + "\n")
            self.textSensors.configure(state='disabled')
            
            if orchestration.isplaying:
                Button(self.rootOrches, text="Stop", command=orchestration.stop).place(x=100, y=400)
            else:
                Button(self.rootOrches, text="Play", command=orchestration.play).place(x=100, y=400)
                
    def demo(self):
        if not(self.master.listOrchestrations):
            #orchestration = Orchestration(self)
            #orchestration.listStates = [State(self, 'E0', True, ''),State(self, 'E1', False, 'p1 >> play("x-o{-[--][-o][---]}")'),State(self, 'E1b', False, 'p1 >> play("x-o{o[--][-o][---]}")'),State(self, 'E2', False, 'p2 >> pluck([0,1,2,[3,7,5]], chop=4, amp=0.5, dur=1)'),State(self, 'E2b', False, 'p2 >> pluck([0,2,3,1,[4,6]], chop=4, amp=0.5, dur=1)'),State(self, 'E3', False, 'p3 >> blip(oct=4, dur=[1/2, 1/2, 1/4])'),State(self, 'E3b', False, 'p3 >> blip(oct=3, dur=[1/2, 1/2, 1/4])'),State(self, 'E4', False, 'Clock.clear()'), State(self, 'memo1', True, ''), State(self, 'memo2', True, ''),State(self, 'memo3', True, '')]
            #orchestration.listSensors = self.master.listSensorsConfig
            #orchestration.transitions = "if E0 and e0 and memo1:\n\tE0 = False\n\tE1 = True\n\nif E0 and e0 and not memo1:\n\tE0 = False\n\tE1b = True\n\nif E1 and not e0 and memo1:\n\tmemo1 = False\n\tE1 = False\n\tE0 = True\n\nif E1b and not e0 and not memo1:\n\tmemo1 = True\n\tE1b = False\n\tE0 = True\n\nif E0 and e1 and memo2:\n\tE0 = False\n\tE2 = True\n\nif E0 and e1 and not memo2:\n\tE0 = False\n\tE2b = True\n\nif E2 and not e1 and memo2:\n\tmemo2 = False\n\tE2 = False\n\tE0 = True\n\nif E2b and not e1 and not memo2:\n\tmemo2 = True\n\tE2b = False\n\tE0 = True\n\nif E0 and e2 and memo3:\n\tE0 = False\n\tE3 = True\n\nif E0 and e2 and not memo3:\n\tE0 = False\n\tE3b = True\n\nif E3 and not e2 and memo3:\n\tmemo3 = False\n\tE3 = False\n\tE0 = True\n\nif E3b and not e2 and not memo3:\n\tmemo3 = True\n\tE3b = False\n\tE0 = True\n\nif E0 and e3:\n\tE0 = False\n\tE4 = True\n\nif E4 and not e3:\n\tE4 = False\n\tE0 = True"
            #self.master.listOrchestrations.append(orchestration)
            
            ### DEMO CAP
            orchestration = Orchestration(self)
            orchestration.listStates = [State(self, 'State0', True, ''),
                                        State(self, 'State1', False, 'm2 >> benoit(P[0, -1, 2, -3,4,None,-2].layer("reverse").offadd(0),amp=0.2, sus=0.2, dur=0.5, oct=3)'),
                                        State(self, 'State2', False, 'm2 >> benoit(P[0, -1, 2, -3,4,None,-2].layer("reverse").offadd(5),amp=0.2, sus=0.2, dur=0.5, oct=3)'),
                                        State(self, 'State3', False, 'm3 >> bounce(P[(-2,), (-10, 2)].zip([2,-4]),dur=[2, 2],amp=0.2,oct=P[4,3].stutter([2,4]),sus=2)'),
                                        State(self, 'State4', False, 'm3 >> bounce(P[(-2,), (-10, 2)].zip([2,5]),dur=[2, 2],amp=0.2,oct=P[4,3].stutter([2,4]),sus=2)'),
                                        State(self, 'State5', False, 'm4 >> glitchbass(P[4,6,5,None,5].layer("reverse").offadd(0),dur=P[1,0.5,0.5,1,0.5,0.5].stutter([2,3,2,3,2]), oct=P[3,4,3,4,3],amp=P[0.5,0,0.5,0,0.5].zip([0.2,0]))'),
                                        State(self, 'State6', False, 'm4 >> glitchbass(P[4,6,5,None,5].layer("reverse").offadd(0),dur=P[1,0.5,0.5,1,0.5,0.5].stutter([2,3,2,3,2]), oct=P[3,4,3,4,3],amp=P[0.5,0,0.5,0,0.5].zip([0.5,0.75]))'),
                                        State(self, 'State7', False, 'm2.penta()'),
                                        State(self, 'State8', False, 'm2.penta(0)'),
                                        State(self, 'State9', False, 'Clock.clear()'),
                                        State(self, 'memo1', True, ''),
                                        State(self, 'memo2', True, ''),
                                        State(self, 'memo3', True, ''),
                                        State(self, 'memo4', True, '')]
            orchestration.listSensors = self.master.listSensorsConfig
            orchestration.transitions = "if State0 and CAP0 and memo1:\n\tState0 = False\n\tState1 = True\n\tmemo1 = False\n\nif State1 and not CAP0:\n\tState1 = False\n\tState0 = True\n\nif State0 and CAP0 and not memo1:\n\tState0 = False\n\tState2 = True\n\tmemo1 = True\n\nif State2 and not CAP0:\n\tState2 = False \n\tState0 = True \n\nif State0 and CAP1 and memo2: \n\tState0 = False \n\tState3 = True \n\tmemo2 = False \n\nif State3 and not CAP1:\n\tState3 = False\n\tState0 = True\n\nif State0 and CAP1 and not memo2:\n\tState0 = False \n\tState4 = True \n\tmemo2 = True \n\nif State4 and not CAP1: \n\tState4 = False \n\tState0 = True \n\nif State0 and CAP2 and memo3:\n\tState0 = False \n\tState5 = True\n\tmemo3 = False\n\nif State5 and not CAP2:\n\tState5 = False \n\tState0 = True \n\nif State0 and CAP2 and not memo3: \n\tState0 = False \n\tState6 = True \n\tmemo3 = True \n\nif State6 and not CAP2: \n\tState6 = False \n\tState0 = True \n\nif State0 and CAP3 and memo4: \n\tState0 = False \n\tState7 = True \n\tmemo4 = False \n\nif State7 and not CAP3: \n\tState7 = False \n\tState0 = True \n\nif State0 and CAP3 and not memo4:\n\tState0 = False \n\tState8 = True \n\tmemo4 = True \n\nif State8 and not CAP3: \n\tState8 = False \n\tState0 = True \n\nif State0 and CAP4: \n\tState0 = False \n\tState9 = True \n\nif State9 and not CAP4: \n\tState9 = False \n\tState0 = True \n\n"
            self.master.listOrchestrations.append(orchestration)
            """### DEMO 2
            orchestration = Orchestration(self)
            orchestration.listStates = [State(self, 'State0b', True, 'm2.solo(0)\nm3.solo(0)\nm4.solo(0)'),
                                        State(self, 'State1b', False, 'm2.solo()'),
                                        State(self, 'State2b', False, 'm3.solo()'),
                                        State(self, 'State3b', False, 'm4.solo()')]
            orchestration.listSensors = self.master.listSensorsConfig
            orchestration.transitions = "if State0b and CAP11:\n\tState0b = False\n\tState1b = True\n\nif State1b and not CAP11:\n\tState1b = False\n\tState0b = True\n\nif State0b and CAP10:\n\tState0b = False\n\tState2b = True\n\nif State2b and not CAP10:\n\tState2b = False\n\tState0b = True\n\nif State0b and CAP9:\n\tState0b = False\n\tState3b = True\n\nif State3b and not CAP9:\n\tState3b = False\n\tState0b = True\n\n"
            self.master.listOrchestrations.append(orchestration)"""
        
        
class ISensor():
    def __init__(self, master):
        self.master = master
        self.root = Toplevel(master.root)
        self.root.title('Sensor')
        self.root.geometry('350x120')
        self.root.grab_set()
        
        #Add a scollbar
        scroll = Scrollbar(self.root, orient='vertical')
        scroll.pack(side=RIGHT, fill='y')
        
        
        self.textSensors = Text(self.root, height=10, width=30, yscrollcommand=scroll.set)
        scroll.config(command=self.textSensors.yview) #attach the scrollbar with the text widget
        self.textSensors.place(x=10, y=10)
        for sensor in master.listSensorsConfig:
            self.textSensors.insert(END, sensor.name + "\n")
        self.textSensors.configure(state='disabled')
        
        Button(self.root, text="New", command=self.newSensor).place(x=270, y=10)
        
    def newSensor(self):
        self.rootSensor = Toplevel(self.root) # Popup
        self.rootSensor.title('Add a sensor')
        self.rootSensor.geometry('360x150')
        self.rootSensor.grab_set()
        
        self.choice = IntVar()
        self.string_var = StringVar()
        self.string_var.set("Choose gpio or i2c.")
        
        check_gpio = Radiobutton(self.rootSensor, text='GPIO', variable=self.choice, value=1, command=self.config_sensor)
        check_gpio.place(x=10, y=10)

        check_i2c = Radiobutton(self.rootSensor, text='I2C', variable=self.choice, value=2, command=self.config_sensor)
        check_i2c.place(x=90, y=10)
        
        self.labelSensor = Label(self.rootSensor, textvariable = self.string_var).place(x=10, y=70)
        
        # Sensor label
        Label(self.rootSensor, text='Label :').place(x=10, y=40)
        self.entryLabelSensor = Entry(self.rootSensor)
        self.entryLabelSensor.place(x=160, y=40)
         
        # Buttons
        btnCancel = Button(self.rootSensor, text='Cancel', command=self.rootSensor.destroy)
        btnCancel.place(x=10, y=100)
        btnSave = Button(self.rootSensor, text='Save', command=self.set_sensor)
        btnSave.place(x=270, y=100)

        
    def config_sensor(self):
        if self.choice.get() == 1:            
            # Pin number for GPIO input
            self.string_var.set("Input pin GPIO :")
            self.spinboxGPIO = Spinbox(self.rootSensor, from_=1, to=40)
            self.spinboxGPIO.place(x=160, y=70)
            
        elif self.choice.get() == 2:
            # Addrress I2C
            listAddr = ['0x5a', '0x5b', '0x5c']
                
            self.string_var.set('Choose a address :')
            self.ComboAddr = ttk.Combobox(self.rootSensor, values=listAddr)
            self.ComboAddr.current(0)
            self.ComboAddr.place(x=160, y=70)
    def set_sensor(self):
        if self.choice.get() == 1:
            sensor = SensorGPIO(self)
            
            self.master.listSensorsConfig.append(sensor)
        
            self.textSensors.configure(state='normal')
            self.textSensors.insert(END, sensor.name + "\n")
            self.textSensors.configure(state='disabled')
        elif self.choice.get() == 2:
            address = int(self.ComboAddr.get(), 16)
            # Create MPR121 object.
            i2c = busio.I2C(board.SCL, board.SDA)
            mpr121 = adafruit_mpr121.MPR121(i2c,address=address)
            for i in range(12):
                sensor = SensorI2C(self, i, mpr121[i])
                self.master.listSensorsConfig.append(sensor)
        
                self.textSensors.configure(state='normal')
                self.textSensors.insert(END, sensor.name + "\n")
                self.textSensors.configure(state='disabled')
            
        self.rootSensor.destroy()