import time
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from SubscriberGroups import Subscriber
from Websites import LoginWebsite, ScrapableWebsite
from Notificator import Notificator

#senderMail = input("Please enter the email for sending notifications:\n")
senderMail = "marko.mx.gluhak@gmail.com"
#senderPassword = getpass("Please enter the password:\n")
senderPassword = "jB2p9&qSyi#l"
mailman = Notificator(senderMail, senderPassword)
scrapableSitesList = list()
while(True):
    scrapableSitesList = ScrapableWebsite.generateList(scrapableSitesList)
    loginSitesList = LoginWebsite.generateList()
    for site in scrapableSitesList:
        if(site.currentState == " "):
            if(site.newPageRequest(loginSitesList) == True):
                break
            print("Added new site")
        else:
            if(site.compareStates(loginSitesList, mailman) == True):
                break
            pass
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print("\n****************  {0}  *****************\n".format(timestamp))
    time.sleep(300)
print("How the fuck did I get here?")
