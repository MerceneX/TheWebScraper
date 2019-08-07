import json
import requests
from bs4 import BeautifulSoup
from JSONReader import JSONReader
from SubscriberGroups import Subscriber


class Website:
    locationFile = "Data/Websites.json"
    @classmethod
    def checkDuplicateURL(cls, element, iterable):
        for listed in iterable:
            if(str(listed.url) == str(element)):
                return True
        return False

    @classmethod
    def sessionLogin(cls):
        try:
            session = requests.Session()
            return session
        except:
            return True

    @classmethod
    def sessionClose(clas, session):
        try:
            session.close()
            return False
        except:
            return True

    def __init__(self, name, url):
        self.name = name
        self.url = url


class LoginWebsite(Website):
    @classmethod
    def generateList(cls):
        sites = JSONReader.readJSON(
            JSONReader.stringFromFile(Website.locationFile))
        loginSitesList = list()
        for site in sites["Websites"]["login"]:
            if(Website.checkDuplicateURL(site["url"], loginSitesList)):
                continue
            loginSitesList.append(LoginWebsite(
                site["name"], site["url"], site["id"], site["payload"]))
        loginSitesList = LoginWebsite.garbageCollection(loginSitesList)
        return loginSitesList

    @classmethod
    def garbageCollection(cls, loginSitesList):
        sites = JSONReader.readJSON(
            JSONReader.stringFromFile(Website.locationFile))
        sitesURL = list()
        for site in sites["Websites"]["login"]:
            sitesURL.append(site["url"])
        for site in loginSitesList:
            if(ScrapableWebsite.checkURLs(site.url, sitesURL)):
                continue
            else:
                loginSitesList.remove(site)
        return loginSitesList

    @classmethod
    def checkURLs(self, url, sitesURL):
        for siteURL in sitesURL:
            if(url == siteURL):
                return True
        return False

    def sessionLogin(self):
        try:
            session = requests.Session()
            session.post(self.url, data=self.payload)
            return session
        except:
            return True

    def __init__(self, name, url, idd, payload):
        super().__init__(name, url)
        self.payload = payload
        self.id = idd


class ScrapableWebsite(Website):
    @classmethod
    def generateList(cls, scrapableSitesList):
        sites = JSONReader.readJSON(
            JSONReader.stringFromFile(Website.locationFile))
        for site in sites["Websites"]["scrapable"]:
            if(Website.checkDuplicateURL(site["url"], scrapableSitesList)):
                continue
            scrapableSitesList.append(ScrapableWebsite(
                site["name"], site["url"], site["searchFor"], site["group"], 1, site["subject"], site["message"]))
        scrapableSitesList = ScrapableWebsite.garbageCollection(
            scrapableSitesList)
        return scrapableSitesList

    @classmethod
    def garbageCollection(cls, scrapableSitesList):
        sites = JSONReader.readJSON(
            JSONReader.stringFromFile(Website.locationFile))
        sitesURL = list()
        for site in sites["Websites"]["scrapable"]:
            sitesURL.append(site["url"])
        for site in scrapableSitesList:
            if(ScrapableWebsite.checkURLs(site.url, sitesURL)):
                continue
            else:
                scrapableSitesList.remove(site)
        return scrapableSitesList

    @classmethod
    def checkURLs(self, url, sitesURL):
        for siteURL in sitesURL:
            if(url == siteURL):
                return True
        return False

    def getData(self, loginSitesList):
        if(self.login == 0):
            session = Website.sessionLogin()
            if(session == True):
                return True
            content = self.searchContent(session)
            if(content == True):
                return True
            if(Website.sessionClose(session) == True):
                return True
            return content
        for site in loginSitesList:
            if(site.id == self.login):
                session = site.sessionLogin()
                if(session == True):
                    return True
                content = self.searchContent(session)
                if(content == True):
                    return True
                if(site.sessionClose(session) == True):
                    return True
                break

        return content

    def newPageRequest(self, loginSitesList):
        content = self.getData(loginSitesList)
        if(content == True):
            return True
        self.currentState = content
        return False

    def searchContent(self, session):
        try:
            return BeautifulSoup(session.get(self.url).content, "html.parser",
                                 from_encoding="utf-8").select_one(self.search)
        except:
            return True

    def compareStates(self, loginSitesList, mailman):
        content = self.getData(loginSitesList)
        if(content == True):
            return True
        if(self.currentState.text != content.text):
            print("change on this site {0}".format(self.name))
            subsList = Subscriber.generateSubscribersMailingList(
                Subscriber.generateSubscribersList(self.group))
            mailman.sendEmail(subsList, self)
            self.currentState = content
        else:
            print("{0} site in the same state".format(self.url))
        return False

    def __init__(self, name, url, search, group, login, subject, message):
        super().__init__(name, url)
        self.search = search
        self.login = login
        self.group = group
        self.currentState = " "
        self.subject = subject
        self.message = message
