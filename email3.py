import smtplib
import os
from os import path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def multiple_attachments():
    dir_path = path.realpath("email.txt");
    files = ["email.txt", "email2.txt"]

    msg = MIMEMultipart()
    msg['To'] = "ajay.panku2@gmail.com"
    msg['From'] = "ajay.panku12@gmail.com"
    msg['Subject'] = "Sending multiple attachment"

    body = MIMEText('Test results attached.', 'html', 'utf-8')
    msg.attach(body)  # add message body (text or html)

    for f in files:  # add files to the message
        file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)

    s = smtplib.SMTP()
    s.connect(host=SMTP_SERVER)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    print('done!')
    s.close()