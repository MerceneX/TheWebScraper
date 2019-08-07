import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from SubscriberGroups import Subscriber
from Websites import LoginWebsite, ScrapableWebsite


class Notificator:

    def sendEmail(self, receivers, website):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['Subject'] = website.subject
        msg.attach(MIMEText("{0}\n{1}".format(
            website.message, website.url), 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        text = msg.as_string()
        for receiver in receivers:
            msg['To'] = receiver
            server.sendmail(self.sender, receiver, text)
            print("Message sent to: " + receiver)
        server.quit()

    def __init__(self, sender, password):
        self.sender = sender
        self.password = password
