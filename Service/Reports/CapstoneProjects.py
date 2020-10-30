# Reading an excel file using Python
import xlrd
import os
# Give the location of the file
loc = (f"{os.getcwd()}/Capstone Projects 9-2-2020.xlsx")


wb = xlrd.open_workbook(loc,on_demand=True)
sheet = wb.sheet_by_index(0)
def get_group_info(i):

    i = int(i)
    message = ("you are in the " + sheet.cell_value((i*4), 1) + "\nproject with " + sheet.cell_value((i*4), 4))
    return message

def get_cell_equals(string):
    i = 0
    while True:

        if sheet.cell_value(i,2) == string:
            print(sheet.cell_value(i, 0))
            return sheet.cell_value(i,0)

        else:
            i+=1



