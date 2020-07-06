import mongoengine


# This function hides all the noSQL magic in mongoengine behind an easily callable function.
# As is, this registers a connection with the local mongoDB client on the computer. Refer to
# the mongoengine docs to add a IPV4 field to connect to a specified computer or server
def global_init():
    mongoengine.register_connection(alias='core', name='Shop_database')
