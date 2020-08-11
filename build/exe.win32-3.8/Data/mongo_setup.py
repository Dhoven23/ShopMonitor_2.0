import mongoengine
from mongoengine import connect


# This function hides all the noSQL magic in mongoengine behind an easily callable function.
# As is, this registers a connection with the local mongoDB client on the computer. Refer to
# the mongoengine docs to add a IPV4 field to connect to a specified computer or server
def global_init():
    DB_URI = "mongodb+srv://DHoven:12345@cluster0-lbs9s.mongodb.net/test?retryWrites=true&w=majority"
    connect(host=DB_URI,alias='core')
