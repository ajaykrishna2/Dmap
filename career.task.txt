import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import shutil
from zipfile import ZipFile
from os import path
email_user = 'ajay.panku2@gmail.com'
email_password = 'password'
email_send = 'lavanya.kr@tibilsolutions.com'

subject = 'subject'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Hi there, sending this email from Python!'
msg.attach(MIMEText(body,'plain'))

if path.exists("email.txt"):
    src = path.realpath("email.txt");
    root_dir, tail = path.split(src)
    shutil.make_archive("test archive", "zip", root_dir)
    with ZipFile("email.zip", "w") as newzip:
        newzip.write("email.txt")
if path.exists("email2.txt"):
    src = path.realpath("email2.txt");
    root_dir, tail = path.split(src)
    shutil.make_archive("test archive", "zip", root_dir)
    with ZipFile("email2.zip", "w") as newzip:
        newzip.write("email2.txt")



files=['email.zip','email2.zip']
for f in files:
    dir_path= "/home/ajay/PycharmProjects/pythonProject";
    file_path = os.path.join(dir_path, f)
    attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
    attachment.add_header('Content-Disposition', 'attachment', filename=f)
    msg.attach(attachment)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()