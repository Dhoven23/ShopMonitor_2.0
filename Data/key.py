
import mongoengine


# ----------------------------------------------------------------------------------------------------
# This is the individual Student class that stores all non-time-sensitive information about a student
# It is meant to be an easy document to interact with, as it is mostly static, except for the boolean
# that indicates to the login service that a student is in the shop
# ----------------------------------------------------------------------------------------------------


class Key(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    keyNumber = mongoengine.IntField(required=True)


    meta = {
        'db_alias': 'core',
        'collection': 'Keys'
    }