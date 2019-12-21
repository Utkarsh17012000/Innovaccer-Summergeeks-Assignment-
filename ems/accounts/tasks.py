from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep
import smtplib

@shared_task
def send_meeting_email(subject,body,frm,to,send_diff):
    sleep(send_diff)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('utkarshtanwar007@gmail.com','hzrplcmjymrjbyvh')

    msg = "Subject: {}\n\n{}".format(subject,body)

    server.sendmail(
        'utkarshtanwar007@gmail.com',
        'Bhargav999reddy@gmail.com',
        msg
    )
    server.close()


