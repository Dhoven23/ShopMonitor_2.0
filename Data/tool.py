import mongoengine

from Data.usages import Usage

class Tool(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    size = mongoengine.StringField(required=True)
    usages = mongoengine.EmbeddedDocumentListField(Usage)


    meta = {
        'db_alias': 'core',
        'collection': 'Tools'
    }

