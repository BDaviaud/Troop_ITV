from __future__ import absolute_import

try:
    from Tkinter import Menu
    import tkFileDialog
    import tkMessageBox
except ImportError:
    from tkinter import Menu
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
    
from functools import partial

from ..config import *
from ..message import *

class MenuBar(Menu):
    def __init__(self, master, visible=True):

        self.root = master

        Menu.__init__(self, master.root)

        # File menu

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="New Document",  command=self.new_file,   accelerator="Ctrl+N")
        filemenu.add_command(label="Save",          command=self.save_file,   accelerator="Ctrl+S")
        filemenu.add_command(label="Open",          command=self.open_file,   accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Start logging performance", command=lambda: "break")
        filemenu.add_command(label="Import logged performance", command=self.root.ImportLog)
        self.add_cascade(label="File", menu=filemenu)

        # Edit menu

        editmenu = Menu(self, tearoff=0)
        editmenu.add_command(label="Cut",        command=self.root.Cut,   accelerator="Ctrl+X")
        editmenu.add_command(label="Copy",       command=self.root.Copy,  accelerator="Ctrl+C")
        editmenu.add_command(label="Paste",      command=self.root.Paste, accelerator="Ctrl+V")
        editmenu.add_command(label="Select All", command=self.root.SelectAll,  accelerator="Ctrl+/")
        editmenu.add_separator()
        editmenu.add_command(label="Increase Font Size",      command=self.root.IncreaseFontSize, accelerator="Ctrl+=")
        editmenu.add_command(label="Decrease Font Size",      command=self.root.DecreaseFontSize, accelerator="Ctrl+-")
        editmenu.add_separator()
        editmenu.add_command(label="Toggle Menu", command=self.root.ToggleMenu, accelerator="Ctrl+M")
        editmenu.add_separator()
        editmenu.add_command(label="Edit Colours", command=self.root.EditColours)
        editmenu.add_checkbutton(label="Toggle Window Transparency",  command=self.root.ToggleTransparency, variable=self.root.transparent)
        self.add_cascade(label="Edit", menu=editmenu)

        # Code menu

        codemenu = Menu(self, tearoff=0)
        codemenu.add_command(label="Evaluate Code",         command=self.root.Evaluate,        accelerator="Ctrl+Return")
        codemenu.add_command(label="Evaluate Single Line",  command=self.root.SingleLineEvaluate,   accelerator="Alt+Return")
        codemenu.add_command(label="Stop All Sound",        command=self.root.stopSound,       accelerator="Ctrl+.")
        codemenu.add_command(label="Re-sync text",          command=self.root.syncText)
        codemenu.add_separator()

        # Allow choice of interpreter
        langmenu = Menu(self, tearoff=0)

        for name, interpreter in langnames.items():

            langmenu.add_checkbutton(label=langtitles[name],
                                     command  = partial(self.root.set_interpreter, interpreter),
                                     variable = self.root.interpreters[name])
            
        codemenu.add_cascade(label="Choose language", menu=langmenu)
        
        self.add_cascade(label="Code", menu=codemenu)

        # Creative constraint menu

        constraintmenu = Menu(self, tearoff=0)

        # Get the names of constraints

        from . import constraints
        constraints = vars(constraints)

        for name in constraints:

            if not name.startswith("_"):

                constraintmenu.add_checkbutton(label=name.title(),
                                           command  = partial(self.root.set_constraint, name),
                                           variable = self.root.creative_constraints[name])

        self.add_cascade(label="Constraints", menu=constraintmenu)        

        # Help

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="Documentation",   command=self.root.OpenGitHub)
        self.add_cascade(label="Help", menu=helpmenu)

        # Add to root

        self.visible = visible
        
        if self.visible:
            
            master.root.config(menu=self)

    def toggle(self):
        self.root.root.config(menu=self if not self.visible else 0)
        self.visible = not self.visible
        return

    def save_file(self, event=None):
        """ Opens a save file dialog """
        lang_files = ("{} file".format(repr(self.root.lang)), self.root.lang.filetype )
        all_files = ("All files", "*.*")
        fn = tkFileDialog.asksaveasfilename(title="Save as...", filetypes=(lang_files, all_files), defaultextension=lang_files[1])
        if len(fn):
            with open(fn, "w") as f:
                f.write(self.root.text.read())
            print("Saved: {}".format(fn))
        return

    def new_file(self, event=None):
        """ Asks if the user wants to clear the screen and does so if yes """
        return

    def open_file(self, event=None):
        """ Opens a fileopen dialog then sets the text box contents to the contents of the file """
        lang_files = ("{} files".format(repr(self.root.lang)), self.root.lang.filetype )
        all_files = ("All files", "*.*")
        fn = tkFileDialog.askopenfilename(title="Open file", filetypes=(lang_files, all_files))
        
        if len(fn):

            with open(fn) as f:
                contents = f.read()

            this_peer = self.root.text.marker.id

            messages = [ MSG_SELECT(this_peer, "1.0", self.root.text.index("end")),
                         MSG_SET_MARK(this_peer, 1, 0),
                         MSG_BACKSPACE(this_peer, 1, 0),
                         MSG_INSERT(this_peer, contents, 1, 0) ]

            self.root.push_queue_put( messages, wait=True)

        return