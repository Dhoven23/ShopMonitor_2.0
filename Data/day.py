import datetime
import mongoengine

from Data.signins import Signin

class Day(mongoengine.Document):

    date = mongoengine.StringField(required=True)

    Begin = mongoengine.IntField(required=True)

    hourly = mongoengine.ListField(required=False)

    logs = mongoengine.IntField(default=0)

    capstone_logs = mongoengine.IntField(default=0)

    signins = mongoengine.EmbeddedDocumentListField(Signin)

    def increment(self):
        self.logs = self.logs + 1
        self.save()

    def increment_capstone(self):
        self.capstone_logs = self.capstone_logs + 1
        self.save()

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
