import codecs
from datetime import datetime
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPRecipientsRefused
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
read_env = lambda property: os.environ.get(property, None) 


def process_email(*args, **kwargs):
    message = kwargs.get("message", None)
    title = kwargs.get("title", None)
    email = kwargs.get("email", None)
    subject = kwargs.get('subject', None)
    full_name = kwargs.get('full_name', None)
 
    try:
        timeNow = datetime.now()
        FROM_EMAIL = read_env('FROM_EMAIL')
        USERNAME = read_env('USERNAME')
        PASSWORD = read_env('PASSWORD')
        SMTP_PORT = read_env('SMTP_PORT')
        SMTP_HOST = read_env('SMTP_HOST')
        TO_EMAIL = read_env('TO_EMAIL')
        FROM = 'SlackBot <{FROM_EMAIL}>'
        SUBJECT = "New message from a customer"

        path = "templates/customer_question.html"

        try:
            f = codecs.open(path, 'r')
            m = f.read()
            mess = str.replace(m, '[full_name]', full_name)
            mess = str.replace(mess, '[title]', title)
            mess = str.replace(mess, '[subject]', subject)
            mess = str.replace(mess, '[message]', message) 
            mess = str.replace(mess, '[email]', email)           
            mess = str.replace(mess, '[greeting]', "Dear")
            mess = str.replace(mess, "[greeting_statement]", "Thank you for contacting us!")
            mess = str.replace(mess, '[greeting_global_link]', 'https://3dact.com')
            mess = str.replace(mess, "[wait_statement]", "While you're waiting, please research 3dact.com")
        except Exception as e:
            logger.error(f"Error parsing email ... {e}")         

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO_EMAIL
        MESSAGE['From'] = FROM_EMAIL
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""

        HTML_BODY  = MIMEText(mess, 'html','utf-8')
        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()
        server = smtplib.SMTP(SMTP_HOST+':'+SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg)
        server.quit()
        print("Successfully sent email")
    except Exception as e:
        print(f"Error sending email ...{e}")
        logger.error(f"Error sending email {e}") 


def process_customer_email(*args, **kwargs):
    message = kwargs.get("message", None)
    title = kwargs.get("title", None)
    email = kwargs.get("email", None)
    subject = kwargs.get('subject', None)
    full_name = kwargs.get('full_name', None)

    print(f"FULL {full_name} SUBJ {subject} EMAIL {email} TITLE {title} MESSAGE {message}")

    try:
        timeNow = datetime.now()
        FROM_EMAIL = read_env('FROM_EMAIL')
        USERNAME = read_env('USERNAME')
        PASSWORD = read_env('PASSWORD')
        SMTP_PORT = read_env('SMTP_PORT')
        SMTP_HOST= read_env('SMTP_HOST')
        TO_EMAIL = read_env('TO_EMAIL')

        FROM = 'SlackBot <{FROM_EMAIL}>'

        SUBJECT = "New message from a customer"
        path = "templates/customer_question.html"

        print(f"FROM_EMAIL {FROM_EMAIL}")
        print(f"TO_EMAIL {TO_EMAIL}")
        print(f"FROM {FROM}")
        print(f"SMTP_HOST {SMTP_HOST}")
        print(f"SMTP_PORT {SMTP_PORT}")
        print(f"PASSWORD {PASSWORD}")
        print(f"USERNAME {USERNAME}")

        try:
            f = codecs.open(path, 'r')
            m = f.read()
            mess = str.replace(m, '[full_name]', full_name)
            mess = str.replace(mess, '[greeting_global_link]', 'https://3dact.com')
            mess = str.replace(mess, '[greeting]', "Dear")
            mess = str.replace(mess, "[greeting_statement]", "Thank you for contacting us!")
            mess = str.replace(mess, '[title]', title)
            mess = str.replace(mess, '[subject]', subject)
            mess = str.replace(mess, '[message]', message) 
            mess = str.replace(mess, '[email]', email)           
            mess = str.replace(mess, "[wait_statement]", "While you're waiting, please research 3dact.com")
            mess = str.replace(mess, '[greeting_statement]', "Thank you for getting in touch with us!")
            mess = str.replace(mess, '[wait_statement]', "Please give us 1 day to respond!")
        except Exception as e:
            logger.error(f"Error parsing email ... {e}")         

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO_EMAIL
        MESSAGE['From'] = FROM
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""

        HTML_BODY  = MIMEText(mess, 'html','utf-8')
        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()
        server = smtplib.SMTP(SMTP_HOST+':'+SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(USERNAME,PASSWORD)
        server.sendmail(FROM, TO_EMAIL, msg)
        server.quit()
    except Exception as e:
        logger.error(f"Error sending email {e}") 


if __name__=='__main__':
    process_email(full_name="Dmitry R", email='dmitryro@gmail.com', title='Fancy Title',
                  subject='Fancy Subject', message='Fancy Message')


    process_customer_email(full_name="Dmitry R", email='dmitryro@gmail.com', title='Fancy Title',
                           subject='Fancy Subject', message='Fancy Message')
