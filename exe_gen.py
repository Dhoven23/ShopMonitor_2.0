import cx_Freeze
import sys
import mongoengine
import tkinter

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("App.py", base = base, icon='app.ico' )]

cx_Freeze.setup(
    name = "ActivityMonitor-Client",
    options = {"build_exe": {"packages":["tkinter","mongoengine"], "include_files": ['Data','Service','app.ico']}},
    version = "0.1.0",
    description = "Engineering Shop Sign in System",
    executables = executables
)