import mongoengine
from mongoengine import connect, disconnect_all

db_name='beta0'

def global_init(Username, Password):
    DB_URI = f"mongodb+srv://{Username}:{Password}@cluster0-lbs9s.mongodb.net/{db_name}?retryWrites=true&w=majority"
    connect(host=DB_URI,alias='core')
def global_disconnect():
    disconnect_all()