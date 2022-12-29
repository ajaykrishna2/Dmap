import smtplib
import configparser
import os
from g_ads4.g_ads import *
configuration_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuration_path)
email_user = config['Email']['gmail_user']
email_password = config['Email']['gmail_password']
sent_from = email_user
to = ['ajay.panku2@gmail.com']
subject = 'Google_ads_automation_status'
body = 'Extracted the google analytics data of '+str(time_date()[0])+' and insertion completed to the database successfully on :'+str(time_date()[1])

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
def email():
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(email_user, email_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")

    except Exception as e:
        print ("Something went wrong….",e)


