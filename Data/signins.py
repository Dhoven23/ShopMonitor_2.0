import mongoengine


# This embedded document class stores the individual login events not processed by the Student class.
# mainly used for analytics, and to check who was in the shop at a given time.
# Don't edit unless you want to port over all existing events. All input args must be type str.
class Signin(mongoengine.EmbeddedDocument):
    Login = mongoengine.StringField(required=True)
    Logout = mongoengine.StringField(default='Still Signed In')
    StudentID = mongoengine.StringField(required=True)
