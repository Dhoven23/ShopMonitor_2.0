import mongoengine

class Usage(mongoengine.EmbeddedDocument):
    checkout_time = mongoengine.StringField(required=True)
    checkout_ID = mongoengine.StringField(required=True)
    return_time = mongoengine.StringField(default='In Use')
    ReturnDateExpect = mongoengine.StringField(required=True)