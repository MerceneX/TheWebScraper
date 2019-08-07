import json
from JSONReader import JSONReader


wantedGroup = "NatashaMath"


class Subscriber:
    fileLocation = "Data/SubscriberGroups.json"
    @classmethod
    def generateSubscribersList(cls, wantedGroup):
        subscribersList = list()
        data = JSONReader.readJSON(
            JSONReader.stringFromFile(Subscriber.fileLocation))
        for group in data["Groups"]:
            if(group["Name"] == wantedGroup):
                for sub in group["Subscribers"]:
                    subscribersList.append(Subscriber(
                        sub['Name'], sub['Surname'], sub['Email']))
                break
        return subscribersList

    @classmethod
    def generateSubscribersMailingList(cls, subscribersList):
        subscribersMailingList = list()
        for sub in subscribersList:
            subscribersMailingList.append(sub.email)

        return subscribersMailingList

    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
