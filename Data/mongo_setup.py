import mongoengine
from mongoengine import connect, disconnect_all


# This function hides all the noSQL magic in mongoengine behind an easily callable function.
# As is, this registers a connection with the local mongoDB client on the computer. Refer to
# the mongoengine docs to add a IPV4 field to connect to a specified computer or server
def global_init(Username, Password):
    DB_URI = f"mongodb+srv://{Username}:{Password}@cluster0-lbs9s.mongodb.net/beta0?retryWrites=true&w=majority"
    connect(host=DB_URI,alias='core')
def global_disconnect():
    disconnect_all()