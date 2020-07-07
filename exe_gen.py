import cx_Freeze
import sys
from email.message import EmailMessage
import docx
import mongoengine
import tkinter
import smtplib
from docx.shared import Inches

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("App.py", base = base, icon='app.ico' )]

cx_Freeze.setup(
    name = "ActivityMonitor-Client",
    options = {"build_exe": {"packages":["tkinter","mongoengine", "docx", "Inches", "smtplib","EmailMessage"], "include_files": ['Data','Service','Plotting','app.ico']}},
    version = "0.1.0",
    description = "Engineering Shop Sign in System",
    executables = executables
)