import mongoengine


class Key(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    keyNumber = mongoengine.IntField(required=True)
    RoomNumber = mongoengine.StringField(default=None)


    meta = {
        'db_alias': 'core',
        'collection': 'Keys'
    }