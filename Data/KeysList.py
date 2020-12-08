from Data.key import Key

RM130_keys = {
    1: "HAAS",
    2: "SHARP MILL\n SURFACE GRINDER",
    3: "TRAK CNC MILL",
    4: "TRAK LATHE",
    5: "HORIZ BAND SAW",
    6: "IRON WORKER",
    7: "VERT BAND SAW",
    8: "COLD SAW",
    9: "FLOOR DRILL PRESS",
    10: "ENDMILL TOOLBOX",
    11: "HAAS PANELS",
}
RM132_keys = {

	12: "PLANER",
    13: "DISC SANDER",
    14: "JOINTER",
    15: "SPINDLE SANDER",
    16: "TABLE SAW",
    17: "MITER SAW",
    18: "FLOOR DRILL PRESS",
    19: "VERT BAND SAW",
    20: "WOOD LATHE",
    21: "WOOD SHOP \nCABINETS"
}
RM131_keys = {
    22: "BENCH GRINDER",
    23: "PLASMA CUTTER",
    24: "TABLE DRILL PRESS",
    25: "MIG WELDER",
    26: "WELDING SHOP\n CABINETS",
}


from Data.mongo_setup import global_init

username = str(input("Username?\n"))
password = str(input("Password?\n"))

global_init(username,password)


def update_keyslist():
    Key.objects.delete()
    for n in RM130_keys:
        print(str(n) + ': ' + RM130_keys[n])
        key = Key()
        key.name = RM130_keys[n]
        key.keyNumber = n
        key.RoomNumber = '130'
        key.save()

    for n in RM131_keys:
        print(str(n) + ': ' + RM131_keys[n])
        key = Key()
        key.name = RM131_keys[n]
        key.keyNumber = n
        key.RoomNumber = '131'
        key.save()

    for n in RM132_keys:
        print(str(n) + ': ' + RM132_keys[n])
        key = Key()
        key.name = RM132_keys[n]
        key.keyNumber = n
        key.RoomNumber = '132'
        key.save()


