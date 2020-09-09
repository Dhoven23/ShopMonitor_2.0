from Data.mongo_setup import global_init,disconnect_all
from mongoengine import connect
global_init("DHoven","12345")

DB_URI = f"mongodb+srv://DHoven:12345@cluster0-lbs9s.mongodb.net/beta1?retryWrites=true&w=majority"
connect(host=DB_URI,alias='core2')

disconnect_all()

