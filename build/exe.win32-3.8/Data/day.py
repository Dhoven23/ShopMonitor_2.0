import datetime
import mongoengine

# ----------------------------------------------------------------------------------------------
# This is the class that stores all necessary information for a given day in the shop.
# It contains easy to understand function handles to dynamically update the logs
# If you intend to edit this class (or any database class) please change the collection
# name at the end to a temporary bin until you are ready to port over all the data logs
# to the new format.
# -----------------------------------------------------------------------------------------------

from Data.signins import Signin


class Day(mongoengine.Document):
    # defines the day for each class instance. Only use the YYYY-MM-DD format as input
    date = mongoengine.StringField(required=True)
    # defines the hour that the day was initialized. This is for analytic purposes
    Begin = mongoengine.IntField(required=True)
    # The list of users per hour. This is an intuitive list for plotting data
    hourly = mongoengine.ListField(required=False)
    # the total number of daily users
    logs = mongoengine.IntField(default=0)
    # the embedded document class handle for the class 'Signin'
    signins = mongoengine.EmbeddedDocumentListField(Signin)

    # This function increments the number of daily users each time it is called
    def increment(self):
        self.logs = self.logs + 1
        self.save()

    # This function increments the hourly users, and handles multi-hour breaks between sign-in events.
    def hourly_entry_add(self):
        hour = int(datetime.datetime.now().hour - self.Begin)

        if not self.hourly:
            self.hourly.append('0')

        last = self.hourly[-1]

        if hour == len(self.hourly) - 1:
            self.hourly[-1] = str(int(self.hourly[-1]) + 1)

        if hour > len(self.hourly) - 1:
            while hour > len(self.hourly) - 1:
                self.hourly.append(last)
            self.hourly[-1] = str(int(self.hourly[-1]) + 1)

        self.save()

    # This function decrements the number of hourly users
    def hourly_entry_rmv(self):
        hour = int(datetime.datetime.now().hour - self.Begin)

        if self.hourly:
            last = self.hourly[-1]

            if hour == len(self.hourly) - 1:
                self.hourly[-1] = str(int(self.hourly[-1]) - 1)

            if hour > len(self.hourly) - 1:
                while hour > len(self.hourly) - 1:
                    self.hourly.append(last)
                self.hourly[-1] = str(int(self.hourly[-1]) - 1)

            self.save()

    meta = {
        'db_alias': 'core',
        'collection': 'Logs'
    }
