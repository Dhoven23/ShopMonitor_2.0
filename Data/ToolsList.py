from Service.data_service import Create_Tool
from Data.mongo_setup import global_init
import os
import xlrd
loc = (f"{os.getcwd()}/ShopToolsList.xlsx")
import mongoengine
from mongoengine import connect
from mongoengine.connection import _get_db


book = xlrd.open_workbook(loc, on_demand=True)
sheet = book.sheet_by_index(0)
username = 'DHoven'
password = '12345'

DB_URI = f"mongodb+srv://{username}:{password}@cluster0-lbs9s.mongodb.net/beta0?retryWrites=true&w=majority"
connect(host=DB_URI,alias='core')
db = _get_db('core')
db.Tools.drop()

def update_tools():
    for i in range (1,sheet.nrows):
        name = str((sheet.cell_value(i, 1)))
        size = str(sheet.cell_value(i,2))
        toolname = name + ',' + size
        print(toolname)

        Create_Tool(toolname)

update_tools()




