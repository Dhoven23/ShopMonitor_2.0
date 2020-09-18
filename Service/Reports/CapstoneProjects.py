# Reading an excel file using Python
import xlrd

# Give the location of the file
loc = ("~/Desktop/FinishedShopApp/venv/TempSource/Service/Reports/Capstone Projects 9-2-2020.xlsx")


wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
def get_group_info(i):

    i = int(i)
    message = ("you are in the " + sheet.cell_value((i*4), 1) + "\nproject with " + sheet.cell_value((i*4), 4))
    return message

